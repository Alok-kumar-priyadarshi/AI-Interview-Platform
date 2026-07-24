import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { tokenStore } from "@/services/tokenStore";
import { useAuth } from "@/contexts/AuthContext";
import { ROUTES } from "@/constants/routes";
import { ErrorState, Spinner } from "@/components/ui";

/**
 * OAuth landing page. The backend completes the code exchange and redirects
 * here with the tokens in the URL fragment (`#access_token=…&refresh_token=…`)
 * on success, or `#error=…` on failure. We read the fragment, store the tokens,
 * and enter the app — no network call or cookie is required here.
 */
export function AuthCallbackPage() {
  const navigate = useNavigate();
  const { refresh } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const ran = useRef(false);

  useEffect(() => {
    if (ran.current) return;
    ran.current = true;

    const params = new URLSearchParams(window.location.hash.replace(/^#/, ""));
    const errorCode = params.get("error");
    const accessToken = params.get("access_token");
    const refreshToken = params.get("refresh_token");

    // Remove the tokens from the address bar / history immediately.
    window.history.replaceState(null, "", window.location.pathname);

    if (errorCode || !accessToken || !refreshToken) {
      setError("Sign-in failed. Please try again.");
      return;
    }

    tokenStore.setTokens(accessToken, refreshToken);
    void refresh().then(() => navigate(ROUTES.dashboard, { replace: true }));
  }, [navigate, refresh]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      {error ? (
        <ErrorState message={error} onRetry={() => navigate(ROUTES.login, { replace: true })} />
      ) : (
        <Spinner label="Signing you in…" />
      )}
    </div>
  );
}
