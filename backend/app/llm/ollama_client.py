import json

from groq import Groq

from app.core.config import GROQ_API_KEY, GROQ_MODEL


class OllamaClient:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    def generate_structured(
        self,
        prompt: str,
        schema: dict
    ) -> dict:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_response",
                    "strict": False,
                    "schema": schema
                }
            }
        )

        return json.loads(
            response.choices[0].message.content
        )