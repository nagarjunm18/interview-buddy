from pydantic import BaseModel, Field


class InterviewReport(BaseModel):
    total_questions: int = 0

    average_technical_accuracy: float = 0
    average_depth: float = 0
    average_clarity: float = 0

    overall_score: float = 0

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    recommendations: list[str] = Field(
        default_factory=list
    )