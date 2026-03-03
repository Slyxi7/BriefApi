from sqlalchemy.orm import Session
from app.models.inscription import Inscription
from app.models.user import User
from app.models.session import Session as SessionModel
from fastapi import HTTPException, status
from sqlalchemy import func

class InscriptionService:


    @staticmethod
    def get_all_inscriptions(db: Session):
        return db.query(Inscription).all()

    @staticmethod
    def get_inscription(db: Session, session_id: int, apprenant_id: int):
        return (
            db.query(Inscription)
            .filter(
                Inscription.session_id == session_id,
                Inscription.apprenant_id == apprenant_id
            )
            .first()
        )

    @staticmethod
    def get_inscription_session(db: Session, session_id: int):
        return (
            db.query(Inscription)
            .filter(Inscription.session_id == session_id).all()
        )

    @staticmethod
    def get_inscription_user(db: Session, apprenant_id: int):
        return (
            db.query(Inscription)
            .filter(Inscription.apprenant_id == apprenant_id).all()
        )
    
    @staticmethod
    def count_apprenants_in_session(db: Session, session_id: int) -> int:
        return (
            db.query(func.count(Inscription.apprenant_id))
            .join(User, User.id == Inscription.apprenant_id)
            .filter(Inscription.session_id == session_id)
            .filter(User.role == "apprenant")
            .scalar()
        ) or 0

    @staticmethod
    def create_inscription(db: Session, inscription_data):
        count = 0
        session = db.query(SessionModel).filter(SessionModel.id == inscription_data.session_id).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La session n'existe pas ."
            )

        user = db.query(User).filter(User.id == inscription_data.apprenant_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="L'utilisateur n'existe pas."
            )

        if user.role != "apprenant" and user.role != "formateur":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vous n'avez pas acces a cette session"
            )

        if InscriptionService.get_inscription(db, inscription_data.session_id, inscription_data.apprenant_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="L'utilisateur est deja inscrit a cette session."
            )

        count = InscriptionService.count_apprenants_in_session(db, inscription_data.session_id)

        if user.role == "apprenant" and count >= session.capacite:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Trop de personne inscrite"
            )

        inscription = Inscription(
            session_id=inscription_data.session_id,
            apprenant_id=inscription_data.apprenant_id
        )

        db.add(inscription)
        db.commit()
        db.refresh(inscription)
        return inscription

    @staticmethod
    def update_inscription(db: Session, session_id: int, apprenant_id: int, inscription_data):

        inscription = InscriptionService.get_inscription(db, session_id, apprenant_id)
        if not inscription:
            return None

        updated_fields = inscription_data.model_dump(exclude_unset=True)

        new_session_id = updated_fields.get("session_id", session_id)
        new_apprenant_id = updated_fields.get("apprenant_id", apprenant_id)

        session = db.query(SessionModel).filter(SessionModel.id == new_session_id).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La session n'existe pas "
            )

        user = db.query(User).filter(User.id == new_apprenant_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="L'apprenant n'existe pas"
            )

        if user.role != "apprenant" and user.role != "formateur":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Seul les apprenants peuvnt etre inscrit. "
            )

        if (new_session_id != session_id or new_apprenant_id != apprenant_id):
            if InscriptionService.get(db, new_session_id, new_apprenant_id):
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="L'apprenant est deja inscrit a cette session."
            )

        for key, value in updated_fields.items():
            setattr(inscription, key, value)

        db.commit()
        db.refresh(inscription)
        return inscription


    @staticmethod
    def delete_inscription(db: Session, session_id: int, apprenant_id: int):
        inscription = InscriptionService.get_inscription(db, session_id, apprenant_id)
        if not inscription:
            return None

        db.delete(inscription)
        db.commit()
        return True