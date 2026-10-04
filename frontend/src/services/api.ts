import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export interface Evaluation {
  technical_accuracy: number;
  depth: number;
  clarity: number;
  strengths: string[];
  missing_concepts: string[];
  decision: string;
  reason: string;
}

export interface Weakness {
  topic: string;
  occurrences: number;
  last_reason: string;
  severity: number;
}

export interface InterviewReport {
  total_questions: number;
  average_technical_accuracy: number;
  average_depth: number;
  average_clarity: number;
  overall_score: number;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
}

export interface InterviewStartResponse {
  session_id: string;
  question: string;
}

export interface AnswerResponse {
  evaluation: Evaluation;
  next_question: string;
}

export async function startInterview(
  candidateId: string,
  jobDescriptionId: string
): Promise<InterviewStartResponse> {
  const response = await API.post("/api/interview/session", null, {
    params: {
      candidate_id: candidateId,
      job_description_id: jobDescriptionId,
    },
  });

  return response.data;
}

export async function submitAnswer(
  sessionId: string,
  answer: string
): Promise<AnswerResponse> {
  const response = await API.post(
    `/api/interview/session/${sessionId}/answer`,
    {
      answer,
    }
  );

  return response.data;
}

export async function getQuestionReason(
  sessionId: string
) {
  const response = await API.post(
    `/api/interview/session/${sessionId}/question-reason`
  );

  return response.data;
}

export async function getInterviewReport(
  sessionId: string
): Promise<InterviewReport> {
  const response = await API.get(
    `/api/interview/session/${sessionId}/report`
  );

  return response.data;
}

export async function getWeaknesses(
  candidateId: string
): Promise<{ candidate_id: string; weaknesses: Weakness[] }> {
  const response = await API.get("/api/weaknesses", {
    params: {
      candidate_id: candidateId,
    },
  });

  return response.data;
}

export async function getHealth() {
  const response = await API.get("/health");
  return response.data;
}

export interface ParsedCandidate {
  candidate_id: string;
  name: string;
  target_role: string;
  experience_years: number;
  skills: string[];
  projects: string[];
}

export async function parseResume(
  resumeText: string
): Promise<ParsedCandidate> {
  const response = await API.post(
    "/api/onboarding/parse-resume",
    {
      resume_text: resumeText,
    }
  );

  return response.data.candidate;
}


export async function createCandidate(
  candidate: ParsedCandidate
): Promise<ParsedCandidate> {
  const response = await API.post(
    "/api/onboarding/candidate",
    candidate
  );

  return response.data;
}


export async function createJobDescription(
  company: string,
  role: string,
  requiredSkills: string[],
  preferredSkills: string[],
  responsibilities: string[]
) {
  const response = await API.post(
    "/api/onboarding/job-description",
    {
      company,
      role,
      required_skills: requiredSkills,
      preferred_skills: preferredSkills,
      responsibilities,
    }
  );

  return response.data;
}