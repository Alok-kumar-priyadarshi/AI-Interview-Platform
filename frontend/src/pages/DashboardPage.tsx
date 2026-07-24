import { Link } from "react-router-dom";
import { Trophy, Target, Flame, CheckCircle2, ArrowRight } from "lucide-react";
import { dashboardApi } from "@/services/api";
import { useAsync } from "@/hooks/useAsync";
import { Card, Spinner, ErrorState, EmptyState, Button, Badge } from "@/components/ui";
import { TrendChart } from "@/components/TrendChart";
import { ROUTES } from "@/constants/routes";

export function DashboardPage() {
  const { data, loading, error, reload } = useAsync(() => dashboardApi.overview(), []);
  const trends = useAsync(() => dashboardApi.trends(), []);

  if (loading) return <Spinner />;
  if (error || !data) return <ErrorState message={error ?? "Unavailable."} onRetry={reload} />;

  const { summary, recommendations, achievements } = data;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <Link to={ROUTES.newInterview}>
          <Button>
            Start new interview <ArrowRight className="h-4 w-4" />
          </Button>
        </Link>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat icon={Target} label="Total interviews" value={summary.total_interviews} />
        <Stat icon={CheckCircle2} label="Completed" value={summary.completed_interviews} />
        <Stat
          icon={Trophy}
          label="Highest score"
          value={summary.highest_score !== null ? `${summary.highest_score}` : "—"}
        />
        <Stat icon={Flame} label="Current streak" value={`${summary.current_streak} day(s)`} />
      </div>

      <Card>
        <h2 className="mb-4 font-semibold text-slate-900">Performance trend</h2>
        {trends.loading ? <Spinner /> : <TrendChart data={trends.data ?? []} />}
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <h2 className="mb-4 font-semibold text-slate-900">Recommendations</h2>
          {recommendations.length === 0 ? (
            <EmptyState title="No recommendations yet" hint="Complete an interview to get personalized advice." />
          ) : (
            <ul className="space-y-3">
              {recommendations.map((rec, i) => (
                <li key={i} className="rounded-lg border border-slate-100 p-3">
                  <div className="mb-1 flex items-center gap-2">
                    <Badge tone={rec.priority === "high" ? "red" : "amber"}>{rec.priority}</Badge>
                    <span className="font-medium text-slate-800">{rec.title}</span>
                  </div>
                  <p className="text-sm text-slate-500">{rec.description}</p>
                </li>
              ))}
            </ul>
          )}
        </Card>

        <Card>
          <h2 className="mb-4 font-semibold text-slate-900">Achievements</h2>
          {achievements.length === 0 ? (
            <EmptyState title="No achievements yet" />
          ) : (
            <ul className="space-y-2">
              {achievements.map((a) => (
                <li key={a.id} className="flex items-center gap-3 rounded-lg bg-brand-50 p-3">
                  <Trophy className="h-5 w-5 text-brand-600" aria-hidden />
                  <span className="text-sm font-medium text-slate-800">{a.title}</span>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>
    </div>
  );
}

function Stat({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Target;
  label: string;
  value: string | number;
}) {
  return (
    <Card className="flex items-center gap-4">
      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-100">
        <Icon className="h-5 w-5 text-brand-600" aria-hidden />
      </div>
      <div>
        <p className="text-sm text-slate-500">{label}</p>
        <p className="text-xl font-bold text-slate-900">{value}</p>
      </div>
    </Card>
  );
}
