from sqlalchemy.orm import Session

from app.db.weakness import CandidateWeaknessDB
from app.models.weakness import Weakness


class WeaknessService:

    def record_weakness(
        self,
        db: Session,
        candidate_id: str,
        topic: str,
        reason: str,
        severity: int = 5
    ) -> Weakness:

        existing = (
            db.query(CandidateWeaknessDB)
            .filter(
                CandidateWeaknessDB.candidate_id == candidate_id,
                CandidateWeaknessDB.topic == topic
            )
            .first()
        )

        if existing is None:

            weakness = CandidateWeaknessDB(
                candidate_id=candidate_id,
                topic=topic,
                occurrences=1,
                last_reason=reason,
                severity=severity
            )

            db.add(weakness)
            db.commit()
            db.refresh(weakness)

        else:

            existing.occurrences += 1
            existing.last_reason = reason

            # Repeated weakness increases severity,
            # but never beyond 10.
            existing.severity = min(
                10,
                max(existing.severity, severity) + 1
            )

            db.commit()
            db.refresh(existing)

            weakness = existing

        return self._to_model(weakness)

    def get_weaknesses(
        self,
        db: Session,
        candidate_id: str
    ) -> list[Weakness]:

        weaknesses = (
            db.query(CandidateWeaknessDB)
            .filter(
                CandidateWeaknessDB.candidate_id == candidate_id
            )
            .all()
        )

        return [
            self._to_model(weakness)
            for weakness in weaknesses
        ]

    def get_top_weaknesses(
        self,
        db: Session,
        candidate_id: str,
        limit: int = 5
    ) -> list[Weakness]:

        weaknesses = (
            db.query(CandidateWeaknessDB)
            .filter(
                CandidateWeaknessDB.candidate_id == candidate_id
            )
            .order_by(
                CandidateWeaknessDB.severity.desc(),
                CandidateWeaknessDB.occurrences.desc()
            )
            .limit(limit)
            .all()
        )

        return [
            self._to_model(weakness)
            for weakness in weaknesses
        ]

    def clear_weaknesses(
        self,
        db: Session,
        candidate_id: str
    ) -> None:

        (
            db.query(CandidateWeaknessDB)
            .filter(
                CandidateWeaknessDB.candidate_id == candidate_id
            )
            .delete(
                synchronize_session=False
            )
        )

        db.commit()

    def _to_model(
        self,
        weakness: CandidateWeaknessDB
    ) -> Weakness:

        return Weakness(
            topic=weakness.topic,
            occurrences=weakness.occurrences,
            last_reason=weakness.last_reason,
            severity=weakness.severity
        )