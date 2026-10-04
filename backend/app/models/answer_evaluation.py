from pydantic import BaseModel, Field


class AnswerEvaluation(BaseModel):
    technical_accuracy: int = Field(ge=0, le=10)
    depth: int = Field(ge=0, le=10)
    clarity: int = Field(ge=0, le=10)

    strengths: list[str] = Field(default_factory=list)
    missing_concepts: list[str] = Field(default_factory=list)

    decision: str
    reason: str