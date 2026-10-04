from sqlalchemy import Column, String, JSON

from app.core.database import Base


class JobDescriptionDB(Base):
    __tablename__ = "job_descriptions"

    id = Column(
        String,
        primary_key=True
    )

    company = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        nullable=False
    )

    required_skills = Column(
        JSON,
        default=list
    )

    preferred_skills = Column(
        JSON,
        default=list
    )

    responsibilities = Column(
        JSON,
        default=list
    )