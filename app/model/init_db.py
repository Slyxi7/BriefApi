from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, ForeignKey, DateTime, Text, Integer, String
from datetime import datetime

engine = create_engine("sqlite:///database.db")

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(50), nullable=False)
    prenom: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    date_inscription: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

class Formation(Base):
    __tablename__ = "formations"

    id: Mapped[int] = mapped_column(primary_key=True)
    titre : Mapped[str] = mapped_column(String(100), nullable=False)
    description : Mapped[str] = mapped_column(Text)
    duree : Mapped[int] = mapped_column(Integer, nullable=False)
    niveau : Mapped[str] = mapped_column(String(50), nullable=False)

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    formation_id: Mapped[int] = mapped_column(ForeignKey("formations.id"), nullable=False)
    date_debut: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    capacite: Mapped[int] = mapped_column(Integer, nullable=False)

class Inscription(Base):
    __tablename__ = "inscriptions"

    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), primary_key=True, nullable=False)
    apprenant_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, nullable=False)

class SessionFormateur(Base):
    __tablename__ = "session_formateurs"

    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), primary_key=True, nullable=False)
    formateur_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, nullable=False)

Base.metadata.create_all(bind=engine)
