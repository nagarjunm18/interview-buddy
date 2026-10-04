import uuid

from sqlalchemy.orm import Session

from app.db.job_description import JobDescriptionDB
from app.models.job_description import JobDescription


class JobDescriptionRepository:

    def create(
        self,
        db: Session,
        job_description: JobDescription
    ) -> tuple[str, JobDescription]:

        job_description_id = str(uuid.uuid4())

        db_job = JobDescriptionDB(
            id=job_description_id,
            company=job_description.company,
            role=job_description.role,
            required_skills=job_description.required_skills,
            preferred_skills=job_description.preferred_skills,
            responsibilities=job_description.responsibilities
        )

        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        return job_description_id, self._to_model(db_job)

    def get(
        self,
        db: Session,
        job_description_id: str
    ) -> JobDescription | None:

        job = (
            db.query(JobDescriptionDB)
            .filter(
                JobDescriptionDB.id == job_description_id
            )
            .first()
        )

        if job is None:
            return None

        return self._to_model(job)

    def _to_model(
        self,
        job: JobDescriptionDB
    ) -> JobDescription:

        return JobDescription(
            company=job.company,
            role=job.role,
            required_skills=job.required_skills or [],
            preferred_skills=job.preferred_skills or [],
            responsibilities=job.responsibilities or []
        )