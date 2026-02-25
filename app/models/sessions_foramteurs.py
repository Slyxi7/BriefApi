from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from base import Base

class SessionFormateur(Base):
    __tablename__ = "session_formateurs"

    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), primary_key=True, nullable=False)
    formateur_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, nullable=False)
