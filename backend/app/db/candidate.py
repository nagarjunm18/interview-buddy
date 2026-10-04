from sqlalchemy import Column, String, Float, JSON

from app.core.database import Base


class CandidateDB(Base):
    __tablename__ = "candidates"

    candidate_id = Column(
        String,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    target_role = Column(
        String,
        nullable=False
    )

    experience_years = Column(
        Float,
        default=0
    )

    skills = Column(
        JSON,
        default=list
    )

    projects = Column(
        JSON,
        default=list
    )