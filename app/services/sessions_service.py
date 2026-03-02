from sqlalchemy.orm import Session
from app.models.session import Session as Sessions
from app.schemas.sessions import SessionsCreate, SessionsUpdate, SessionsRead, SessionsDelete

class SessionService:

    @staticmethod
    def get_all_sessions(db: Session):
        return db.query(Sessions).all()

    @staticmethod
    def get_session_by_id(db: Session, Sessions_id: int):
        return db.query(Sessions).filter(Sessions.id == Sessions_id).first()

    @staticmethod
    def create_session(db: Session, session_data):

        new_session = Sessions(
            formation_id=session_data.formation_id,
            date_debut=session_data.date_debut,
            date_fin=session_data.date_fin,
            capacite=session_data.capacite,
        )

        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session

    @staticmethod
    def update_user(db: Session, session_id: int, session_data):
        session = SessionService.get_session_by_id(db, session_id)
        if not session:
            return None

        update_data = session_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(session, key, value)

        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def delete_session(db: Session, session_id: int):
        session = SessionService.get_session_by_id(db, session_id)
        if not session:
            return None

        db.delete(session)
        db.commit()
        return True