import * as pdfjsLib from "pdfjs-dist";
import { useState } from "react";

pdfjsLib.GlobalWorkerOptions.workerSrc =
  `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.mjs`;
import {
  startInterview,
  submitAnswer,
  getQuestionReason,
  getInterviewReport,
  getWeaknesses,
  parseResume,
  createCandidate,
  createJobDescription,
  type Evaluation,
  type InterviewReport,
  type Weakness,
} from "./services/api";
import "./index.css";

type Screen = "setup" | "interview" | "report";

function App() {
  const [screen, setScreen] = useState<Screen>("setup");

  const [candidateId, setCandidateId] = useState("nagarjun");
  const [jobDescriptionId, setJobDescriptionId] = useState("");

  const [sessionId, setSessionId] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [resumeFile, setResumeFile] = useState<File | null>(null);

const [parsedCandidate, setParsedCandidate] =
  useState<any>(null);

const [targetRole, setTargetRole] =
  useState("");

const [jobDescription, setJobDescription] =
  useState("");

const [parsingResume, setParsingResume] =
  useState(false);

  const [evaluation, setEvaluation] =
    useState<Evaluation | null>(null);

  const [report, setReport] =
    useState<InterviewReport | null>(null);

  const [weaknesses, setWeaknesses] =
    useState<Weakness[]>([]);

  const [questionReason, setQuestionReason] =
    useState("");

  const [loading, setLoading] = useState(false);
  const [reasonLoading, setReasonLoading] = useState(false);
  const [error, setError] = useState("");

  const [questionNumber, setQuestionNumber] = useState(1);

  // ============================================================
  // RESUME-BASED ONBOARDING + START INTERVIEW
  // ============================================================

  async function handleResumeUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      setError("Please upload a PDF resume.");
      return;
    }

    try {
      setParsingResume(true);
      setError("");
      setParsedCandidate(null);

      const text = await extractPdfText(file);

      if (!text.trim()) {
        throw new Error(
          "Could not extract text from this PDF. Please use a text-based PDF."
        );
      }

      const candidate = await parseResume(text);

      setResumeFile(file);
      setParsedCandidate(candidate);
      setCandidateId(candidate.candidate_id);
      setTargetRole(candidate.target_role || "");

    } catch (err: any) {
      console.error("RESUME PARSING ERROR:", err);

      setError(
        err?.response?.data?.detail ||
          err?.message ||
          "Could not parse the resume."
      );
    } finally {
      setParsingResume(false);
    }
  }

  async function handleStartInterview() {
    if (!parsedCandidate) {
      setError("Please upload and parse your resume first.");
      return;
    }

    if (!targetRole.trim()) {
      setError("Please enter your target role.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setEvaluation(null);

      const candidate = {
        ...parsedCandidate,
        candidate_id:
          parsedCandidate.candidate_id || candidateId.trim(),
        target_role: targetRole.trim(),
      };

      setCandidateId(candidate.candidate_id);

      try {
        await createCandidate(candidate);
      } catch (candidateError: any) {
        const detail =
          candidateError?.response?.data?.detail || "";

        if (
          !detail.toLowerCase().includes("already exists") &&
          candidateError?.response?.status !== 400
        ) {
          throw candidateError;
        }
      }

      let newJobDescriptionId = "";

      if (jobDescription.trim()) {
        const jobResult = await createJobDescription(
          "Target Company",
          targetRole.trim(),
          candidate.skills || [],
          [],
          jobDescription
            .split("\n")
            .map((line: string) => line.trim())
            .filter((line: string) => line.length > 0)
        );

        newJobDescriptionId =
          jobResult.job_description_id;
      } else {
        const jobResult = await createJobDescription(
          "General",
          targetRole.trim(),
          candidate.skills || [],
          [],
          []
        );

        newJobDescriptionId =
          jobResult.job_description_id;
      }

      setJobDescriptionId(newJobDescriptionId);

      const result = await startInterview(
        candidate.candidate_id,
        newJobDescriptionId
      );

      setSessionId(result.session_id);
      setQuestion(result.question);
      setAnswer("");
      setQuestionNumber(1);
      setScreen("interview");

      try {
        const weaknessResult = await getWeaknesses(
          candidate.candidate_id
        );

        setWeaknesses(
          weaknessResult.weaknesses || []
        );
      } catch {
        // Weakness loading should not stop the interview
      }
    } catch (err: any) {
      console.error("START INTERVIEW ERROR:", err);

      setError(
        err?.response?.data?.detail ||
          "Could not start the interview. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

async function extractPdfText(file: File) {
  try {
    const arrayBuffer = await file.arrayBuffer();

    const loadingTask = pdfjsLib.getDocument({
      data: new Uint8Array(arrayBuffer),
    });

    const pdf = await loadingTask.promise;

    let fullText = "";

    for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
      const page = await pdf.getPage(pageNumber);
      const content = await page.getTextContent();

      const pageText = content.items
        .map((item: any) => {
          if ("str" in item) {
            return item.str;
          }
          return "";
        })
        .join(" ");

      fullText += pageText + "\n";
    }

    const cleanedText = fullText
      .replace(/\s+/g, " ")
      .trim();

    console.log("PDF extracted text:", cleanedText);
    console.log("Extracted characters:", cleanedText.length);

    if (!cleanedText || cleanedText.length < 20) {
      throw new Error(
        "This PDF does not contain enough selectable text. It may be an image/scanned PDF."
      );
    }

    return cleanedText;
  } catch (error) {
    console.error("PDF extraction error:", error);
    throw new Error(
      "Could not extract text from this PDF. Please use a text-based PDF."
    );
  }
}

  // ==========================================================
  // SUBMIT ANSWER
  // ============================================================

  async function handleSubmitAnswer() {
    if (!answer.trim()) {
      setError("Please enter your answer first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const result = await submitAnswer(
        sessionId,
        answer
      );

      setEvaluation(result.evaluation);

      setQuestion(result.next_question);
      setAnswer("");

      setQuestionNumber(
        (previous) => previous + 1
      );

      // Refresh persistent weaknesses
      try {
        const weaknessResult = await getWeaknesses(
          candidateId
        );

        setWeaknesses(
          weaknessResult.weaknesses || []
        );
      } catch {
        // Don't interrupt interview
      }
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          "Could not submit the answer."
      );
    } finally {
      setLoading(false);
    }
  }

  // ============================================================
  // QUESTION REASON
  // ============================================================

async function handleQuestionReason() {
  try {
    setReasonLoading(true);
    setError("");

    const result = await getQuestionReason(sessionId);

    console.log("QUESTION REASON RESPONSE:", result);

    const reason =
      typeof result === "string"
        ? result
        : result.reason ||
          result.explanation ||
          "This question was selected based on your profile, skills, projects, job requirements, and previous interview performance.";

    setQuestionReason(reason);
  } catch (err: any) {
    console.error("QUESTION REASON ERROR:", err);

    setError(
      err?.response?.data?.detail ||
        "Could not get the question reason."
    );
  } finally {
    setReasonLoading(false);
  }
}

  // ============================================================
  // END INTERVIEW
  // ============================================================

  async function handleEndInterview() {
    try {
      setLoading(true);
      setError("");

      const result =
        await getInterviewReport(sessionId);

      setReport(result);
      setScreen("report");
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          "Could not generate the interview report."
      );
    } finally {
      setLoading(false);
    }
  }

  // ============================================================
  // RESET
  // ============================================================

  function handleNewInterview() {
    setScreen("setup");
    setSessionId("");
    setQuestion("");
    setAnswer("");
    setEvaluation(null);
    setReport(null);
    setQuestionReason("");
    setError("");
    setQuestionNumber(1);
    setJobDescriptionId("");
  }

  // ============================================================
  // SETUP SCREEN
  // ============================================================

  if (screen === "setup") {
    return (
      <div className="app">
        <header className="navbar">
          <div className="brand">
            <div className="brand-icon">IB</div>
            <span>InterviewBuddy</span>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            AI Interview Platform
          </div>
        </header>

        <main className="setup-container">
          <section className="hero">
            <div className="badge">
              AI-Powered Mock Interviews
            </div>

            <h1>
              Prepare smarter.
              <br />
              <span>Interview better.</span>
            </h1>

            <p>
              InterviewBuddy conducts adaptive technical
              interviews based on your actual resume,
              target role, job requirements, and previous
              weaknesses.
            </p>
          </section>

          <section className="setup-card">
            <div className="card-header">
              <div>
                <h2>Set Up Your Interview</h2>
                <p>
                  Upload your resume and InterviewBuddy will
                  build your candidate profile automatically.
                </p>
              </div>
            </div>

            <div className="form-group">
              <label>Resume PDF</label>

              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleResumeUpload}
                disabled={parsingResume || loading}
              />

              <small>
                Your resume is used to extract your skills
                and projects for personalized questions.
              </small>
            </div>

            {parsingResume && (
              <div className="memory-preview">
                <div className="section-title">
                  📄 Reading your resume...
                </div>

                <p>
                  InterviewBuddy is extracting your
                  profile. This may take a moment.
                </p>
              </div>
            )}

            {resumeFile && parsedCandidate && !parsingResume && (
              <div className="memory-preview">
                <div className="section-title">
                  ✓ Resume Parsed
                </div>

                <p>
                  <strong>Name:</strong>{" "}
                  {parsedCandidate.name}
                </p>

                <p>
                  <strong>Skills:</strong>{" "}
                  {(parsedCandidate.skills || []).join(", ") ||
                    "No skills extracted"}
                </p>

                <p>
                  <strong>Projects:</strong>{" "}
                  {(parsedCandidate.projects || []).join(", ") ||
                    "No projects extracted"}
                </p>
              </div>
            )}

            <div className="form-group">
              <label>Target Role</label>

              <input
                value={targetRole}
                onChange={(e) =>
                  setTargetRole(e.target.value)
                }
                placeholder="e.g. Backend Developer"
                disabled={loading}
              />

              <small>
                Tell InterviewBuddy what role you are
                preparing for.
              </small>
            </div>

            <div className="form-group">
              <label>
                Job Description{" "}
                <span style={{ opacity: 0.6 }}>
                  (Optional)
                </span>
              </label>

              <textarea
                value={jobDescription}
                onChange={(e) =>
                  setJobDescription(e.target.value)
                }
                placeholder="Paste the job description here for a job-specific interview. You can leave this empty for a general role-based interview."
                rows={7}
                disabled={loading}
              />

              <small>
                Optional. Adding a JD makes the questions
                more closely match the job requirements.
              </small>
            </div>

            {error && (
              <div className="error">
                {error}
              </div>
            )}

            <button
              className="primary-button"
              onClick={handleStartInterview}
              disabled={
                loading ||
                parsingResume ||
                !parsedCandidate ||
                !targetRole.trim()
              }
            >
              {loading
                ? "Preparing Interview..."
                : "Start Interview →"}
            </button>
          </section>

          {weaknesses.length > 0 && (
            <section className="memory-preview">
              <div className="section-title">
                <span>🧠</span>
                Your Interview Memory
              </div>

              <p>
                InterviewBuddy has remembered these
                areas from previous interviews.
              </p>

              <div className="weakness-list">
                {weaknesses.slice(0, 4).map(
                  (weakness) => (
                    <div
                      className="weakness-mini"
                      key={weakness.topic}
                    >
                      <span>{weakness.topic}</span>

                      <strong>
                        {weakness.occurrences}x
                      </strong>
                    </div>
                  )
                )}
              </div>
            </section>
          )}

          <section className="feature-grid">
            <Feature
              icon="🎯"
              title="Adaptive Questions"
              text="Questions change based on your answers."
            />

            <Feature
              icon="🧠"
              title="Persistent Memory"
              text="Weak areas are remembered across sessions."
            />

            <Feature
              icon="📚"
              title="RAG Grounding"
              text="Questions are grounded in your profile and job."
            />

            <Feature
              icon="📊"
              title="Detailed Evaluation"
              text="Get technical, depth and clarity feedback."
            />
          </section>
        </main>
      </div>
    );
  }

  // ============================================================
  // INTERVIEW SCREEN
  // ============================================================

  if (screen === "interview") {
    return (
      <div className="app">
        <header className="navbar">
          <div className="brand">
            <div className="brand-icon">IB</div>
            <span>InterviewBuddy</span>
          </div>

          <div className="interview-status">
            Question {questionNumber}
          </div>
        </header>

        <main className="interview-container">

          <div className="interview-top">
            <div>
              <span className="eyebrow">
                TECHNICAL INTERVIEW
              </span>

              <h1>
                Let's see what you know.
              </h1>
            </div>

            <button
              className="end-button"
              onClick={handleEndInterview}
              disabled={loading}
            >
              End Interview
            </button>
          </div>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

          <div className="interview-grid">

            <section className="question-card">

              <div className="question-number">
                QUESTION {questionNumber}
              </div>

              <h2>{question}</h2>

              <button
                className="reason-button"
                onClick={handleQuestionReason}
                disabled={reasonLoading}
              >
                {reasonLoading
                  ? "Thinking..."
                  : "💡 Why am I being asked this?"}
              </button>

              {questionReason && (
                <div className="reason-box">
                  <strong>Why this question?</strong>
                  <p>{questionReason}</p>
                </div>
              )}

              <div className="answer-section">

                <label>Your Answer</label>

                <textarea
                  value={answer}
                  onChange={(e) =>
                    setAnswer(e.target.value)
                  }
                  placeholder="Explain your answer clearly. You can include technical details, examples, and reasoning..."
                  rows={9}
                />

                <div className="answer-footer">
                  <span>
                    Take your time. Quality matters more
                    than speed.
                  </span>

                  <button
                    className="primary-button submit-button"
                    onClick={handleSubmitAnswer}
                    disabled={
                      loading || !answer.trim()
                    }
                  >
                    {loading
                      ? "Evaluating..."
                      : "Submit Answer →"}
                  </button>
                </div>
              </div>
            </section>

            <aside>

              <div className="side-card">
                <div className="side-title">
                  <span>🧠</span>
                  What InterviewBuddy Knows
                </div>

                <div className="side-item">
                  <span>Candidate</span>
                  <strong>{candidateId}</strong>
                </div>

                <div className="side-item">
                  <span>Memory</span>
                  <strong>
                    {weaknesses.length} weaknesses
                  </strong>
                </div>

                <div className="side-item">
                  <span>Mode</span>
                  <strong>Adaptive</strong>
                </div>
              </div>

              {weaknesses.length > 0 && (
                <div className="side-card">
                  <div className="side-title">
                    Previous Weaknesses
                  </div>

                  {weaknesses.slice(0, 5).map(
                    (weakness) => (
                      <div
                        className="weakness-row"
                        key={weakness.topic}
                      >
                        <div>
                          <span>
                            {weakness.topic}
                          </span>

                          <small>
                            Seen {weakness.occurrences}x
                          </small>
                        </div>

                        <div className="severity">
                          {weakness.severity}/10
                        </div>
                      </div>
                    )
                  )}
                </div>
              )}
            </aside>
          </div>

          {evaluation && (
            <EvaluationCard
              evaluation={evaluation}
            />
          )}

        </main>
      </div>
    );
  }

  // ============================================================
  // REPORT SCREEN
  // ============================================================

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">IB</div>
          <span>InterviewBuddy</span>
        </div>

        <div className="status">
          Interview Complete
        </div>
      </header>

      <main className="report-container">

        <div className="report-header">
          <div className="badge">
            Interview Complete
          </div>

          <h1>Your Interview Report</h1>

          <p>
            Here's how you performed in this interview.
          </p>
        </div>

        {report && (
          <>
            <div className="score-card">
              <div>
                <span className="score-label">
                  OVERALL SCORE
                </span>

                <div className="big-score">
                  {report.overall_score}
                  <span>/10</span>
                </div>
              </div>

              <div className="score-message">
                <h3>
                  Keep improving.
                </h3>

                <p>
                  Your performance has been analyzed
                  across multiple technical dimensions.
                </p>
              </div>
            </div>

            <div className="metrics-grid">

              <Metric
                label="Technical Accuracy"
                value={
                  report.average_technical_accuracy
                }
              />

              <Metric
                label="Depth"
                value={report.average_depth}
              />

              <Metric
                label="Clarity"
                value={report.average_clarity}
              />

              <Metric
                label="Questions"
                value={report.total_questions}
                suffix=""
              />

            </div>

            <div className="report-grid">

              <ReportSection
                title="Strengths"
                icon="✓"
                items={report.strengths}
                emptyText="No strengths recorded."
              />

              <ReportSection
                title="Weaknesses"
                icon="!"
                items={report.weaknesses}
                emptyText="No weaknesses recorded."
              />

              <ReportSection
                title="Recommendations"
                icon="→"
                items={report.recommendations}
                emptyText="No recommendations available."
              />

            </div>

            {weaknesses.length > 0 && (
              <section className="persistent-memory">
                <div className="section-title">
                  🧠 Persistent Memory
                </div>

                <p>
                  These weaknesses are stored in
                  PostgreSQL and will be available in
                  future interviews.
                </p>

                <div className="weakness-list">
                  {weaknesses.map((weakness) => (
                    <div
                      className="weakness-mini"
                      key={weakness.topic}
                    >
                      <span>
                        {weakness.topic}
                      </span>

                      <strong>
                        {weakness.occurrences}x
                      </strong>
                    </div>
                  ))}
                </div>
              </section>
            )}

            <button
              className="primary-button new-interview"
              onClick={handleNewInterview}
            >
              Start New Interview →
            </button>
          </>
        )}
      </main>
    </div>
  );
}


