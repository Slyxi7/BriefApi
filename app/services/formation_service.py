from sqlalchemy.orm import Session
from app.model.base import Formation  # adapte ton import selon ton arbo


class FormationService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Formation).all()


    @staticmethod
    def get_by_id(db: Session, formation_id: int):
        return db.query(Formation).filter(Formation.id == formation_id).first()


    @staticmethod
    def create(db: Session, formation_data):
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
    def update(db: Session, formation_id: int, formation_data):
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
    def delete(db: Session, formation_id: int):
        formation = FormationService.get_by_id(db, formation_id)
        if not formation:
            return None

        db.delete(formation)
        db.commit()
        return True