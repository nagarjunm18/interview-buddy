from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    candidate_id: str = Field(default="default")
    name: str
    target_role: str
    experience_years: float = Field(default=0)
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)