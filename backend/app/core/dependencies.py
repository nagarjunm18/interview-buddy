from app.services.candidate_service import CandidateService
from app.services.interview_service import InterviewService
from app.services.job_description_service import JobDescriptionService
from app.services.interview_context_service import InterviewContextService
from app.services.answer_evaluation_service import AnswerEvaluationService
from app.services.interview_session_service import InterviewSessionService
from app.services.weakness_service import WeaknessService
from app.services.interview_report_service import InterviewReportService
from app.services.question_reason_service import QuestionReasonService
from app.services.resume_parser_service import ResumeParserService


weakness_service = WeaknessService()
interview_session_service = InterviewSessionService()
question_reason_service = QuestionReasonService()
interview_report_service = InterviewReportService()
answer_evaluation_service = AnswerEvaluationService()
resume_parser_service = ResumeParserService()
interview_context_service = InterviewContextService()


candidate_service = CandidateService()
job_description_service = JobDescriptionService()
interview_service = InterviewService()