from app.core.database import Base, engine

from app.db.candidate import CandidateDB
from app.db.job_description import JobDescriptionDB
from app.db.interview import InterviewSessionDB
from app.db.weakness import CandidateWeaknessDB


def init_db():
    Base.metadata.create_all(bind=engine)