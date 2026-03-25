from pydantic import BaseModel


class IncomingMessage(BaseModel):
    phone: str
    message: str