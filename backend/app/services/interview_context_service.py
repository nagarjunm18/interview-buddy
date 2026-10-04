from app.models.interview_context import InterviewContext
from app.models.candidate import CandidateProfile
from app.models.job_description import JobDescription


class InterviewContextService:

    def build_context(
        self,
        candidate: CandidateProfile,
        job_description: JobDescription,
        job_description_id: str | None = None
    ) -> InterviewContext:

        return InterviewContext(
            candidate=candidate,
            job_description=job_description,
            job_description_id=job_description_id
        )