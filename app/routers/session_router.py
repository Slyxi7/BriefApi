from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.sessions_service import SessionService
from app.services.inscription_service import InscriptionService
from app.schemas.sessions import SessionsCreate, SessionsUpdate, SessionsRead,SessionsDelete

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.get(
    "/",
    response_model=list[SessionsRead],
    summary="List all sessions",
    description="Returns the list of all training sessions available in the database.",
    responses={
        200: {"description": "Session list retrieved successfully"}
    }
)
def route_get_sessions(db: Session = Depends(get_db)):
    return SessionService.get_all_sessions(db)


@router.get(
    "/{session_id}",
    response_model=SessionsRead,
    summary="Get a session",
    description="Returns the information of a specific session using its identifier.",
    responses={
        200: {"description": "Session found"},
        404: {"description": "Session not found"}
    }
)
def route_get_session_by_id(session_id: int, db: Session = Depends(get_db)):
    session = SessionService.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post(
    "/",
    response_model=SessionsRead,
    status_code=201,
    summary="Create a session",
    description="Creates a new training session with an associated training program, instructor, dates, and maximum capacity.",
    responses={
        201: {"description": "Session created successfully"},
        400: {"description": "Invalid data"},
        404: {"description": "Training program or instructor not found"}
    }
)
def route_create_session(session: SessionsCreate, db: Session = Depends(get_db)):
    return SessionService.create_session(db, session)

@router.put(
    "/{session_id}",
    response_model=SessionsRead,
    summary="Update a session",
    description="Updates the information of an existing session (dates, capacity, instructor, training program).",
    responses={
        200: {"description": "Session updated successfully"},
        404: {"description": "Session not found"},
        400: {"description": "Invalid data"}
    }
)
def route_update_session(session_id: int, session_update: SessionsUpdate, db: Session = Depends(get_db)):
    session_db = SessionService.get_session_by_id(db, session_id)

    if not session_db:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionService.update_session(db, session_db, session_update)

@router.delete(
    "/{session_id}",
    status_code=204,
    summary="Delete a session",
    description="Deletes an existing session from the database using its identifier.",
    responses={
        204: {"description": "Session deleted successfully"},
        404: {"description": "Session not found"}
    }
)
def route_delete_session(session_id: int, delete_schema: SessionsDelete, db: Session = Depends(get_db)):
    session_db = SessionService.get_session_by_id(db, session_id)

    if not session_db:
        raise HTTPException(status_code=404, detail="Session not foun")

    return SessionService.delete_session(db, session_db, delete_schema)

@router.get(
    "/{session_id}/inscriptions",
    summary="List session enrollments",
    description="Returns the list of enrollments (learners registered) for a given session.",
    responses={
        200: {"description": "Enrollment list retrieved successfully"},
        404: {"description": "Session not found"}
    }
)
def get_user_inscriptions(session_id: int, db: Session = Depends(get_db)):
    return InscriptionService.get_inscription_session(db, session_id)

@router.patch(
    "/{session_id}",
    response_model=SessionsRead,
    summary="Partially update a session",
    description="Updates one or more fields of an existing session.",
    responses={
        200: {"description": "Session updated successfully"},
        404: {"description": "Session not found"},
        400: {"description": "No fields provided for update"}
    }
)
def patch_session(
    session_id: int,
    payload: SessionsUpdate,
    db: Session = Depends(get_db)
):
    return SessionService.patch_session(db, session_id, payload)