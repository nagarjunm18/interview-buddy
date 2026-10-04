from app.models.interview_context import InterviewContext
from app.models.question_reason import QuestionReason


class QuestionReasonService:

    def explain(
        self,
        context: InterviewContext,
        question: str
    ) -> QuestionReason:

        reasons = []

        candidate = context.candidate
        job = context.job_description

        question_lower = question.lower()

        # Candidate project relevance
        for project in candidate.projects:

            project_keywords = project.lower().split()

            if any(
                keyword in question_lower
                for keyword in project_keywords
                if len(keyword) > 3
            ):
                reasons.append(
                    f"The question relates to your project: {project}."
                )
                break

        # Skill relevance
        for skill in candidate.skills:

            if skill.lower() in question_lower:

                reasons.append(
                    f"The question relates to your skill: {skill}."
                )

        # Required JD skill relevance
        for skill in job.required_skills:

            if skill.lower() in question_lower:

                reasons.append(
                    f"{skill} is a required skill for the target role."
                )

        # Preferred JD skill relevance
        for skill in job.preferred_skills:

            if skill.lower() in question_lower:

                reasons.append(
                    f"{skill} is listed as a preferred skill for the role."
                )

        # Weakness relevance
        for weakness in context.weaknesses:

            if weakness.topic.lower() in question_lower:

                reasons.append(
                    f"You previously showed a weakness in {weakness.topic}."
                )

        if not reasons:

            reasons.append(
                "The question was selected based on your target role, "
                "candidate profile, and interview context."
            )

        return QuestionReason(
            reasons=list(dict.fromkeys(reasons))
        )