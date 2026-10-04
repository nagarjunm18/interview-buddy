from sqlalchemy.orm import Session

from app.db.candidate import CandidateDB
from app.models.candidate import CandidateProfile


class CandidateRepository:

    def create(
        self,
        db: Session,
        candidate: CandidateProfile
    ) -> CandidateProfile:

        db_candidate = CandidateDB(
            candidate_id=candidate.candidate_id,
            name=candidate.name,
            target_role=candidate.target_role,
            experience_years=candidate.experience_years,
            skills=candidate.skills,
            projects=candidate.projects
        )

        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)

        return self._to_model(db_candidate)

    def get(
        self,
        db: Session,
        candidate_id: str
    ) -> CandidateProfile | None:

        candidate = (
            db.query(CandidateDB)
            .filter(
                CandidateDB.candidate_id == candidate_id
            )
            .first()
        )

        if candidate is None:
            return None

        return self._to_model(candidate)

    def _to_model(
        self,
        candidate: CandidateDB
    ) -> CandidateProfile:

        return CandidateProfile(
            candidate_id=candidate.candidate_id,
            name=candidate.name,
            target_role=candidate.target_role,
            experience_years=candidate.experience_years,
            skills=candidate.skills or [],
            projects=candidate.projects or []
        )