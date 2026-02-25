from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer, String
from base import Base

class Formation(Base):
    __tablename__ = "formations"

    id: Mapped[int] = mapped_column(primary_key=True)
    titre : Mapped[str] = mapped_column(String(100), nullable=False)
    description : Mapped[str] = mapped_column(Text)
    duree : Mapped[int] = mapped_column(Integer, nullable=False)
    niveau : Mapped[str] = mapped_column(String(50), nullable=False)