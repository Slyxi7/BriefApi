from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
import bcrypt

from app.models.user import User


class UserService:

    @staticmethod
    def get_all_users(db: Session, include_deleted: bool = False):
        q = db.query(User)
        if not include_deleted:
            q = q.filter(User.is_deleted.is_(False))
        return q.all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int, include_deleted: bool = False):
        q = db.query(User).filter(User.id == user_id)
        if not include_deleted:
            q = q.filter(User.is_deleted.is_(False))
        user = q.first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str, include_deleted: bool = False):
        q = db.query(User).filter(User.email == email)
        if not include_deleted:
            q = q.filter(User.is_deleted.is_(False))
        return q.first()

    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed_bytes.decode("utf-8")

    @staticmethod
    def create_user(db: Session, user_data):
        if UserService.get_user_by_email(db, user_data.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        hashed_pwd = UserService.hash_password(user_data.password)

        new_user = User(
            nom=user_data.nom,
            prenom=user_data.prenom,
            email=user_data.email,
            role=user_data.role,
            hashed_password=hashed_pwd,
            date_inscription=datetime.utcnow(),
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_data):
        user = UserService.get_user_by_id(db, user_id)

        update_data = user_data.model_dump(exclude_unset=True)

        new_email = update_data.get("email")
        if new_email and new_email != user.email:
            if UserService.get_user_by_email(db, new_email) is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already in use",
                )

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int, hard: bool = False):
        user = UserService.get_user_by_id(db, user_id, include_deleted=True)

        if hard:
            db.delete(user)
        else:
            user.is_deleted = True

        db.commit()
        return True

    @staticmethod
    def patch_user(db: Session, user_id: int, user_data):
        user = UserService.get_user_by_id(db, user_id)

        update_data = user_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        new_email = update_data.get("email")
        if new_email and new_email != user.email:
            if UserService.get_user_by_email(db, new_email) is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already in use",
                )

        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user