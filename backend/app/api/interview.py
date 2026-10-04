from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    candidate_service,
    job_description_service,
    interview_context_service,
    interview_service,
    answer_evaluation_service,
    interview_session_service,
    weakness_service,
    interview_report_service,
    question_reason_service
)

from app.models.answer_submission import AnswerSubmission
from app.models.interview_session import InterviewTurn


router = APIRouter(
    prefix="/api/interview",
    tags=["Interview"]
)


# ============================================================
# CREATE INTERVIEW SESSION
# ============================================================

@router.post("/session")
def create_interview_session(
    candidate_id: str,
    job_description_id: str,
    db: Session = Depends(get_db)
):

    candidate = candidate_service.get_candidate(
        db,
        candidate_id
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found"
        )

    job_description = (
        job_description_service.get_job_description(
            db,
            job_description_id
        )
    )

    if job_description is None:
        raise HTTPException(
            status_code=404,
            detail="Job description not found"
        )

    # Build interview context
    context = interview_context_service.build_context(
        candidate=candidate,
        job_description=job_description,
        job_description_id=job_description_id
    )

    # --------------------------------------------------------
    # Load persistent weaknesses from PostgreSQL
    # --------------------------------------------------------

    context.weaknesses = (
        weakness_service.get_top_weaknesses(
            db=db,
            candidate_id=candidate.candidate_id
        )
    )

    # --------------------------------------------------------
    # Index candidate context for RAG
    # --------------------------------------------------------

    interview_service.index_candidate_context(
        context
    )

    # --------------------------------------------------------
    # Generate first interview question
    # --------------------------------------------------------

    question = interview_service.generate_question(
        context
    )

    context.current_question = question

    context.previous_questions.append(
        question
    )

    # --------------------------------------------------------
    # Create persistent interview session
    # --------------------------------------------------------

    session = interview_session_service.create_session(
        db,
        context
    )

    # Add first question as a turn
    session.turns.append(
        InterviewTurn(
            question=question
        )
    )

    session = interview_session_service.update_session(
        db,
        session
    )

    return {
        "session_id": session.session_id,
        "question": question
    }


# ============================================================
# GET INTERVIEW SESSION
# ============================================================

@router.get("/session/{session_id}")
def get_interview_session(
    session_id: str,
    db: Session = Depends(get_db)
):

    session = interview_session_service.get_session(
        db,
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    return session


# ============================================================
# SUBMIT ANSWER
# ============================================================

@router.post("/session/{session_id}/answer")
def submit_answer(
    session_id: str,
    submission: AnswerSubmission,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Load interview session
    # --------------------------------------------------------

    session = interview_session_service.get_session(
        db,
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    if not session.turns:
        raise HTTPException(
            status_code=400,
            detail="Interview session has no questions"
        )

    # --------------------------------------------------------
    # Get current question
    # --------------------------------------------------------

    current_turn = session.turns[-1]

    # --------------------------------------------------------
    # Evaluate candidate answer
    # --------------------------------------------------------

    evaluation = answer_evaluation_service.evaluate(
        question=current_turn.question,
        answer=submission.answer
    )

    # Store answer
    current_turn.answer = submission.answer

    # Store evaluation
    current_turn.evaluation = (
        evaluation.model_dump()
    )

    # Store answer in interview context
    session.context.previous_answers.append(
        submission.answer
    )

    # ========================================================
    # PERSIST WEAKNESSES TO POSTGRESQL
    # ========================================================

    for concept in evaluation.missing_concepts:

        weakness_service.record_weakness(
            db=db,
            candidate_id=(
                session.context.candidate.candidate_id
            ),
            topic=concept,
            reason=evaluation.reason,
            severity=max(
                0,
                10 - evaluation.depth
            )
        )

    # --------------------------------------------------------
    # Reload updated weaknesses from PostgreSQL
    # --------------------------------------------------------

    session.context.weaknesses = (
        weakness_service.get_top_weaknesses(
            db=db,
            candidate_id=(
                session.context.candidate.candidate_id
            )
        )
    )

    # ========================================================
    # GENERATE NEXT QUESTION
    # ========================================================

    if evaluation.decision == "MOVE_ON":

        next_question = (
            interview_service.generate_question(
                session.context
            )
        )

    else:

        next_question = (
            interview_service.generate_follow_up(
                context=session.context,
                question=current_turn.question,
                answer=submission.answer,
                evaluation=evaluation
            )
        )

    # --------------------------------------------------------
    # Update interview context
    # --------------------------------------------------------

    session.context.current_question = next_question

    session.context.previous_questions.append(
        next_question
    )

    # --------------------------------------------------------
    # Add next question as a new turn
    # --------------------------------------------------------

    session.turns.append(
        InterviewTurn(
            question=next_question
        )
    )

    # --------------------------------------------------------
    # Persist updated interview session
    # --------------------------------------------------------

    interview_session_service.update_session(
        db,
        session
    )

    return {
        "evaluation": evaluation,
        "next_question": next_question
    }


# ============================================================
# INTERVIEW REPORT
# ============================================================

@router.get("/session/{session_id}/report")
def get_interview_report(
    session_id: str,
    db: Session = Depends(get_db)
):

    session = interview_session_service.get_session(
        db,
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    report = interview_report_service.generate_report(
        session
    )

    return report


# ============================================================
# QUESTION REASON
# ============================================================

@router.post("/session/{session_id}/question-reason")
def get_question_reason(
    session_id: str,
    db: Session = Depends(get_db)
):

    session = interview_session_service.get_session(
        db,
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    if not session.context.current_question:
        raise HTTPException(
            status_code=400,
            detail="No current question"
        )

    return question_reason_service.explain(
        context=session.context,
        question=session.context.current_question
    )


# ============================================================
# STANDALONE ANSWER EVALUATION
# ============================================================

@router.post("/evaluate")
def evaluate_answer(
    submission: AnswerSubmission
):

    return answer_evaluation_service.evaluate(
        question=submission.question,
        answer=submission.answer
    )