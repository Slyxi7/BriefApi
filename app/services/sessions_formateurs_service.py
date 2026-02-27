from sqlalchemy.orm import Session
from app.models.sessions_foramteurs import SessionFormateur
from app.models.user import User
from app.models.session import Session as SessionModel

class SessionsFormateursService:


    @staticmethod
    def get_all(db: Session):
        return db.query(SessionFormateur).all()


    @staticmethod
    def get(db: Session, session_id: int, formateur_id: int):
        return (
            db.query(SessionFormateur)
            .filter(
                SessionFormateur.session_id == session_id,
                SessionFormateur.formateur_id == formateur_id
            )
            .first()
        )

    @staticmethod
    def create(db: Session, data):

        session = db.query(SessionModel).filter(SessionModel.id == data.session_id).first()
        if not session:
            raise ValueError("La session n'existe pas.")

        formateur = db.query(User).filter(User.id == data.formateur_id).first()
        if not formateur:
            raise ValueError("Le formateur spécifié n'existe pas.")

        if formateur.role != "formateur":
            raise ValueError("Seuls les formateurs peuvent être affectés à une session.")

        existing = SessionsFormateursService.get(db, data.session_id, data.formateur_id)
        if existing:
            raise ValueError("Ce formateur est déjà affecté à cette session.")
        
        sf = SessionFormateur(
            session_id=data.session_id,
            formateur_id=data.formateur_id
        )

        db.add(sf)
        db.commit()
        db.refresh(sf)
        return sf


    @staticmethod
    def update(db: Session, session_id: int, formateur_id: int, data):

        sf = SessionsFormateursService.get(db, session_id, formateur_id)
        if not sf:
            return None

        updated_fields = data.model_dump(exclude_unset=True)

        new_session_id = updated_fields.get("session_id", session_id)
        new_formateur_id = updated_fields.get("formateur_id", formateur_id)

        session = db.query(SessionModel).filter(SessionModel.id == new_session_id).first()
        if not session:
            raise ValueError("La nouvelle session n'existe pas.")

        formateur = db.query(User).filter(User.id == new_formateur_id).first()
        if not formateur:
            raise ValueError("Le formateur ne peut être trouvé.")

        if formateur.role != "formateur":
            raise ValueError("Seuls les formateurs peuvent être affectés.")

        if new_session_id != session_id or new_formateur_id != formateur_id:
            existing = SessionsFormateursService.get(db, new_session_id, new_formateur_id)
            if existing:
                raise ValueError("Cette affectation existe déjà.")

        for key, value in updated_fields.items():
            setattr(sf, key, value)

        db.commit()
        db.refresh(sf)
        return sf

    @staticmethod
    def delete(db: Session, session_id: int, formateur_id: int):
        sf = SessionsFormateursService.get(db, session_id, formateur_id)
        if not sf:
            return None

        db.delete(sf)
        db.commit()
        return True