from pydantic import BaseModel


class MessageInterpretation(BaseModel):
    intent: str
    urgency: str
    notes: str