from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.formation import Formation

class FormationService:

    @staticmethod
    def get_all_formations(db: Session):
        return db.query(Formation).all()

    @staticmethod
    def get_formation_by_id(db: Session, formation_id: int):
        formation = db.query(Formation).filter(Formation.id == formation_id).first()
        if not formation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Training program not found",
            )
        return formation

    @staticmethod
    def create_formation(db: Session, formation_data):
        new_formation = Formation(
            titre=formation_data.titre,
            description=formation_data.description,
            duree=formation_data.duree,
            niveau=formation_data.niveau,
        )

        db.add(new_formation)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A training program with this title already exists",
            )

        db.refresh(new_formation)
        return new_formation

    @staticmethod
    def update_formation(db: Session, formation_id: int, formation_data):
        formation = FormationService.get_formation_by_id(db, formation_id)

        update_data = formation_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(formation, key, value)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A training program with this title already exists",
            )

        db.refresh(formation)
        return formation

    @staticmethod
    def delete_formation(db: Session, formation_id: int):
        formation = FormationService.get_formation_by_id(db, formation_id)

        db.delete(formation)
        db.commit()
        return True

    @staticmethod
    def patch_formation(db: Session, formation_id: int, formation_data):
        formation = FormationService.get_formation_by_id(db, formation_id)

        update_data = formation_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        for key, value in update_data.items():
            setattr(formation, key, value)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A training program with this title already exists",
            )

        db.refresh(formation)
        return formation