from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.formations import FormationCreate, FormationUpdate, FormationRead
from app.services.formation_service import FormationService

router = APIRouter(prefix="/trainings", tags=["Trainings"])

@router.post(
    "/",
    response_model=FormationRead,
    status_code=201,
    summary="Create a training program",
    description="Creates a new training program in the database with its title and description.",
    responses={
        201: {"description": "Training program created successfully"},
        400: {"description": "Invalid data"},
        409: {"description": "A training program with this title already exists"},
    },
)
def create_formation(payload: FormationCreate, db: Session = Depends(get_db)):
    return FormationService.create_formation(db, payload)

@router.get(
    "/",
    response_model=list[FormationRead],
    summary="List all training programs",
    description="Returns the list of all available training programs stored in the database.",
    responses={200: {"description": "Training program list retrieved successfully"}},
)
def list_formations(db: Session = Depends(get_db)):
    return FormationService.get_all_formations(db)

@router.get(
    "/{formation_id}",
    response_model=FormationRead,
    summary="Get a training program",
    description="Returns a specific training program by its identifier.",
    responses={
        200: {"description": "Training program found"},
        404: {"description": "Training program not found"},
    },
)
def get_formation(formation_id: int, db: Session = Depends(get_db)):
    return FormationService.get_formation_by_id(db, formation_id)

@router.put(
    "/{formation_id}",
    response_model=FormationRead,
    summary="Update a training program",
    description="Updates an existing training program using its identifier.",
    responses={
        200: {"description": "Training program updated successfully"},
        404: {"description": "Training program not found"},
        400: {"description": "Invalid data"},
    },
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
    summary="Delete a training program",
    description="Deletes an existing training program from the database using its identifier.",
    responses={
        204: {"description": "Training program deleted successfully"},
        404: {"description": "Training program not found"},
    },
)
def delete_formation(formation_id: int, db: Session = Depends(get_db)):
    return FormationService.delete_formation(db, formation_id)

@router.patch(
    "/{formation_id}",
    response_model=FormationRead,
    summary="Partially update a training program",
    description="Updates one or more fields of an existing training program.",
    responses={
        200: {"description": "Training program updated successfully"},
        404: {"description": "Training program not found"},
        400: {"description": "No fields provided for update"},
    },
)
def patch_formation(
    formation_id: int,
    payload: FormationUpdate,
    db: Session = Depends(get_db)
):
    return FormationService.patch_formation(db, formation_id, payload)