from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.inscription import InscriptionCreate, InscriptionUpdate, InscriptionRead
from app.services.inscription_service import InscriptionService

router = APIRouter(prefix="/inscriptions", tags=["Inscriptions"])

@router.post("/", response_model=InscriptionRead)
def create_inscription(payload: InscriptionCreate, db: Session = Depends(get_db)):
    return InscriptionService.create_inscription(db, payload)

@router.get("/", response_model=list[InscriptionRead])
def list_inscriptions(db: Session = Depends(get_db)):
    return InscriptionService.get_all_inscriptions(db)

@router.get("/{session_id}/{apprenant_id}", response_model=InscriptionRead)
def get_inscription(session_id: int, apprenant_id: int, db: Session = Depends(get_db)):
    return InscriptionService.get_inscription(db, session_id, apprenant_id)

@router.put("/{session_id}/{apprenant_id}", response_model=InscriptionRead)
def update_inscription(
    session_id: int,
    apprenant_id: int,
    payload: InscriptionUpdate,
    db: Session = Depends(get_db)
):
    return InscriptionService.update_inscription(db, session_id, apprenant_id, payload)

@router.delete("/{session_id}/{apprenant_id}")
def delete_inscription(session_id: int, apprenant_id: int, db: Session = Depends(get_db)):
    return InscriptionService.delete_inscription(db, session_id, apprenant_id)