from sqlalchemy.orm import Session

from app.models.job_description import JobDescription
from app.repositories.job_description_repository import (
    JobDescriptionRepository
)


class JobDescriptionService:

    def __init__(self):
        self.repository = JobDescriptionRepository()

    def create_job_description(
        self,
        db: Session,
        job_description: JobDescription
    ) -> tuple[str, JobDescription]:

        return self.repository.create(
            db,
            job_description
        )

    def get_job_description(
        self,
        db: Session,
        job_description_id: str
    ) -> JobDescription | None:

        return self.repository.get(
            db,
            job_description_id
        )