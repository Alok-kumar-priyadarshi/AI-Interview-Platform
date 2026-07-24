import { Link } from "react-router-dom";
import { Plus, Play, FileBarChart } from "lucide-react";
import { interviewApi } from "@/services/api";
import { useAsync } from "@/hooks/useAsync";
import { Card, Spinner, ErrorState, EmptyState, Button, Badge } from "@/components/ui";
import { ROUTES } from "@/constants/routes";

const STATUS_TONE: Record<string, "green" | "amber" | "blue" | "red" | "slate"> = {
  completed: "green",
  in_progress: "blue",
  ready: "amber",
  failed: "red",
  cancelled: "slate",
  created: "slate",
};

export function InterviewsPage() {
  const { data, loading, error, reload } = useAsync(() => interviewApi.list(1, 50), []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Interviews</h1>
        <Link to={ROUTES.newInterview}>
          <Button>
            <Plus className="h-4 w-4" /> New interview
          </Button>
        </Link>
      </div>

      {loading ? (
        <Spinner />
      ) : error ? (
        <ErrorState message={error} onRetry={reload} />
      ) : !data || data.items.length === 0 ? (
        <EmptyState
          title="No interviews yet"
          hint="Create your first mock interview from a resume."
          action={
            <Link to={ROUTES.newInterview}>
              <Button>Start now</Button>
            </Link>
          }
        />
      ) : (
        <div className="space-y-3">
          {data.items.map((iv) => (
            <Card key={iv.id} className="flex flex-wrap items-center gap-4">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <p className="font-medium text-slate-800">{iv.title}</p>
                  <Badge tone={STATUS_TONE[iv.status] ?? "slate"}>{iv.status}</Badge>
                </div>
                <p className="text-xs text-slate-400">
                  {iv.difficulty} · {iv.mode} · {iv.answered_questions}/{iv.total_questions} answered
                </p>
              </div>
              {iv.overall_score !== null && (
                <span className="text-lg font-bold text-slate-900">{iv.overall_score}</span>
              )}
              {iv.status === "completed" ? (
                <Link to={ROUTES.report(iv.id)}>
                  <Button variant="secondary" size="sm">
                    <FileBarChart className="h-4 w-4" /> Report
                  </Button>
                </Link>
              ) : (
                <Link to={ROUTES.interview(iv.id)}>
                  <Button size="sm">
                    <Play className="h-4 w-4" /> Open
                  </Button>
                </Link>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
