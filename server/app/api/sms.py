import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.employee import Employee
from app.models.event import Event
from app.models.shift import Shift
from app.schemas.message import IncomingMessage
from app.services.drafter import generate_cover_message
from app.services.explainer import generate_cover_explanation
from app.services.interpreter import interpret_message
from app.services.retriever import retrieve_policies

router = APIRouter()


@router.post("/sms")
def handle_sms(payload: IncomingMessage, db: Session = Depends(get_db)):
    interpretation = interpret_message(payload.message)
    intent = interpretation.get("intent")

    if intent != "call_out":
        return {
            "status": "ignored",
            "phone": payload.phone,
            "message": payload.message,
            "interpretation": interpretation,
        }

    employee = db.query(Employee).filter(Employee.phone == payload.phone).first()

    if not employee:
        return {"error": "Employee not found"}

    shift = (
        db.query(Shift)
        .filter(Shift.employee_id == employee.id, Shift.status == "scheduled")
        .first()
    )

    if not shift:
        return {"error": "No scheduled shift found"}

    shift.status = "called_out"

    event = Event(
        employee_id=employee.id,
        shift_id=shift.id,
        event_type="call_out",
        message=payload.message,
        status="open",
    )
    db.add(event)
    db.commit()

    employees_already_scheduled = (
        db.query(Shift.employee_id)
        .filter(
            Shift.date == shift.date,
            Shift.shift_type == shift.shift_type,
            Shift.status == "scheduled",
        )
        .all()
    )

    scheduled_employee_ids = {row[0] for row in employees_already_scheduled}
    candidates = db.query(Employee).filter(Employee.is_active == True).all()

    ranked_candidates = []

    for candidate in candidates:
        if candidate.id == shift.employee_id:
            continue

        if candidate.id in scheduled_employee_ids:
            continue

        priority = 99
        reason = "fallback option"

        if candidate.role == "floater":
            priority = 1
            reason = "floater available for coverage"
        elif (
            candidate.role == "dedicated" and candidate.home_store_id == shift.store_id
        ):
            priority = 2
            reason = "dedicated employee from same store"
        elif (
            candidate.role == "dedicated" and candidate.home_store_id != shift.store_id
        ):
            priority = 3
            reason = "dedicated employee from another store"
        elif candidate.role == "manager":
            priority = 4
            reason = "manager can cover as emergency option"

        ranked_candidates.append(
            {
                "employee_id": candidate.id,
                "name": candidate.name,
                "role": candidate.role,
                "home_store_id": candidate.home_store_id,
                "priority": priority,
                "reason": reason,
            }
        )

    ranked_candidates.sort(key=lambda x: x["priority"])

    policy_query = f"""
    Call-out coverage rules for a {shift.shift_type} shift.
    Relevant policies about replacement priority, same-store coverage, floaters, managers, and shift type rules.
    """
    retrieved_policies = retrieve_policies(policy_query)

    explanation = generate_cover_explanation(
        shift_id=shift.id,
        store_id=shift.store_id,
        date=str(shift.date),
        shift_type=shift.shift_type,
        recommendations=ranked_candidates,
        policies=retrieved_policies,
    )

    draft_message = generate_cover_message(
        store_id=shift.store_id,
        date=str(shift.date),
        shift_type=shift.shift_type,
        recommendations=ranked_candidates,
    )

    result = {
        "status": "call_out_recorded",
        "phone": payload.phone,
        "employee": employee.name,
        "shift_id": shift.id,
        "interpretation": interpretation,
        "retrieved_policies": retrieved_policies,
        "recommendations": ranked_candidates,
        "explanation": explanation,
        "draft_message": draft_message,
    }

    print("🔥 ABOUT TO CALL N8N WEBHOOK")

    try:
        webhook_response = requests.post(
            "http://shiftpilot-n8n:5678/webhook-test/6d2e6446-9109-44a4-a6f1-4405d332104a",
            json=result,
            timeout=5,
        )
        print("n8n webhook status:", webhook_response.status_code)
        print("n8n webhook response:", webhook_response.text)
    except Exception as e:
        print("Failed to send to n8n:", e)

    return result
