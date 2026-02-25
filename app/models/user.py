from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String
from sqlalchemy import Enum as SQLEnum
from datetime import datetime
from base import Base
from enums.roles import Roles
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(50), nullable=False)
    prenom: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[Roles] =  mapped_column(SQLEnum(Roles), nullable=False)
    date_inscription: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
