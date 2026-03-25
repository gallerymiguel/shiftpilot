from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models.shift import Shift
from app.db.deps import get_db
from app.services.retriever import seed_policy_collection

from app.api.recommendations import router as recommendation_router
from app.api.events import router as event_router
from app.api.seed import router as seed_router
from app.db.base import Base
from app.db.session import engine
from app.api.messages import router as message_router
from app.api.sms import router as sms_router

import app.models.employee  # noqa: F401
import app.models.store  # noqa: F401
import app.models.shift  # noqa: F401
import app.models.event  # noqa: F401


app = FastAPI(title="ShiftPilot API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_policy_collection()

app.include_router(seed_router)
app.include_router(event_router)
app.include_router(recommendation_router)
app.include_router(message_router)
app.include_router(sms_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/debug/shifts")
def debug_shifts(db: Session = Depends(get_db)):
    shifts = db.query(Shift).all()

    return [
        {
            "shift_id": shift.id,
            "store_id": shift.store_id,
            "employee_id": shift.employee_id,
            "date": shift.date,
            "shift_type": shift.shift_type,
            "status": shift.status,
        }
        for shift in shifts
    ]