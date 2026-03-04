from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.database.connection import get_db
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.services.user_service import UserService
from app.services.inscription_service import InscriptionService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    "/",
    response_model=UserRead,
    status_code=201,
    summary="Créer un utilisateur",
    description="Crée un nouvel utilisateur dans la base de données avec son nom, prénom, email et rôle.",
    responses={
        201: {"description": "Utilisateur créé avec succès"},
        400: {"description": "Requête invalide"},
        409: {"description": "Email déjà utilisé"}
    }
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, payload)

@router.get(
    "/",
    response_model=list[UserRead],
    summary="Lister tous les utilisateurs",
    description="Retourne la liste de tous les utilisateurs enregistrés dans la base de données.",
    responses={
        200: {"description": "Liste des utilisateurs récupérée avec succès"}
    }
)
def list_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)

@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Récupérer un utilisateur",
    description="Retourne les informations d'un utilisateur spécifique à partir de son identifiant.",
    responses={
        200: {"description": "Utilisateur trouvé"},
        404: {"description": "Utilisateur non trouvé"}
    }
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(db, user_id)

@router.put(
    "/{user_id}",
    response_model=UserRead,
    summary="Mettre à jour un utilisateur",
    description="Met à jour les informations d'un utilisateur existant à partir de son identifiant.",
    responses={
        200: {"description": "Utilisateur mis à jour avec succès"},
        404: {"description": "Utilisateur non trouvé"},
        400: {"description": "Données invalides"}
    }
)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(db, user_id, payload)

@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Supprimer un utilisateur",
    description="Soft delete par défaut. Ajouter ?hard=true pour supprimer définitivement.",
    responses={
        204: {"description": "Utilisateur supprimé avec succès"},
        404: {"description": "Utilisateur non trouvé"}
    }
)
def delete_user(user_id: int, hard: bool = False, db: Session = Depends(get_db)):
    result = UserService.delete(db, user_id, hard)

    if result is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return

@router.get(
    "/{user_id}/inscriptions",
    summary="Lister les inscriptions d'un utilisateur",
    description="Retourne toutes les inscriptions aux sessions pour un utilisateur donné.",
    responses={
        200: {"description": "Liste des inscriptions récupérée avec succès"},
        404: {"description": "Utilisateur non trouvé"}
    }
)
def get_user_inscriptions(user_id: int, db: Session = Depends(get_db)):
    return InscriptionService.get_inscription_user(db, user_id)

@router.patch(
    "/{user_id}",
    response_model=UserRead,
    summary="Mettre à jour partiellement un utilisateur",
    description="Met à jour un ou plusieurs champs d'un utilisateur (nom, prénom, email, rôle).",
    responses={
        200: {"description": "Utilisateur mis à jour avec succès"},
        404: {"description": "Utilisateur non trouvé"},
        409: {"description": "Email déjà utilisé"},
        400: {"description": "Aucun champ fourni pour la mise à jour"},
    },
)
def patch_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return UserService.patch_user(db, user_id, payload)