from pydantic import BaseModel, Field


class QuestionReason(BaseModel):
    reasons: list[str] = Field(
        default_factory=list
    )