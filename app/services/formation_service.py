from sqlalchemy.orm import Session
from app.models.formation import Formation
from fastapi import HTTPException

class FormationService:

    @staticmethod
    def get_all_formations(db: Session):
        return db.query(Formation).all()

    @staticmethod
    def get_formation_by_id(db: Session, formation_id: int):
        return db.query(Formation).filter(Formation.id == formation_id).first()

    @staticmethod
    def create_formation(db: Session, formation_data):
        new_formation = Formation(
            titre=formation_data.titre,
            description=formation_data.description,
            duree=formation_data.duree,
            niveau=formation_data.niveau
        )

        db.add(new_formation)
        db.commit()
        db.refresh(new_formation)
        return new_formation


    @staticmethod
    def update_formation(db: Session, formation_id: int, formation_data):
        formation = FormationService.get_by_id(db, formation_id)
        if not formation:
            return None

        update_data = formation_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(formation, key, value)

        db.commit()
        db.refresh(formation)
        return formation

    @staticmethod
    def delete_formation(db: Session, formation_id: int):
        formation = FormationService.get_by_id(db, formation_id)
        if not formation:
            return None

        db.delete(formation)
        db.commit()
        return True

    @staticmethod
    def patch_formation(db: Session, formation_id: int, formation_data):
        formation = FormationService.get_formation_by_id(db, formation_id)
        if not formation:
            raise HTTPException(status_code=404, detail="Formation introuvable")

        update_data = formation_data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="Aucun champ fourni pour la mise à jour")

        for key, value in update_data.items():
            setattr(formation, key, value)

        db.commit()
        db.refresh(formation)
        return formation