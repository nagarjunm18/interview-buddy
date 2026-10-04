from pydantic import BaseModel, Field


class Weakness(BaseModel):
    topic: str
    occurrences: int = 1
    last_reason: str
    severity: int = Field(default=5, ge=0, le=10)