from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.inscription import Inscription
from app.models.user import User
from app.models.session import Session as SessionModel


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
        return db.query(Inscription).filter(Inscription.session_id == session_id).all()

    @staticmethod
    def get_inscription_user(db: Session, apprenant_id: int):
        return db.query(Inscription).filter(Inscription.apprenant_id == apprenant_id).all()

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
        session = db.query(SessionModel).filter(SessionModel.id == inscription_data.session_id).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        user = db.query(User).filter(User.id == inscription_data.apprenant_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.role not in ("apprenant", "formateur"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this session",
            )

        if InscriptionService.get_inscription(db, inscription_data.session_id, inscription_data.apprenant_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already enrolled in this session",
            )

        count = InscriptionService.count_apprenants_in_session(db, inscription_data.session_id)
        if user.role == "apprenant" and count >= session.capacite:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is full",
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found",
            )

        updated_fields = inscription_data.model_dump(exclude_unset=True)

        new_session_id = updated_fields.get("session_id", session_id)
        new_apprenant_id = updated_fields.get("apprenant_id", apprenant_id)

        session = db.query(SessionModel).filter(SessionModel.id == new_session_id).first()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        user = db.query(User).filter(User.id == new_apprenant_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.role not in ("apprenant", "formateur"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only learners or instructors can be enrolled",
            )

        if (new_session_id != session_id or new_apprenant_id != apprenant_id):
            if InscriptionService.get_inscription(db, new_session_id, new_apprenant_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User is already enrolled in this session",
                )

        if user.role == "apprenant":
            count = InscriptionService.count_apprenants_in_session(db, new_session_id)
            if count >= session.capacite:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Session is full",
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found",
            )

        db.delete(inscription)
        db.commit()
        return True