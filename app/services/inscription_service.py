from sqlalchemy.orm import Session
from app.models.inscription import Inscription
from app.models.user import User
from app.models.session import Session as SessionModel

class InscriptionService:


    @staticmethod
    def get_all_inscription(db: Session):
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
    def create_inscription(db: Session, inscription_data):

        session = db.query(SessionModel).filter(SessionModel.id == inscription_data.session_id).first()
        if not session:
            raise ValueError("La session n'existe pas.")

        user = db.query(User).filter(User.id == inscription_data.apprenant_id).first()
        if not user:
            raise ValueError("L'apprenant n'existe pas.")

        if user.role != "apprenant":
            raise ValueError("Seuls les apprenants peuvent être inscrits à une session.")

        existing = InscriptionService.get(db, inscription_data.session_id, inscription_data.apprenant_id)
        if existing:
            raise ValueError("Cet apprenant est déjà inscrit à cette session.")

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

        inscription = InscriptionService.get(db, session_id, apprenant_id)
        if not inscription:
            return None

        updated_fields = inscription_data.model_dump(exclude_unset=True)

        new_session_id = updated_fields.get("session_id", session_id)
        new_apprenant_id = updated_fields.get("apprenant_id", apprenant_id)

        session = db.query(SessionModel).filter(SessionModel.id == new_session_id).first()
        if not session:
            raise ValueError("La session spécifiée n'existe pas.")

        user = db.query(User).filter(User.id == new_apprenant_id).first()
        if not user:
            raise ValueError("L'apprenant spécifié n'existe pas.")

        if user.role != "apprenant":
            raise ValueError("Seuls les apprenants peuvent être inscrits.")

        if (new_session_id != session_id or new_apprenant_id != apprenant_id):
            if InscriptionService.get(db, new_session_id, new_apprenant_id):
                raise ValueError("Cette inscription existe déjà.")

        for key, value in updated_fields.items():
            setattr(inscription, key, value)

        db.commit()
        db.refresh(inscription)
        return inscription


    @staticmethod
    def delete_inscription(db: Session, session_id: int, apprenant_id: int):
        inscription = InscriptionService.get(db, session_id, apprenant_id)
        if not inscription:
            return None

        db.delete(inscription)
        db.commit()
        return True