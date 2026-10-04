import os

from dotenv import load_dotenv


load_dotenv()


OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:4b"
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured in .env"
    )

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured in .env"
    )