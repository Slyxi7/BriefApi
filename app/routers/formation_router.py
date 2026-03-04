from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.formations import FormationCreate, FormationUpdate, FormationRead
from app.services.formation_service import FormationService

router = APIRouter(prefix="/formations", tags=["Formations"])

@router.post(
    "/",
    response_model=FormationRead,
    status_code=201,
    summary="Créer une formation",
    description="Crée une nouvelle formation dans la base de données avec son titre et sa description.",
    responses={
        201: {"description": "Formation créée avec succès"},
        400: {"description": "Données invalides"},
        409: {"description": "Une formation avec ce titre existe déjà"}
    }
)
def create_formation(payload: FormationCreate, db: Session = Depends(get_db)):
    return FormationService.create_formation(db, payload)

@router.get(
    "/",
    response_model=list[FormationRead],
    summary="Lister toutes les formations",
    description="Retourne la liste de toutes les formations disponibles dans la base de données.",
    responses={
        200: {"description": "Liste des formations récupérée avec succès"}
    }
)
def list_formations(db: Session = Depends(get_db)):
    return FormationService.get_all_formations(db)

@router.get(
    "/{formation_id}",
    response_model=FormationRead,
    summary="Récupérer une formation",
    description="Retourne les informations d'une formation spécifique à partir de son identifiant.",
    responses={
        200: {"description": "Formation trouvée"},
        404: {"description": "Formation introuvable"}
    }
)
def get_formation(formation_id: int, db: Session = Depends(get_db)):
    return FormationService.get_formation_by_id(db, formation_id)

@router.put(
    "/{formation_id}",
    response_model=FormationRead,
    summary="Mettre à jour une formation",
    description="Met à jour les informations d'une formation existante à partir de son identifiant.",
    responses={
        200: {"description": "Formation mise à jour avec succès"},
        404: {"description": "Formation introuvable"},
        400: {"description": "Données invalides"}
    }
)
def update_formation(
    formation_id: int,
    payload: FormationUpdate,
    db: Session = Depends(get_db)
):
    return FormationService.update_formation(db, formation_id, payload)

@router.delete(
    "/{formation_id}",
    status_code=204,
    summary="Supprimer une formation",
    description="Supprime une formation existante de la base de données à partir de son identifiant.",
    responses={
        204: {"description": "Formation supprimée avec succès"},
        404: {"description": "Formation introuvable"}
    }
)
def delete_formation(formation_id: int, db: Session = Depends(get_db)):
    return FormationService.delete_formation(db, formation_id)

@router.patch(
    "/{formation_id}",
    response_model=FormationRead,
    summary="Mettre à jour partiellement une formation",
    description="Met à jour un ou plusieurs champs d'une formation existante.",
    responses={
        200: {"description": "Formation mise à jour avec succès"},
        404: {"description": "Formation introuvable"},
        400: {"description": "Aucun champ fourni pour la mise à jour"}
    }
)
def patch_formation(
    formation_id: int,
    payload: FormationUpdate,
    db: Session = Depends(get_db)
):
    return FormationService.patch_formation(db, formation_id, payload)