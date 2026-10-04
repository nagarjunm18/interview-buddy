from app.llm.ollama_client import OllamaClient
from app.models.answer_evaluation import AnswerEvaluation


class AnswerEvaluationService:

    def __init__(self):
        self.llm = OllamaClient()

    def evaluate(
        self,
        question: str,
        answer: str
    ) -> AnswerEvaluation:

        prompt = f"""
You are evaluating a candidate's answer during a technical interview.

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Evaluate the answer objectively.

Consider:

1. Technical accuracy
2. Depth of understanding
3. Clarity
4. Important concepts that are missing
5. Strong points in the answer

Then decide what the interviewer should do next.

Allowed decisions:
- FOLLOW_UP
- CHALLENGE
- CLARIFY
- MOVE_ON

Use FOLLOW_UP when the answer is partially correct but needs deeper explanation.

Use CHALLENGE when the answer is confident but should be tested with a harder question or edge case.

Use CLARIFY when the answer is ambiguous or difficult to understand.

Use MOVE_ON when the answer adequately addresses the question.

Scores must be integers from 0 to 10.

Return only the structured evaluation.
"""

        schema = AnswerEvaluation.model_json_schema()

        result = self.llm.generate_structured(
            prompt=prompt,
            schema=schema
        )

        return AnswerEvaluation.model_validate(result)