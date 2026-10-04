from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.interview import router as interview_router
from app.api.candidate import router as candidate_router
from app.api.job_description import router as job_description_router
from app.api.weakness import router as weakness_router
from app.api.onboarding import router as onboarding_router

from app.db.init_db import init_db

init_db()


app = FastAPI(
    title="InterviewBuddy API",
    description="AI-powered adaptive interview preparation platform",
    version="0.1.0"
)

app.include_router(onboarding_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://interview-buddy-1-quvm.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(interview_router)
app.include_router(candidate_router)
app.include_router(job_description_router)
app.include_router(weakness_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }