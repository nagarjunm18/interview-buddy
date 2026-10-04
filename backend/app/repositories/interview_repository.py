from sqlalchemy.orm import Session

from app.db.interview import InterviewSessionDB
from app.models.interview_session import (
    InterviewSession,
    InterviewTurn
)
from app.models.interview_context import InterviewContext
from app.models.candidate import CandidateProfile
from app.models.job_description import JobDescription
from app.models.weakness import Weakness


class InterviewRepository:

    def create(
        self,
        db: Session,
        session: InterviewSession
    ) -> InterviewSession:

        db_session = InterviewSessionDB(
            session_id=session.session_id,
            candidate_id=session.context.candidate.candidate_id,
            job_description_id=self._job_description_id(session),
            status=session.status,
            context=session.context.model_dump(),
            turns=[
                turn.model_dump()
                for turn in session.turns
            ],
            weaknesses=[
                weakness.model_dump()
                for weakness in session.context.weaknesses
            ]
        )

        db.add(db_session)
        db.commit()
        db.refresh(db_session)

        return self._to_model(db_session)

    def get(
        self,
        db: Session,
        session_id: str
    ) -> InterviewSession | None:

        db_session = (
            db.query(InterviewSessionDB)
            .filter(
                InterviewSessionDB.session_id == session_id
            )
            .first()
        )

        if db_session is None:
            return None

        return self._to_model(db_session)

    def update(
        self,
        db: Session,
        session: InterviewSession
    ) -> InterviewSession:

        db_session = (
            db.query(InterviewSessionDB)
            .filter(
                InterviewSessionDB.session_id == session.session_id
            )
            .first()
        )

        if db_session is None:
            raise ValueError(
                "Interview session not found"
            )

        db_session.status = session.status

        db_session.context = (
            session.context.model_dump()
        )

        db_session.turns = [
            turn.model_dump()
            for turn in session.turns
        ]

        db_session.weaknesses = [
            weakness.model_dump()
            for weakness in session.context.weaknesses
        ]

        db.commit()
        db.refresh(db_session)

        return self._to_model(db_session)

    def _job_description_id(
        self,
        session: InterviewSession
    ) -> str:

        return getattr(
            session.context,
            "job_description_id",
            "unknown"
        )

    def _to_model(
        self,
        db_session: InterviewSessionDB
    ) -> InterviewSession:

        candidate_data = db_session.context["candidate"]
        job_data = db_session.context["job_description"]

        candidate = CandidateProfile(
            **candidate_data
        )

        job_description = JobDescription(
            **job_data
        )

        weaknesses = [
            Weakness(**weakness)
            for weakness in db_session.weaknesses
        ]

        context_data = db_session.context.copy()

        context_data["candidate"] = candidate
        context_data["job_description"] = job_description
        context_data["weaknesses"] = weaknesses

        context = InterviewContext(
            **context_data
        )

        turns = [
            InterviewTurn(**turn)
            for turn in db_session.turns
        ]

        return InterviewSession(
            session_id=db_session.session_id,
            context=context,
            turns=turns,
            status=db_session.status
        )