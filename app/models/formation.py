from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer, String
from sqlalchemy import Enum as SQLEnum
from app.models.base import Base
from app.enums.level import Level

class Formation(Base):
    __tablename__ = "formations"

    id: Mapped[int] = mapped_column(primary_key=True)
    titre : Mapped[str] = mapped_column(String(100), nullable=False)
    description : Mapped[str] = mapped_column(Text)
    duree : Mapped[int] = mapped_column(Integer, nullable=False)
    niveau: Mapped[Level] = mapped_column(SQLEnum(Level), nullable=False)