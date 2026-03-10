from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
import app.models.store  # noqa: F401

app = FastAPI(title="ShiftPilot API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}