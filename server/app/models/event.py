from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    shift_id: Mapped[int] = mapped_column(ForeignKey("shifts.id"))

    event_type: Mapped[str] = mapped_column(String, nullable=False)  
    # call_out | late | availability_change

    message: Mapped[str] = mapped_column(String, nullable=True)

    status: Mapped[str] = mapped_column(String, default="open")
    # open | resolved