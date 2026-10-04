from app.services.answer_evaluation_service import AnswerEvaluationService


service = AnswerEvaluationService()


question = """
In your RentMate project, how did you design the REST API endpoints
to handle student rental requests?
"""

answer = """
I created REST API endpoints using Spring Boot. I used a POST endpoint
to create rental requests and connected it to MySQL. The controller
receives the request and the service layer handles the business logic.
"""


evaluation = service.evaluate(
    question=question,
    answer=answer
)

print("\nANSWER EVALUATION")
print("=================")
print(evaluation.model_dump_json(indent=2))