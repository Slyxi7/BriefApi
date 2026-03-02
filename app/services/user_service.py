from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User
from fastapi import HTTPException, status
import bcrypt

class UserService:

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode('utf-8')


    @staticmethod
    def create_user(db: Session, user_data):
        hashed_pwd = UserService.hash_password(user_data.password)


        if UserService.get_user_by_email(db, user_data.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email déjà enregistré"
            )

        new_user = User(
            nom=user_data.nom,
            prenom=user_data.prenom,
            email=user_data.email,
            role=user_data.role,
            hashed_password= hashed_pwd,
            date_inscription=datetime.utcnow()
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_data):
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None

        db.delete(user)
        db.commit()
        return True