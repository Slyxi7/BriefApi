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
    summary="Create a user",
    description="Creates a new user in the database with their first name, last name, email, and role.",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid request"},
        409: {"description": "Email already in use"}
    }
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, payload)

@router.get(
    "/",
    response_model=list[UserRead],
    summary="List all users",
    description="Returns the list of all users stored in the database.",
    responses={
        200: {"description": "User list retrieved successfully"}
    }
)
def list_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)

@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get a user",
    description="Returns the information of a specific user using their identifier.",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    }
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(db, user_id)

@router.put(
    "/{user_id}",
    response_model=UserRead,
    summary="Update a user",
    description="Updates the information of an existing user using their identifier.",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"},
        400: {"description": "Invalid data"}
    }
)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return UserService.update_user(db, user_id, payload)

@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Delete a user",
    description="Soft delete by default. Add ?hard=true to permanently delete the user.",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"}
    }
)
def delete_user(user_id: int, hard: bool = False, db: Session = Depends(get_db)):
    result = UserService.delete(db, user_id, hard)

    if result is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return

@router.get(
    "/{user_id}/inscriptions",
    summary="List user enrollments",
    description="Returns all session enrollments for a given user.",
    responses={
        200: {"description": "Enrollment list retrieved successfully"},
        404: {"description": "User not found"}
    }
)
def get_user_inscriptions(user_id: int, db: Session = Depends(get_db)):
    return InscriptionService.get_inscription_user(db, user_id)

@router.patch(
    "/{user_id}",
    response_model=UserRead,
    summary="Partially update a user",
    description="Updates one or more fields of a user (first name, last name, email, role).",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"},
        409: {"description": "Email already in use"},
        400: {"description": "No fields provided for update"},
    },
)
def patch_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return UserService.patch_user(db, user_id, payload)