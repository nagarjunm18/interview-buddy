import re

from app.llm.ollama_client import OllamaClient
from app.models.candidate import CandidateProfile


class ResumeParserService:

    def __init__(self):
        self.llm = OllamaClient()

    def parse(self, resume_text: str) -> CandidateProfile:

        prompt = f"""
You are a resume parser.

Extract a structured candidate profile from the resume below.

RESUME:
{resume_text}

Rules:

1. Extract the candidate's name.
2. Extract technical skills explicitly mentioned.
3. Extract projects explicitly mentioned.
4. Extract years of experience if clearly stated.
5. If experience is not stated, use 0.
6. Do not invent skills.
7. Do not invent projects.
8. Do not infer technologies that are not explicitly mentioned.
9. The target role will be supplied separately, so do not guess it.

Return only structured data matching this schema:

{{
    "candidate_id": "default",
    "name": "Candidate Name",
    "target_role": "Software Engineer",
    "experience_years": 0,
    "skills": [],
    "projects": []
}}
"""

        schema = CandidateProfile.model_json_schema()

        result = self.llm.generate_structured(
            prompt=prompt,
            schema=schema
        )

        return CandidateProfile.model_validate(result)