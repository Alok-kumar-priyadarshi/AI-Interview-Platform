import { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { interviewApi, resumeApi } from "@/services/api";
import { useAsync } from "@/hooks/useAsync";
import { ApiError } from "@/services/apiClient";
import { Card, Spinner, ErrorState, EmptyState, Button } from "@/components/ui";
import { ROUTES } from "@/constants/routes";
import type { InterviewCreatePayload } from "@/types/api";

export function NewInterviewPage() {
  const navigate = useNavigate();
  const { data: resumes, loading, error, reload } = useAsync(() => resumeApi.list(), []);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState<InterviewCreatePayload>({
    resume_id: "",
    interview_type: "technical",
    difficulty: "medium",
    mode: "text",
    language: "en",
    question_count: 5,
  });

  if (loading) return <Spinner />;
  if (error) return <ErrorState message={error} onRetry={reload} />;
  if (!resumes || resumes.length === 0)
    return (
      <EmptyState
        title="Upload a resume first"
        hint="Interviews are generated from your resume."
        action={
          <Button onClick={() => navigate(ROUTES.resume)}>Go to resumes</Button>
        }
      />
    );

  const completed = resumes.filter((r) => r.status === "completed");
  const usable = completed.length > 0 ? completed : resumes;
  const resumeId = form.resume_id || usable[0].id;

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const result = await interviewApi.create({ ...form, resume_id: resumeId });
      toast.success("Interview generated.");
      navigate(ROUTES.interview(result.interview_id));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Failed to create interview.");
    } finally {
      setSubmitting(false);
    }
  };

  const update = <K extends keyof InterviewCreatePayload>(key: K, value: InterviewCreatePayload[K]) =>
    setForm((f) => ({ ...f, [key]: value }));

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">New interview</h1>
      <Card>
        <form onSubmit={submit} className="space-y-5">
          <Field label="Resume">
            <select
              className="input"
              value={resumeId}
              onChange={(e) => update("resume_id", e.target.value)}
            >
              {usable.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.file_name}
                </option>
              ))}
            </select>
          </Field>

          <div className="grid gap-5 sm:grid-cols-2">
            <Field label="Focus">
              <select
                className="input"
                value={form.interview_type}
                onChange={(e) => update("interview_type", e.target.value as InterviewCreatePayload["interview_type"])}
              >
                <option value="technical">Technical</option>
                <option value="behavioral">Behavioral</option>
                <option value="mixed">Mixed</option>
              </select>
            </Field>
            <Field label="Difficulty">
              <select
                className="input"
                value={form.difficulty}
                onChange={(e) => update("difficulty", e.target.value as InterviewCreatePayload["difficulty"])}
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </Field>
            <Field label="Mode">
              <select
                className="input"
                value={form.mode}
                onChange={(e) => update("mode", e.target.value as InterviewCreatePayload["mode"])}
              >
                <option value="text">Text</option>
                <option value="voice">Voice</option>
              </select>
            </Field>
            <Field label="Number of questions">
              <input
                type="number"
                min={5}
                max={50}
                className="input"
                value={form.question_count}
                onChange={(e) => update("question_count", Number(e.target.value))}
              />
            </Field>
          </div>

          <Button type="submit" loading={submitting} className="w-full">
            Generate interview
          </Button>
        </form>
      </Card>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1 block text-sm font-medium text-slate-700">{label}</span>
      {children}
    </label>
  );
}
