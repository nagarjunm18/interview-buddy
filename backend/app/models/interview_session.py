from pydantic import BaseModel, Field

from app.models.interview_context import InterviewContext


class InterviewTurn(BaseModel):
    question: str
    answer: str | None = None
    evaluation: dict | None = None


class InterviewSession(BaseModel):
    session_id: str
    context: InterviewContext
    turns: list[InterviewTurn] = Field(default_factory=list)
    status: str = "active"