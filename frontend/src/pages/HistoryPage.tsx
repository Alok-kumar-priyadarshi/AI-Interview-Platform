import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import client, { ApiError, unwrap } from "@/services/apiClient";
import { reportApi } from "@/services/api";
import { useAsync } from "@/hooks/useAsync";
import { Card, Spinner, ErrorState, EmptyState, Badge, Button } from "@/components/ui";
import { ROUTES } from "@/constants/routes";
import type { Paginated } from "@/types/api";

interface HistoryItem {
  history_id: string;
  interview_id: string;
  completed_at: string | null;
  overall_score: number | null;
  grade: string;
  difficulty: string;
  mode: string;
  target_role: string;
}

const historyApi = {
  list: () => unwrap<Paginated<HistoryItem>>(client.get("/history", { params: { page: 1, page_size: 50 } })),
};

export function HistoryPage() {
  const navigate = useNavigate();
  const { data, loading, error, reload } = useAsync(() => historyApi.list(), []);

  const openReport = async (interviewId: string) => {
    try {
      const ref = await reportApi.forInterview(interviewId);
      navigate(ROUTES.report(ref.report_id));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Report not available.");
    }
  };

  if (loading) return <Spinner />;
  if (error) return <ErrorState message={error} onRetry={reload} />;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">History</h1>
      {!data || data.items.length === 0 ? (
        <EmptyState title="No completed interviews yet" hint="Finish an interview to see it here." />
      ) : (
        <div className="space-y-3">
          {data.items.map((item) => (
            <Card key={item.history_id} className="flex flex-wrap items-center gap-4">
              <div className="min-w-0 flex-1">
                <p className="font-medium text-slate-800">{item.target_role}</p>
                <p className="text-xs text-slate-400">
                  {item.difficulty} · {item.mode}
                  {item.completed_at && ` · ${new Date(item.completed_at).toLocaleDateString()}`}
                </p>
              </div>
              {item.overall_score !== null && (
                <Badge tone="green">
                  {item.overall_score} · {item.grade}
                </Badge>
              )}
              <Button variant="secondary" size="sm" onClick={() => openReport(item.interview_id)}>
                View report
              </Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
