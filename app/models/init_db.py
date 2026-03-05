from sqlalchemy import create_engine
from app.models.base import Base
from app.models.inscription import Inscription
from app.models.formation import Formation
from app.models.session import Session
from app.models.user import User

engine = create_engine("sqlite:///./database.db")

Base.metadata.create_all(bind=engine)
