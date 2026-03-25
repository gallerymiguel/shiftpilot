from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.employee import Employee
from app.models.shift import Shift
from app.services.explainer import generate_cover_explanation
from app.services.retriever import retrieve_policies

router = APIRouter()


@router.get("/recommend-cover/{shift_id}")
def recommend_cover(shift_id: int, db: Session = Depends(get_db)):
    target_shift = db.query(Shift).filter(Shift.id == shift_id).first()

    if not target_shift:
        return {"error": "Shift not found"}

    if target_shift.status != "called_out":
        return {"error": "Shift is not marked as called_out"}

    employees_already_scheduled = (
        db.query(Shift.employee_id)
        .filter(
            Shift.date == target_shift.date,
            Shift.shift_type == target_shift.shift_type,
            Shift.status == "scheduled",
        )
        .all()
    )

    scheduled_employee_ids = {row[0] for row in employees_already_scheduled}

    candidates = db.query(Employee).filter(Employee.is_active == True).all()

    ranked_candidates = []

    for employee in candidates:
        if employee.id == target_shift.employee_id:
            continue

        if employee.id in scheduled_employee_ids:
            continue

        priority = 99
        reason = "fallback option"

        if employee.role == "floater":
            priority = 1
            reason = "floater available for coverage"
        elif (
            employee.role == "dedicated"
            and employee.home_store_id == target_shift.store_id
        ):
            priority = 2
            reason = "dedicated employee from same store"
        elif (
            employee.role == "dedicated"
            and employee.home_store_id != target_shift.store_id
        ):
            priority = 3
            reason = "dedicated employee from another store"
        elif employee.role == "manager":
            priority = 4
            reason = "manager can cover as emergency option"

        ranked_candidates.append(
            {
                "employee_id": employee.id,
                "name": employee.name,
                "role": employee.role,
                "home_store_id": employee.home_store_id,
                "priority": priority,
                "reason": reason,
            }
        )

    ranked_candidates.sort(key=lambda candidate: candidate["priority"])

    policy_query = f"Coverage rules for a {target_shift.shift_type} shift on {target_shift.date} at store {target_shift.store_id}"
    retrieved_policies = retrieve_policies(policy_query)

    explanation = generate_cover_explanation(
        shift_id=target_shift.id,
        store_id=target_shift.store_id,
        date=str(target_shift.date),
        shift_type=target_shift.shift_type,
        recommendations=ranked_candidates,
        policies=retrieved_policies,
    )

    return {
        "shift_id": target_shift.id,
        "store_id": target_shift.store_id,
        "date": target_shift.date,
        "shift_type": target_shift.shift_type,
        "retrieved_policies": retrieved_policies,
        "recommendations": ranked_candidates,
        "explanation": explanation,
    }
