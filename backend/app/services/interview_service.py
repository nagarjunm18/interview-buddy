from app.llm.ollama_client import OllamaClient
from app.models.interview_context import InterviewContext
from app.models.answer_evaluation import AnswerEvaluation
from app.services.rag_service import RAGService


class InterviewService:

    def __init__(self):
        self.llm = OllamaClient()
        self.rag = RAGService()

    def index_candidate_context(
        self,
        context: InterviewContext
    ) -> int:

        candidate = context.candidate
        job = context.job_description

        text = f"""
Candidate Profile

Name:
{candidate.name}

Target Role:
{candidate.target_role}

Experience:
{candidate.experience_years} years

Skills:
{", ".join(candidate.skills)}

Projects:
{", ".join(candidate.projects)}

Job Description

Company:
{job.company}

Role:
{job.role}

Required Skills:
{", ".join(job.required_skills)}

Preferred Skills:
{", ".join(job.preferred_skills)}

Responsibilities:
{" ".join(job.responsibilities)}
"""

        return self.rag.index_document(
            document_id=candidate.candidate_id,
            text=text,
            metadata={
                "candidate_id": candidate.candidate_id,
                "type": "candidate_context"
            }
        )

    def generate_question(
        self,
        context: InterviewContext
    ) -> str:

        candidate = context.candidate
        job = context.job_description

        skills = ", ".join(candidate.skills)

        projects = ", ".join(candidate.projects)

        required_skills = ", ".join(
            job.required_skills
        )

        preferred_skills = ", ".join(
            job.preferred_skills
        )

        responsibilities = "\n".join(
            f"- {item}"
            for item in job.responsibilities
        )

        previous_questions = "\n".join(
            f"- {question}"
            for question in context.previous_questions
        )

        weaknesses = "\n".join(
            f"- {weakness.topic} "
            f"(severity: {weakness.severity}/10, "
            f"occurrences: {weakness.occurrences})"
            for weakness in context.weaknesses
        )

        retrieval = self.rag.retrieve(
            query=f"""
Generate a technical interview question for
the candidate targeting the role {candidate.target_role}.

Focus on relevant skills, projects, job requirements,
and responsibilities.

IMPORTANT GROUNDING RULES:

Only ask questions about:
1. Technologies explicitly listed in the candidate profile.
2. Projects explicitly listed in the candidate profile.
3. Features explicitly described for those projects.
4. Skills and responsibilities explicitly present in the job description.
5. Concepts discussed earlier in the current interview.

Do NOT assume that a project contains a feature just because
that feature is common for that type of application.

For example, if the candidate's project does not mention
payment processing, do not ask about payment processing.

If a question would require an unsupported assumption,
choose a different question grounded in the provided context.

Before generating the question, verify that the topic is
supported by the retrieved context.

If it is not supported, choose another topic.
""",
            top_k=3,
            candidate_id=candidate.candidate_id
        )

        if retrieval["retrieval_success"]:

            retrieved_context = "\n\n".join(
                result["chunk"].text
                for result in retrieval["results"]
            )

        else:

            retrieved_context = (
                "No sufficiently relevant retrieved context."
            )

        prompt = f"""
You are conducting a realistic technical interview.

CANDIDATE

Name:
{candidate.name}

Target Role:
{candidate.target_role}

Experience:
{candidate.experience_years} years

Skills:
{skills}

Projects:
{projects}

JOB

Company:
{job.company}

Role:
{job.role}

Required Skills:
{required_skills}

Preferred Skills:
{preferred_skills}

Responsibilities:
{responsibilities}

PREVIOUS QUESTIONS:
{previous_questions}

KNOWN WEAKNESSES:
{weaknesses}

RETRIEVED CONTEXT:
{retrieved_context}

Generate ONE interview question.

Prioritize topics that:

1. Match the target role.
2. Match the job requirements.
3. Relate to the candidate's projects or skills.
4. Address known weaknesses when appropriate.
5. Have not already been asked.
6. Use the retrieved context when it is relevant.

Only ask about candidate experience, skills,
projects, or job requirements supported by the
provided context.

Do not invent candidate experience or projects.

Do not repeat a previous question.

Do not provide the answer.

Return only the interview question.
"""

        return self.llm.generate(prompt)

    def generate_follow_up(
        self,
        context: InterviewContext,
        question: str,
        answer: str,
        evaluation: AnswerEvaluation
    ) -> str:

        missing = ", ".join(
            evaluation.missing_concepts
        )

        prompt = f"""
You are conducting an adaptive technical interview.

Previous question:
{question}

Candidate answer:
{answer}

Evaluation:

Technical accuracy:
{evaluation.technical_accuracy}/10

Depth:
{evaluation.depth}/10

Clarity:
{evaluation.clarity}/10

Missing concepts:
{missing}

Decision:
{evaluation.decision}

Reason:
{evaluation.reason}

Generate ONE follow-up interview question.

The follow-up should specifically address
the weaknesses or missing concepts identified
in the evaluation.

Do not repeat the previous question.

Do not provide the answer.

Return only the question.
"""

        return self.llm.generate(prompt)