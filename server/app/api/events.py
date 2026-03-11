from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.employee import Employee
from app.models.event import Event
from app.models.shift import Shift

router = APIRouter()


@router.post("/callout")
def employee_callout(phone: str, message: str, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(Employee.phone == phone).first()

    if not employee:
        return {"error": "Employee not found"}

    shift = db.query(Shift).filter(
        Shift.employee_id == employee.id,
        Shift.status == "scheduled"
    ).first()

    if not shift:
        return {"error": "No scheduled shift found"}

    shift.status = "called_out"

    event = Event(
        employee_id=employee.id,
        shift_id=shift.id,
        event_type="call_out",
        message=message,
        status="open"
    )

    db.add(event)
    db.commit()

    return {
        "message": "Call out recorded",
        "employee": employee.name,
        "shift_id": shift.id
    }