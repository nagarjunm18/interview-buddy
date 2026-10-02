from ollama import Client


class OllamaClient:
    def __init__(self, host: str = "http://localhost:11434"):
        self.client = Client(host=host)
        self.model = "qwen3:4b"

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