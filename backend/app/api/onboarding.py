from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.core.dependencies import (
    resume_parser_service,
    candidate_service,
    job_description_service
)
from app.models.candidate import CandidateProfile
from app.models.job_description import JobDescription


router = APIRouter(
    prefix="/api/onboarding",
    tags=["Onboarding"]
)


class ResumeParseRequest(BaseModel):
    resume_text: str = Field(min_length=20)


class ResumeParseResponse(BaseModel):
    candidate: CandidateProfile


class CreateProfileRequest(BaseModel):
    candidate_id: str
    name: str
    target_role: str
    experience_years: float = 0
    skills: list[str] = []
    projects: list[str] = []


class CreateJobRequest(BaseModel):
    company: str = "Target Company"
    role: str
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    responsibilities: list[str] = []


@router.post("/parse-resume", response_model=ResumeParseResponse)
def parse_resume(request: ResumeParseRequest):

    try:
        candidate = resume_parser_service.parse(
            request.resume_text
        )

        candidate.candidate_id = (
            "candidate-" + str(uuid.uuid4())[:8]
        )

        return {
            "candidate": candidate
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Resume parsing failed: {str(e)}"
        )


@router.post("/candidate")
def create_candidate(
    request: CreateProfileRequest,
    db: Session = Depends(get_db)
):

    candidate = CandidateProfile(
        candidate_id=request.candidate_id,
        name=request.name,
        target_role=request.target_role,
        experience_years=request.experience_years,
        skills=request.skills,
        projects=request.projects
    )

    try:
        created = candidate_service.create_candidate(
            db,
            candidate
        )

        return created.model_dump()

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/job-description")
def create_job_description(
    request: CreateJobRequest,
    db: Session = Depends(get_db)
):

    job = JobDescription(
        company=request.company,
        role=request.role,
        required_skills=request.required_skills,
        preferred_skills=request.preferred_skills,
        responsibilities=request.responsibilities
    )

    try:
        job_id, created = job_description_service.create_job_description(
            db,
            job
        )

        return {
            "job_description_id": job_id,
            "job_description": created.model_dump()
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )