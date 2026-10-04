from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    candidate_service,
    weakness_service
)

router = APIRouter(
    prefix="/api/weaknesses",
    tags=["Weaknesses"]
)


@router.get("")
def get_weaknesses(
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

    weaknesses = weakness_service.get_top_weaknesses(
        db=db,
        candidate_id=candidate.candidate_id
    )

    return {
        "candidate_id": candidate.candidate_id,
        "weaknesses": weaknesses
    }