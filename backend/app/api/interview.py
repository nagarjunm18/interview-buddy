from fastapi import APIRouter
from pydantic import BaseModel

from app.services.interview_service import InterviewService


router = APIRouter(prefix="/api/interview", tags=["Interview"])

interview_service = InterviewService()


class InterviewRequest(BaseModel):
    role: str
    skills: list[str]


@router.post("/question")
def generate_question(request: InterviewRequest):
    question = interview_service.generate_question(
        role=request.role,
        skills=request.skills
    )

    return {
        "question": question
    }