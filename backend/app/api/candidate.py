from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import candidate_service
from app.models.candidate import CandidateProfile


router = APIRouter(
    prefix="/api/candidate",
    tags=["Candidate"]
)


@router.post("")
def create_candidate(
    candidate: CandidateProfile,
    db: Session = Depends(get_db)
):

    try:
        return candidate_service.create_candidate(
            db,
            candidate
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.get("/{candidate_id}")
def get_candidate(
    candidate_id: str,
    db: Session = Depends(get_db)
):

    candidate = candidate_service.get_candidate(
        db,
        candidate_id
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    return candidate