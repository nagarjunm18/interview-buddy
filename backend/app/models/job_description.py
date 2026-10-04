from pydantic import BaseModel, Field


class JobDescription(BaseModel):
    company: str
    role: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)