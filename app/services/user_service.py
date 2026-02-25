from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
from app.model.base import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create(db: Session, user_data):
        """Création d’un utilisateur"""
        hashed_pwd = UserService.hash_password(user_data.password)

        new_user = User(
            nom=user_data.nom,
            prenom=user_data.prenom,
            email=user_data.email,
            role=user_data.role,
            hashed_password=hashed_pwd,
            date_inscription=datetime.utcnow()
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update(db: Session, user_id: int, user_data):
        user = UserService.get_by_id(db, user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        # empêcher update du mot de passe ici (sauf si tu veux l’ajouter)
        if "password" in update_data:
            update_data["hashed_password"] = UserService.hash_password(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int):
        """Suppression définitive (car pas de soft delete dans ton modèle)"""
        user = UserService.get_by_id(db, user_id)
        if not user:
            return None

        db.delete(user)
        db.commit()
        return True