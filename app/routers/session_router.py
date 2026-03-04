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
    summary="Lister toutes les sessions",
    description="Retourne la liste de toutes les sessions de formation disponibles dans la base de données.",
    responses={
        200: {"description": "Liste des sessions récupérée avec succès"}
    }
)
def route_get_sessions(db: Session = Depends(get_db)):
    return SessionService.get_all_sessions(db)

@router.get(
    "/{session_id}",
    response_model=SessionsRead,
    summary="Récupérer une session",
    description="Retourne les informations d'une session spécifique à partir de son identifiant.",
    responses={
        200: {"description": "Session trouvée"},
        404: {"description": "Session introuvable"}
    }
)
def route_get_session_by_id(session_id: int, db: Session = Depends(get_db)):
    session = SessionService.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable")
    return session

@router.post(
    "/",
    response_model=SessionsRead,
    status_code=201,
    summary="Créer une session",
    description="Crée une nouvelle session de formation avec une formation associée, un formateur, des dates et une capacité maximale.",
    responses={
        201: {"description": "Session créée avec succès"},
        400: {"description": "Données invalides"},
        404: {"description": "Formation ou formateur introuvable"}
    }
)
def route_create_session(session: SessionsCreate, db: Session = Depends(get_db)):
    return SessionService.create_session(db, session)

@router.put(
    "/{session_id}",
    response_model=SessionsRead,
    summary="Mettre à jour une session",
    description="Met à jour les informations d'une session existante (dates, capacité, formateur, formation).",
    responses={
        200: {"description": "Session mise à jour avec succès"},
        404: {"description": "Session introuvable"},
        400: {"description": "Données invalides"}
    }
)
def route_update_session(session_id: int, session_update: SessionsUpdate, db: Session = Depends(get_db)):
    session_db = SessionService.get_session_by_id(db, session_id)

    if not session_db:
        raise HTTPException(status_code=404, detail="Session introuvable")

    return SessionService.update_session(db, session_db, session_update)

@router.delete(
    "/{session_id}",
    status_code=204,
    summary="Supprimer une session",
    description="Supprime une session existante de la base de données à partir de son identifiant.",
    responses={
        204: {"description": "Session supprimée avec succès"},
        404: {"description": "Session introuvable"}
    }
)
def route_delete_session(session_id: int, delete_schema: SessionsDelete, db: Session = Depends(get_db)):
    session_db = SessionService.get_session_by_id(db, session_id)

    if not session_db:
        raise HTTPException(status_code=404, detail="Session introuvable")

    return SessionService.delete_session(db, session_db, delete_schema)

@router.get(
    "/{session_id}/inscriptions",
    summary="Lister les inscriptions d'une session",
    description="Retourne la liste des inscriptions (apprenants inscrits) pour une session donnée.",
    responses={
        200: {"description": "Liste des inscriptions récupérée avec succès"},
        404: {"description": "Session introuvable"}
    }
)
def get_user_inscriptions(session_id: int, db: Session = Depends(get_db)):
    return InscriptionService.get_inscription_session(db, session_id)

@router.patch(
    "/{session_id}",
    response_model=SessionsRead,
    summary="Mettre à jour partiellement une session",
    description="Met à jour un ou plusieurs champs d'une session existante.",
    responses={
        200: {"description": "Session mise à jour avec succès"},
        404: {"description": "Session introuvable"},
        400: {"description": "Aucun champ fourni pour la mise à jour"}
    }
)
def patch_session(
    session_id: int,
    payload: SessionsUpdate,
    db: Session = Depends(get_db)
):
    return SessionService.patch_session(db, session_id, payload)