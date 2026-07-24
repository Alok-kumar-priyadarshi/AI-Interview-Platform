import { Navigate } from "react-router-dom";
import { Sparkles } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { authApi } from "@/services/api";
import { ROUTES } from "@/constants/routes";
import { Spinner } from "@/components/ui";

export function LoginPage() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <Spinner label="Loading…" />;
  if (isAuthenticated) return <Navigate to={ROUTES.dashboard} replace />;

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-brand-50 to-slate-100 p-6">
      <div className="card w-full max-w-md p-8 text-center">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-brand-600">
          <Sparkles className="h-6 w-6 text-white" aria-hidden />
        </div>
        <h1 className="text-2xl font-bold text-slate-900">AI Career Interview Platform</h1>
        <p className="mt-2 text-sm text-slate-500">
          Practice AI-powered mock interviews tailored to your resume and target role.
        </p>
        <a
          href={authApi.googleLoginUrl()}
          className="mt-8 flex w-full items-center justify-center gap-3 rounded-lg border border-slate-300 bg-white px-4 py-2.5 font-medium text-slate-700 transition-colors hover:bg-slate-50"
        >
          <GoogleIcon />
          Continue with Google
        </a>
        <p className="mt-6 text-xs text-slate-400">
          By continuing you agree to practice interviews being processed by AI.
        </p>
      </div>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg className="h-5 w-5" viewBox="0 0 24 24" aria-hidden>
      <path
        fill="#4285F4"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.27-4.74 3.27-8.1z"
      />
      <path
        fill="#34A853"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23z"
      />
      <path
        fill="#FBBC05"
        d="M5.84 14.09a6.6 6.6 0 0 1 0-4.18V7.07H2.18a11 11 0 0 0 0 9.86l3.66-2.84z"
      />
      <path
        fill="#EA4335"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84C6.71 7.31 9.14 5.38 12 5.38z"
      />
    </svg>
  );
}
