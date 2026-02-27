# routers/formation_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.formation import FormationCreate, FormationUpdate, InscriptionRead
from services.formation_services import FormationService

router = APIRouter(prefix="/formations", tags=["Formations"])

@router.post("/", response_model=InscriptionRead)
def create_formation(payload: FormationCreate, db: Session = Depends(get_db)):
    return FormationService.create_formation(db, payload)

@router.get("/", response_model=list[InscriptionRead])
def list_formations(db: Session = Depends(get_db)):
    return FormationService.get_all_formations(db)

@router.get("/{formation_id}", response_model=InscriptionRead)
def get_formation(formation_id: int, db: Session = Depends(get_db)):
    return FormationService.get_formation_by_id(db, formation_id)

@router.put("/{formation_id}", response_model=InscriptionRead)
def update_formation(
    formation_id: int,
    payload: FormationUpdate,
    db: Session = Depends(get_db)
):
    return FormationService.update_formation(db, formation_id, payload)

@router.delete("/{formation_id}")
def delete_formation(formation_id: int, db: Session = Depends(get_db)):
    return FormationService.delete_formation(db, formation_id)