from pydantic import BaseModel, Field

from app.models.candidate import CandidateProfile
from app.models.job_description import JobDescription
from app.models.weakness import Weakness


class InterviewContext(BaseModel):

    candidate: CandidateProfile

    job_description: JobDescription

    job_description_id: str | None = None

    current_question: str | None = None

    previous_questions: list[str] = Field(
        default_factory=list
    )

    previous_answers: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[Weakness] = Field(
        default_factory=list
    )