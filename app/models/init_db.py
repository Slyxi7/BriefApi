from sqlalchemy import create_engine
from base import Base
from inscription import Inscription
from formation import Formation
from session import Session
from sessions_foramteurs import SessionFormateur
from user import User

engine = create_engine("sqlite:///database.db")

Base.metadata.create_all(bind=engine)
