from app.models.interview_report import InterviewReport
from app.models.interview_session import InterviewSession


class InterviewReportService:

    def generate_report(
        self,
        session: InterviewSession
    ) -> InterviewReport:

        evaluated_turns = [
            turn
            for turn in session.turns
            if turn.evaluation is not None
        ]

        if not evaluated_turns:
            return InterviewReport()

        evaluations = [
            turn.evaluation
            for turn in evaluated_turns
        ]

        technical_scores = [
            evaluation["technical_accuracy"]
            for evaluation in evaluations
        ]

        depth_scores = [
            evaluation["depth"]
            for evaluation in evaluations
        ]

        clarity_scores = [
            evaluation["clarity"]
            for evaluation in evaluations
        ]

        average_technical = (
            sum(technical_scores)
            / len(technical_scores)
        )

        average_depth = (
            sum(depth_scores)
            / len(depth_scores)
        )

        average_clarity = (
            sum(clarity_scores)
            / len(clarity_scores)
        )

        overall_score = (
            average_technical
            + average_depth
            + average_clarity
        ) / 3

        strengths = []

        for evaluation in evaluations:
            strengths.extend(
                evaluation.get("strengths", [])
            )

        missing_concepts = []

        for evaluation in evaluations:
            missing_concepts.extend(
                evaluation.get(
                    "missing_concepts",
                    []
                )
            )

        strengths = list(dict.fromkeys(strengths))
        missing_concepts = list(
            dict.fromkeys(missing_concepts)
        )

        recommendations = [
            f"Practice explaining {topic} with a concrete example."
            for topic in missing_concepts[:5]
        ]

        return InterviewReport(
            total_questions=len(evaluated_turns),

            average_technical_accuracy=round(
                average_technical,
                2
            ),

            average_depth=round(
                average_depth,
                2
            ),

            average_clarity=round(
                average_clarity,
                2
            ),

            overall_score=round(
                overall_score,
                2
            ),

            strengths=strengths[:10],

            weaknesses=missing_concepts[:10],

            recommendations=recommendations
        )