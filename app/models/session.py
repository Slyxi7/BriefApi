from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, Integer
from datetime import datetime
from app.models.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    formation_id: Mapped[int] = mapped_column(ForeignKey("formations.id"), nullable=False)
    date_debut: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    capacite: Mapped[int] = mapped_column(Integer, nullable=False)
