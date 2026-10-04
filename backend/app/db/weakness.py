from sqlalchemy import Column, Integer, String, UniqueConstraint

from app.core.database import Base


class CandidateWeaknessDB(Base):
    __tablename__ = "candidate_weaknesses"

    id = Column(Integer, primary_key=True, autoincrement=True)

    candidate_id = Column(
        String,
        nullable=False,
        index=True
    )

    topic = Column(
        String,
        nullable=False
    )

    occurrences = Column(
        Integer,
        nullable=False,
        default=1
    )

    last_reason = Column(
        String,
        nullable=False
    )

    severity = Column(
        Integer,
        nullable=False,
        default=5
    )

    __table_args__ = (
        UniqueConstraint(
            "candidate_id",
            "topic",
            name="uq_candidate_weakness_topic"
        ),
    )