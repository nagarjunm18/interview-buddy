import uuid

from sqlalchemy.orm import Session

from app.models.interview_session import (
    InterviewSession,
    InterviewTurn
)
from app.models.interview_context import InterviewContext
from app.repositories.interview_repository import (
    InterviewRepository
)


class InterviewSessionService:

    def __init__(self):
        self.repository = InterviewRepository()

    def create_session(
        self,
        db: Session,
        context: InterviewContext
    ) -> InterviewSession:

        session_id = str(uuid.uuid4())

        session = InterviewSession(
            session_id=session_id,
            context=context
        )

        return self.repository.create(
            db,
            session
        )

    def get_session(
        self,
        db: Session,
        session_id: str
    ) -> InterviewSession | None:

        return self.repository.get(
            db,
            session_id
        )

    def update_session(
        self,
        db: Session,
        session: InterviewSession
    ) -> InterviewSession:

        return self.repository.update(
            db,
            session
        )

    def add_turn(
        self,
        db: Session,
        session_id: str,
        turn: InterviewTurn
    ) -> InterviewSession:

        session = self.get_session(
            db,
            session_id
        )

        if session is None:
            raise ValueError(
                "Interview session not found"
            )

        session.turns.append(turn)

        return self.update_session(
            db,
            session
        )