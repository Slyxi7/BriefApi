from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.inscription import InscriptionCreate, InscriptionUpdate, InscriptionRead
from app.services.inscription_service import InscriptionService

router = APIRouter(prefix="/inscriptions", tags=["Inscriptions"])

@router.post(
    "/",
    response_model=InscriptionRead,
    status_code=201,
    summary="Créer une inscription",
    description="Inscrit un apprenant à une session de formation.",
    responses={
        201: {"description": "Inscription créée avec succès"},
        404: {"description": "Session ou apprenant introuvable"},
        409: {"description": "L'apprenant est déjà inscrit à cette session"},
        400: {"description": "Session complète"}
    }
)
def create_inscription(payload: InscriptionCreate, db: Session = Depends(get_db)):
    return InscriptionService.create_inscription(db, payload)

@router.get(
    "/",
    response_model=list[InscriptionRead],
    summary="Lister toutes les inscriptions",
    description="Retourne la liste de toutes les inscriptions aux sessions de formation.",
    responses={
        200: {"description": "Liste des inscriptions récupérée avec succès"}
    }
)
def list_inscriptions(db: Session = Depends(get_db)):
    return InscriptionService.get_all_inscriptions(db)

@router.get(
    "/sessions/{session_id}/apprenants/{apprenant_id}",
    response_model=InscriptionRead,
    summary="Récupérer une inscription",
    description="Retourne l'inscription d'un apprenant spécifique à une session donnée.",
    responses={
        200: {"description": "Inscription trouvée"},
        404: {"description": "Inscription introuvable"}
    }
)
def get_inscription(session_id: int, apprenant_id: int, db: Session = Depends(get_db)):
    return InscriptionService.get_inscription(db, session_id, apprenant_id)

@router.put(
    "/sessions/{session_id}/apprenants/{apprenant_id}",
    response_model=InscriptionRead,
    summary="Mettre à jour une inscription",
    description="Met à jour l'inscription d'un apprenant à une session donnée.",
    responses={
        200: {"description": "Inscription mise à jour avec succès"},
        404: {"description": "Inscription introuvable"},
        400: {"description": "Données invalides"}
    }
)
def update_inscription(
    session_id: int,
    apprenant_id: int,
    payload: InscriptionUpdate,
    db: Session = Depends(get_db)
):
    return InscriptionService.update_inscription(db, session_id, apprenant_id, payload)

@router.delete(
    "/sessions/{session_id}/apprenants/{apprenant_id}",
    status_code=204,
    summary="Supprimer une inscription",
    description="Désinscrit un apprenant d'une session donnée.",
    responses={
        204: {"description": "Inscription supprimée avec succès"},
        404: {"description": "Inscription introuvable"}
    }
)
def delete_inscription(session_id: int, apprenant_id: int, db: Session = Depends(get_db)):
    return InscriptionService.delete_inscription(db, session_id, apprenant_id)