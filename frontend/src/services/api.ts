// Typed API surface. UI components never call axios directly — they use these
// functions (usually via hooks).

import client, { unwrap } from "@/services/apiClient";
import type {
  CurrentQuestion,
  DashboardOverview,
  InterviewCreatePayload,
  InterviewStatus,
  InterviewSummary,
  Paginated,
  ReportDetail,
  ResumeMetadata,
  ResumeSummary,
  User,
} from "@/types/api";

const API = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export const authApi = {
  /** Full-page redirect URL that starts the Google OAuth flow. */
  googleLoginUrl: (): string => `${API}/auth/google/login`,
  me: () => unwrap<User>(client.get("/auth/me")),
  logout: () => client.post("/auth/logout"),
};

export const userApi = {
  me: () => unwrap<User>(client.get("/users/me")),
  updateProfile: (fullName: string) =>
    unwrap<User>(client.patch("/users/me", { full_name: fullName })),
  statistics: () => unwrap<Record<string, number | null>>(client.get("/users/me/statistics")),
};

export const resumeApi = {
  list: () => unwrap<ResumeSummary[]>(client.get("/resumes")),
  upload: (file: File, onProgress?: (pct: number) => void) => {
    const form = new FormData();
    form.append("file", file);
    return unwrap<{ resume_id: string; status: string }>(
      client.post("/resumes", form, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (e) => {
          if (onProgress && e.total) onProgress(Math.round((e.loaded / e.total) * 100));
        },
      }),
    );
  },
  metadata: (id: string) => unwrap<ResumeMetadata>(client.get(`/resumes/${id}/metadata`)),
  setDefault: (id: string) => client.patch(`/resumes/${id}/default`),
  remove: (id: string) => client.delete(`/resumes/${id}`),
};

export const interviewApi = {
  list: (page = 1, pageSize = 20) =>
    unwrap<Paginated<InterviewSummary>>(
      client.get("/interviews", { params: { page, page_size: pageSize } }),
    ),
  create: (payload: InterviewCreatePayload) =>
    unwrap<{ interview_id: string; status: string }>(client.post("/interviews", payload)),
  get: (id: string) => unwrap<InterviewSummary>(client.get(`/interviews/${id}`)),
  status: (id: string) => unwrap<InterviewStatus>(client.get(`/interviews/${id}/status`)),
  start: (id: string) => client.post(`/interviews/${id}/start`),
  complete: (id: string) => client.post(`/interviews/${id}/complete`),
  cancel: (id: string) => client.post(`/interviews/${id}/cancel`),
  currentQuestion: (id: string) =>
    unwrap<CurrentQuestion>(client.get(`/interviews/${id}/questions/current`)),
  submitAnswer: (id: string, questionId: string, answer: string) =>
    unwrap<{ answer_id: string; submitted_at: string }>(
      client.post(`/interviews/${id}/answers`, { question_id: questionId, answer }),
    ),
  submitVoiceAnswer: (id: string, questionId: string, audio: Blob, language = "en") => {
    const form = new FormData();
    form.append("question_id", questionId);
    form.append("language", language);
    form.append("audio", audio, "answer.webm");
    return unwrap<{ answer_id: string; transcription_status: string }>(
      client.post(`/interviews/${id}/answers/voice`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      }),
    );
  },
};

export const reportApi = {
  list: (page = 1, pageSize = 20) =>
    unwrap<Paginated<{ report_id: string; overall_score: number; grade: string; created_at: string }>>(
      client.get("/reports", { params: { page, page_size: pageSize } }),
    ),
  get: (id: string) => unwrap<ReportDetail>(client.get(`/reports/${id}`)),
  forInterview: (interviewId: string) =>
    unwrap<{ report_id: string; status: string }>(client.get(`/interviews/${interviewId}/report`)),
};

export const dashboardApi = {
  overview: () => unwrap<DashboardOverview>(client.get("/dashboard")),
  statistics: () => unwrap<Record<string, number | null>>(client.get("/dashboard/statistics")),
  trends: () => unwrap<{ date: string; score: number }[]>(client.get("/dashboard/trends")),
};
