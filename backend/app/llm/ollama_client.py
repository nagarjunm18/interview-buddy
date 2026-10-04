import json

from ollama import Client
from app.core.config import OLLAMA_HOST, OLLAMA_MODEL


class OllamaClient:
    def __init__(self):
        self.client = Client(host=OLLAMA_HOST)
        self.model = OLLAMA_MODEL

    def generate(self, prompt: str) -> str:
        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    def generate_structured(self, prompt: str, schema: dict) -> dict:
        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format=schema
        )

        return json.loads(response["message"]["content"])