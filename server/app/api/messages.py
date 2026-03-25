from fastapi import APIRouter

from app.schemas.message import IncomingMessage
from app.services.interpreter import interpret_message

router = APIRouter()


@router.post("/interpret-message")
def interpret_incoming_message(payload: IncomingMessage):
    result = interpret_message(payload.message)

    return {
        "phone": payload.phone,
        "message": payload.message,
        "interpretation": result,
    }