// ============================================================
// COMPONENTS
// ============================================================

function Feature({
  icon,
  title,
  text,
}: {
  icon: string;
  title: string;
  text: string;
}) {
  return (
    <div className="feature-card">
      <div className="feature-icon">
        {icon}
      </div>

      <h3>{title}</h3>

      <p>{text}</p>
    </div>
  );
}


function EvaluationCard({
  evaluation,
}: {
  evaluation: Evaluation;
}) {
  return (
    <section className="evaluation-card">

      <div className="evaluation-header">
        <div>
          <span className="eyebrow">
            AI EVALUATION
          </span>

          <h2>How did you do?</h2>
        </div>

        <div className="decision">
          {evaluation.decision}
        </div>
      </div>

      <div className="evaluation-metrics">

        <Metric
          label="Technical Accuracy"
          value={evaluation.technical_accuracy}
        />

        <Metric
          label="Depth"
          value={evaluation.depth}
        />

        <Metric
          label="Clarity"
          value={evaluation.clarity}
        />

      </div>

      <div className="evaluation-columns">

        <div>
          <h3>✓ Strengths</h3>

          {evaluation.strengths.length > 0 ? (
            <ul>
              {evaluation.strengths.map(
                (item) => (
                  <li key={item}>{item}</li>
                )
              )}
            </ul>
          ) : (
            <p className="muted">
              No specific strengths recorded.
            </p>
          )}
        </div>

        <div>
          <h3>! Missing Concepts</h3>

          {evaluation.missing_concepts.length > 0 ? (
            <ul>
              {evaluation.missing_concepts.map(
                (item) => (
                  <li key={item}>{item}</li>
                )
              )}
            </ul>
          ) : (
            <p className="muted">
              No major missing concepts.
            </p>
          )}
        </div>

      </div>

      <div className="evaluation-reason">
        <strong>AI Feedback</strong>
        <p>{evaluation.reason}</p>
      </div>

    </section>
  );
}


function Metric({
  label,
  value,
  suffix = "/10",
}: {
  label: string;
  value: number;
  suffix?: string;
}) {
  return (
    <div className="metric">
      <span>{label}</span>

      <strong>
        {typeof value === "number"
          ? Number(value).toFixed(
              value % 1 === 0 ? 0 : 1
            )
          : value}

        {suffix}
      </strong>
    </div>
  );
}


function ReportSection({
  title,
  icon,
  items,
  emptyText,
}: {
  title: string;
  icon: string;
  items: string[];
  emptyText: string;
}) {
  return (
    <section className="report-section">

      <h2>
        <span>{icon}</span>
        {title}
      </h2>

      {items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="muted">
          {emptyText}
        </p>
      )}

    </section>
  );
}


export default App;