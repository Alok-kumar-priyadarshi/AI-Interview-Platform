// Shared API types mirroring the backend response envelopes and domain models.

export interface SuccessEnvelope<T> {
  success: true;
  message: string;
  data: T;
}

export interface ErrorDetail {
  field: string;
  message: string;
}

export interface ErrorEnvelope {
  success: false;
  error: {
    code: string;
    message: string;
    details?: ErrorDetail[];
  };
  request_id?: string;
}

export interface Paginated<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

// --- Auth / user ---------------------------------------------------------
export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  profile_picture_url: string | null;
  role: string;
  is_active: boolean;
  last_login_at: string | null;
  created_at: string;
}

// --- Resume --------------------------------------------------------------
export interface ResumeSummary {
  id: string;
  file_name: string;
  status: string;
  uploaded_at: string;
  is_default: boolean;
}

export interface ResumeMetadata {
  professional_summary: string | null;
  total_experience_years: number | null;
  highest_education: string | null;
  current_job_title: string | null;
  skills: Record<string, unknown>[];
  languages: string[];
  ai_confidence_score: number | null;
}

// --- Interview -----------------------------------------------------------
export interface InterviewSummary {
  id: string;
  title: string;
  status: string;
  difficulty: string;
  mode: string;
  target_role: string;
  total_questions: number;
  answered_questions: number;
  overall_score: number | null;
  created_at: string;
  // Present on the detail response (GET /interviews/{id}).
  interviewer_voice?: string | null;
}

export interface InterviewCreatePayload {
  resume_id: string;
  interview_type: "technical" | "behavioral" | "mixed";
  difficulty: "easy" | "medium" | "hard";
  mode: "text" | "voice";
  language: "en" | "hi";
  interviewer_voice?: "male" | "female" | null;
  question_count: number;
  time_limit_minutes?: number | null;
}

export interface CurrentQuestion {
  question_id: string;
  sequence: number;
  category: string;
  difficulty: string;
  question: string;
  estimated_time_seconds: number | null;
}

export interface InterviewStatus {
  status: string;
  current_question: number | null;
  completed_questions: number;
  remaining_questions: number;
  elapsed_seconds: number | null;
}

// --- Reports / dashboard -------------------------------------------------
export interface ReportDetail {
  report_id: string;
  overall_score: number;
  grade: string;
  hiring_recommendation: string;
  summary: string;
  categories: Record<string, number>;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  generated_at: string;
}

export interface DashboardSummary {
  total_interviews: number;
  completed_interviews: number;
  average_score: number | null;
  highest_score: number | null;
  current_streak: number;
}

export interface DashboardOverview {
  summary: DashboardSummary;
  recent_interviews: Record<string, unknown>[];
  recommendations: { priority: string; title: string; description: string }[];
  achievements: { id: string; title: string }[];
}
