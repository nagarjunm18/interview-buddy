from app.llm.ollama_client import OllamaClient


class InterviewService:
    def __init__(self):
        self.llm = OllamaClient()

    def generate_question(self, role: str, skills: list[str]) -> str:
        skills_text = ", ".join(skills)

        prompt = f"""
You are an AI technical interviewer.

Target role: {role}
Candidate skills: {skills_text}

Generate ONE realistic technical interview question
appropriate for this candidate.

Do not provide the answer.
Return only the interview question.
"""

        return self.llm.generate(prompt)