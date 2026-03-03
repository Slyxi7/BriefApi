from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.sessions_service import SessionService
from app.services.inscription_service import InscriptionService
from app.schemas.sessions import SessionsCreate, SessionsUpdate, SessionsRead,SessionsDelete

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get("/", response_model=list[SessionsRead])
def route_get_sessions(db: Session = Depends(get_db)):
    return SessionService.get_all_sessions(db)

@router.get("/{session_id}", response_model=SessionsRead)
def route_get_session_by_id(session_id: int, db: Session = Depends(get_db)):
    session = SessionService.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")
    return session

@router.post("/", response_model=SessionsRead, status_code=201)
def route_create_session(session: SessionsCreate, db: Session = Depends(get_db)):
    return SessionService.create_session(db, session)

@router.put("/{session_id}", response_model=SessionsRead)
def route_update_session(session_id: int, session_update: SessionsUpdate, db: Session = Depends(get_db)):
    session_db = SessionService.get_session_by_id(db, session_id)

    if not session_db:
        raise HTTPException(status_code=404, detail="Session introuvable")

    return SessionService.update_session(db, session_db, session_update)

@router.delete("/{session_id}")
def route_delete_session(session_id: int, delete_schema: SessionsDelete, db: Session = Depends(get_db)):
    session_db = SessionService.get_session_by_id(db, session_id)

    if not session_db:
        raise HTTPException(status_code=404, detail="Session introuvable")

    return SessionService.delete_session(db, session_db, delete_schema)

@router.get("/{session_id}/inscriptions")
def get_user_inscriptions(session_id: int, db: Session = Depends(get_db)):
    return InscriptionService.get_inscription_session(db, session_id)