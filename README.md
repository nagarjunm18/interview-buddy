InterviewBuddy

AI-powered personalized mock interview platform that adapts questions based on a candidate's resume, target role, job description, and previous performance.

🚀 Live Demo

Frontend: InterviewBuddy
API Docs: Swagger API
Source Code: GitHub Repository

✨ Features
📄 Resume-based onboarding
🎯 Target-role personalization
💼 Optional Job Description support
🧠 RAG-based retrieval
🤖 AI-generated interview questions
📊 Structured answer evaluation
🔁 Adaptive follow-up questions
🧠 Persistent weakness tracking
📋 Interview performance report
🏗️ Architecture
Candidate
   │
   ▼
Resume / Job Description
   │
   ▼
Candidate Profile
   │
   ▼
Interview Engine
   ├── RAG Retrieval
   ├── LLM
   └── Memory
   │
   ▼
Answer Evaluation
   │
   ▼
PostgreSQL
🛠️ Tech Stack

Frontend

React
TypeScript
Vite

Backend

Python
FastAPI
SQLAlchemy
PostgreSQL

AI

Groq — gpt-oss-20b
Ollama — qwen3:4b for local development
TF-IDF retrieval
RAG
Structured LLM evaluation

Deployment

Render
🧠 How It Works
Candidate uploads a resume.
InterviewBuddy extracts the candidate profile.
Candidate selects a target role and optionally provides a JD.
Relevant information is retrieved using RAG.
The AI generates a personalized question.
The candidate submits an answer.
The answer is evaluated for:
Technical accuracy
Depth
Clarity
Missing concepts
Weak areas are stored and used to influence future questions.
🔍 Retrieval

InterviewBuddy uses a lightweight TF-IDF retrieval pipeline:

Document
   ↓
Chunking
   ↓
TF-IDF Vectorization
   ↓
Normalized Vectors
   ↓
Cosine Similarity
   ↓
Similarity Threshold
   ↓
Relevant Context

A similarity threshold prevents irrelevant context from being used for questions.

💡 Key Engineering Decision

For deployment on limited-memory infrastructure, the project uses TF-IDF retrieval instead of heavyweight embedding models.

This keeps the application lightweight while still providing useful document retrieval.

🚀 Local Development
Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Frontend
cd frontend
npm install
npm run dev

Configure the required environment variables in .env.

🏆 Hacktoberfest

Built for Hacktoberfest Weekend Challenge 2026 — Build for a Friend.

The goal was to build a practical AI tool personalized for a real candidate rather than a generic chatbot.

👨‍💻 Author

Nagarjun M

CSE Undergraduate | Backend & AI Engineering
