from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.models.formation import Formation
from fastapi import HTTPException, status

class SessionService:

    @staticmethod
    def get_all_sessions(db: Session):
        return db.query(SessionModel).all()

    @staticmethod
    def get_session_by_id(db: Session, Sessions_id: int):
        return db.query(SessionModel).filter(SessionModel.id == Sessions_id).first()

    @staticmethod
    def get_sessions_by_formation(db: Session, formation_id: int):
        return db.query(SessionModel).filter(SessionModel.formation_id == formation_id).all()

    @staticmethod
    def create_session(db: Session, session_data):

        if not db.query(Formation).filter(Formation.id == session_data.formation_id).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La formation n'existe pas "
            )

        new_session = SessionModel(
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
    
    @staticmethod
    def patch_session(db: Session, session_id: int, session_data):
        session = SessionService.get_session_by_id(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session introuvable")

        update_data = session_data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="Aucun champ fourni pour la mise à jour")

        for key, value in update_data.items():
            setattr(session, key, value)

        db.commit()
        db.refresh(session)
        return session