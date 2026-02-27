from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

# Services
from services.sessions_services import (
    get_sessions,
    get_session_by_id,
    create_session,
    update_session,
    delete_session
)

# Schemas
from schemas.sessions_schema import (
    SessionsCreate,
    SessionsUpdate,
    SessionsRead,
    SessionsDelete
)

router = APIRouter(prefix="/sessions", tags=["Sessions"])



@router.get("/", response_model=list[SessionsRead])
def route_get_sessions(db: Session = Depends(get_db)):
    return get_sessions(db)



@router.get("/{session_id}", response_model=SessionsRead)
def route_get_session_by_id(session_id: int, db: Session = Depends(get_db)):
    session = get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")
    return session

@router.post("/", response_model=SessionsRead, status_code=201)
def route_create_session(session: SessionsCreate, db: Session = Depends(get_db)):
    return create_session(db, session)


@router.put("/{session_id}", response_model=SessionsRead)
def route_update_session(session_id: int, session_update: SessionsUpdate, db: Session = Depends(get_db)):
    session_db = get_session_by_id(db, session_id)

    if not session_db:
        raise HTTPException(status_code=404, detail="Session introuvable")

    return update_session(db, session_db, session_update)


@router.delete("/{session_id}")
def route_delete_session(session_id: int, delete_schema: SessionsDelete, db: Session = Depends(get_db)):
    session_db = get_session_by_id(db, session_id)

    if not session_db:
        raise HTTPException(status_code=404, detail="Session introuvable")

    return delete_session(db, session_db, delete_schema)