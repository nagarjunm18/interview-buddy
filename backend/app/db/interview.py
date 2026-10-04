from sqlalchemy import Column, String, JSON

from app.core.database import Base


class InterviewSessionDB(Base):
    __tablename__ = "interview_sessions"

    session_id = Column(
        String,
        primary_key=True
    )

    candidate_id = Column(
        String,
        nullable=False
    )

    job_description_id = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="active",
        nullable=False
    )

    context = Column(
        JSON,
        nullable=False
    )

    turns = Column(
        JSON,
        default=list,
        nullable=False
    )

    weaknesses = Column(
        JSON,
        default=list,
        nullable=False
    )