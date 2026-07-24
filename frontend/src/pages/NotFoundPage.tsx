import { Link } from "react-router-dom";
import { Button } from "@/components/ui";
import { ROUTES } from "@/constants/routes";

export function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 p-6 text-center">
      <p className="text-6xl font-bold text-brand-600">404</p>
      <p className="text-slate-600">This page could not be found.</p>
      <Link to={ROUTES.dashboard}>
        <Button>Back to dashboard</Button>
      </Link>
    </div>
  );
}
