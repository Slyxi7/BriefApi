from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.inscription import InscriptionCreate, InscriptionUpdate, InscriptionRead
from app.services.inscription_service import InscriptionService

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post(
    "/",
    response_model=InscriptionRead,
    status_code=201,
    summary="Create an enrollment",
    description="Enrolls a learner in a training session.",
    responses={
        201: {"description": "Enrollment created successfully"},
        404: {"description": "Session or learner not found"},
        409: {"description": "The learner is already enrolled in this session"},
        400: {"description": "Session is full"}
    }
)
def create_inscription(payload: InscriptionCreate, db: Session = Depends(get_db)):
    return InscriptionService.create_inscription(db, payload)

@router.get(
    "/",
    response_model=list[InscriptionRead],
    summary="List all enrollments",
    description="Returns the list of all enrollments for training sessions.",
    responses={
        200: {"description": "Enrollment list retrieved successfully"}
    }
)
def list_inscriptions(db: Session = Depends(get_db)):
    return InscriptionService.get_all_inscriptions(db)

@router.delete(
    "/sessions/{session_id}/apprenants/{apprenant_id}",
    status_code=204,
    summary="Delete an enrollment",
    description="Unenrolls a learner from a given session.",
    responses={
        204: {"description": "Enrollment deleted successfully"},
        404: {"description": "Enrollment not found"}
    }
)
def delete_inscription(session_id: int, apprenant_id: int, db: Session = Depends(get_db)):
    return InscriptionService.delete_inscription(db, session_id, apprenant_id)