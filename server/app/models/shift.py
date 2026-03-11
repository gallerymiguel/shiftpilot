from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Shift(Base):
    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    shift_type: Mapped[str] = mapped_column(String, nullable=False)  # open | mid10 | mid11 | close
    status: Mapped[str] = mapped_column(String, nullable=False, default="scheduled")  # scheduled | called_out | covered