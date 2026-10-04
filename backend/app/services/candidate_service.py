from sqlalchemy.orm import Session

from app.models.candidate import CandidateProfile
from app.repositories.candidate_repository import CandidateRepository


class CandidateService:

    def __init__(self):
        self.repository = CandidateRepository()

    def create_candidate(
        self,
        db: Session,
        candidate: CandidateProfile
    ) -> CandidateProfile:

        existing = self.repository.get(
            db,
            candidate.candidate_id
        )

        if existing is not None:
            raise ValueError(
                "Candidate with this ID already exists"
            )

        return self.repository.create(
            db,
            candidate
        )

    def get_candidate(
        self,
        db: Session,
        candidate_id: str
    ) -> CandidateProfile | None:

        return self.repository.get(
            db,
            candidate_id
        )