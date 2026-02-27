# routers/sessions_formateurs_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.sessions_formateurs import (
    SessionsFormateursCreate,
    SessionsFormateursUpdate,
    SessionsFormateursRead
)
from services.sessions_formateurs_services import SessionsFormateursService

router = APIRouter(prefix="/sessions-formateurs", tags=["Sessions - Formateurs"])

@router.post("/", response_model=SessionsFormateursRead)
def link_formateur(payload: SessionsFormateursCreate, db: Session = Depends(get_db)):
    return SessionsFormateursService.create_relation(db, payload)

@router.get("/", response_model=list[SessionsFormateursRead])
def get_all(db: Session = Depends(get_db)):
    return SessionsFormateursService.get_all_relations(db)

@router.get("/{session_id}/{formateur_id}", response_model=SessionsFormateursRead)
def get_one(session_id: int, formateur_id: int, db: Session = Depends(get_db)):
    return SessionsFormateursService.get_relation(db, session_id, formateur_id)

@router.put("/{session_id}/{formateur_id}", response_model=SessionsFormateursRead)
def update_relation(
    session_id: int,
    formateur_id: int,
    payload: SessionsFormateursUpdate,
    db: Session = Depends(get_db)
):
    return SessionsFormateursService.update_relation(db, session_id, formateur_id, payload)

@router.delete("/{session_id}/{formateur_id}")
def delete_relation(session_id: int, formateur_id: int, db: Session = Depends(get_db)):
    return SessionsFormateursService.delete_relation(db, session_id, formateur_id)