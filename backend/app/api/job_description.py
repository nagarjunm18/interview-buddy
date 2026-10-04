from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import job_description_service
from app.models.job_description import JobDescription


router = APIRouter(
    prefix="/api/job-description",
    tags=["Job Description"]
)


@router.post("")
def create_job_description(
    job_description: JobDescription,
    db: Session = Depends(get_db)
):

    job_id, saved_job = (
        job_description_service.create_job_description(
            db,
            job_description
        )
    )

    return {
        "job_description_id": job_id,
        "job_description": saved_job
    }


@router.get("/{job_description_id}")
def get_job_description(
    job_description_id: str,
    db: Session = Depends(get_db)
):

    job = job_description_service.get_job_description(
        db,
        job_description_id
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job description not found"
        )

    return {
        "job_description_id": job_description_id,
        "job_description": job
    }