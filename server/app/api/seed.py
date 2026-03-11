from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.employee import Employee
from app.models.store import Store
from app.models.shift import Shift



router = APIRouter()


@router.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    existing_store = db.query(Store).first()
    if existing_store:
        return {"message": "Seed data already exists"}

    store_1 = Store(name="Twin Liquors Hancock")
    store_2 = Store(name="Twin Liquors Mueller")

    db.add_all([store_1, store_2])
    db.commit()
    db.refresh(store_1)
    db.refresh(store_2)

    employees = [
        Employee(
            name="Maria",
            phone="+15125550001",
            role="floater",
            home_store_id=None,
            is_active=True,
        ),
        Employee(
            name="Josh",
            phone="+15125550002",
            role="dedicated",
            home_store_id=store_1.id,
            is_active=True,
        ),
        Employee(
            name="Elena",
            phone="+15125550003",
            role="dedicated",
            home_store_id=store_1.id,
            is_active=True,
        ),
        Employee(
            name="Marcus",
            phone="+15125550004",
            role="dedicated",
            home_store_id=store_2.id,
            is_active=True,
        ),
        Employee(
            name="Sonia",
            phone="+15125550005",
            role="manager",
            home_store_id=store_2.id,
            is_active=True,
        ),
    ]

    db.add_all(employees)
    db.commit()
    
    all_employees = db.query(Employee).all()
    employee_by_name = {employee.name: employee for employee in all_employees}
    
    shifts = [
    Shift(
        store_id=store_1.id,
        employee_id=employee_by_name["Josh"].id,
        date="2026-03-13",
        shift_type="open",
        status="scheduled",
    ),
    Shift(
        store_id=store_1.id,
        employee_id=employee_by_name["Elena"].id,
        date="2026-03-13",
        shift_type="close",
        status="scheduled",
    ),
    Shift(
        store_id=store_1.id,
        employee_id=employee_by_name["Maria"].id,
        date="2026-03-13",
        shift_type="close",
        status="scheduled",
    ),
    Shift(
        store_id=store_2.id,
        employee_id=employee_by_name["Marcus"].id,
        date="2026-03-13",
        shift_type="open",
        status="scheduled",
    ),
    Shift(
        store_id=store_2.id,
        employee_id=employee_by_name["Sonia"].id,
        date="2026-03-13",
        shift_type="close",
        status="scheduled",
    ),
]
    
    db.add_all(shifts)
    db.commit()

    return {
    "message": "Seed data created successfully",
    "stores_created": 2,
    "employees_created": len(employees),
    "shifts_created": len(shifts),
}