import { useParams } from "react-router-dom";
import { ThumbsUp, ThumbsDown, Lightbulb } from "lucide-react";
import { reportApi } from "@/services/api";
import { useAsync } from "@/hooks/useAsync";
import { Card, Spinner, ErrorState, Badge } from "@/components/ui";

const RECOMMENDATION_TONE: Record<string, "green" | "blue" | "amber" | "red"> = {
  strong_hire: "green",
  hire: "blue",
  borderline: "amber",
  no_hire: "red",
};

export function ReportPage() {
  const { id = "" } = useParams();
  const { data, loading, error, reload } = useAsync(() => reportApi.get(id), [id]);

  if (loading) return <Spinner label="Loading report…" />;
  if (error || !data) return <ErrorState message={error ?? "Report unavailable."} onRetry={reload} />;

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold text-slate-900">Interview Report</h1>
        <Badge tone={RECOMMENDATION_TONE[data.hiring_recommendation] ?? "slate"}>
          {data.hiring_recommendation.replace("_", " ")}
        </Badge>
      </div>

      <Card className="flex items-center gap-6">
        <div className="flex h-24 w-24 shrink-0 flex-col items-center justify-center rounded-full bg-brand-50">
          <span className="text-3xl font-bold text-brand-700">{Math.round(data.overall_score)}</span>
          <span className="text-xs text-slate-500">Grade {data.grade}</span>
        </div>
        <p className="text-slate-700">{data.summary}</p>
      </Card>

      {Object.keys(data.categories).length > 0 && (
        <Card>
          <h2 className="mb-4 font-semibold text-slate-900">Category scores</h2>
          <div className="space-y-3">
            {Object.entries(data.categories).map(([name, score]) => (
              <div key={name}>
                <div className="mb-1 flex justify-between text-sm">
                  <span className="capitalize text-slate-600">{name.replace(/_/g, " ")}</span>
                  <span className="font-medium text-slate-900">{Math.round(score)}</span>
                </div>
                <div className="h-2 rounded-full bg-slate-100">
                  <div className="h-2 rounded-full bg-brand-500" style={{ width: `${score}%` }} />
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        <ListCard icon={ThumbsUp} tone="text-green-600" title="Strengths" items={data.strengths} />
        <ListCard icon={ThumbsDown} tone="text-amber-600" title="Weaknesses" items={data.weaknesses} />
      </div>

      <Card>
        <h2 className="mb-4 flex items-center gap-2 font-semibold text-slate-900">
          <Lightbulb className="h-5 w-5 text-brand-600" aria-hidden /> Recommendations
        </h2>
        <ul className="list-inside list-disc space-y-1 text-slate-700">
          {data.recommendations.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      </Card>
    </div>
  );
}

function ListCard({
  icon: Icon,
  tone,
  title,
  items,
}: {
  icon: typeof ThumbsUp;
  tone: string;
  title: string;
  items: string[];
}) {
  return (
    <Card>
      <h2 className="mb-3 flex items-center gap-2 font-semibold text-slate-900">
        <Icon className={`h-5 w-5 ${tone}`} aria-hidden /> {title}
      </h2>
      {items.length === 0 ? (
        <p className="text-sm text-slate-400">None noted.</p>
      ) : (
        <ul className="list-inside list-disc space-y-1 text-sm text-slate-700">
          {items.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      )}
    </Card>
  );
}
