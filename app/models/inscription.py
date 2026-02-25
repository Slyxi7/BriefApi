from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from base import Base

class Inscription(Base):
    __tablename__ = "inscriptions"

    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), primary_key=True, nullable=False)
    apprenant_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, nullable=False)
