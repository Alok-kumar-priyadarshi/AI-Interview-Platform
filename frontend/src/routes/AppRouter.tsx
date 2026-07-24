import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { AuthenticatedLayout } from "@/layouts/AuthenticatedLayout";
import { Spinner } from "@/components/ui";
import { ROUTES } from "@/constants/routes";
import { LoginPage } from "@/pages/LoginPage";
import { AuthCallbackPage } from "@/pages/AuthCallbackPage";

// Lazy-load authenticated pages so heavy deps (charts, animations) are split
// out of the initial bundle (frontend-architecture.md — code splitting).
const DashboardPage = lazy(() => import("@/pages/DashboardPage").then((m) => ({ default: m.DashboardPage })));
const ResumePage = lazy(() => import("@/pages/ResumePage").then((m) => ({ default: m.ResumePage })));
const InterviewsPage = lazy(() => import("@/pages/InterviewsPage").then((m) => ({ default: m.InterviewsPage })));
const NewInterviewPage = lazy(() => import("@/pages/NewInterviewPage").then((m) => ({ default: m.NewInterviewPage })));
const InterviewRunPage = lazy(() => import("@/pages/InterviewRunPage").then((m) => ({ default: m.InterviewRunPage })));
const ReportPage = lazy(() => import("@/pages/ReportPage").then((m) => ({ default: m.ReportPage })));
const HistoryPage = lazy(() => import("@/pages/HistoryPage").then((m) => ({ default: m.HistoryPage })));
const ProfilePage = lazy(() => import("@/pages/ProfilePage").then((m) => ({ default: m.ProfilePage })));
const NotFoundPage = lazy(() => import("@/pages/NotFoundPage").then((m) => ({ default: m.NotFoundPage })));

export function AppRouter() {
  return (
    <Suspense fallback={<Spinner label="Loading…" />}>
      <Routes>
        <Route path={ROUTES.login} element={<LoginPage />} />
        <Route path={ROUTES.authCallback} element={<AuthCallbackPage />} />

        <Route
          element={
            <ProtectedRoute>
              <AuthenticatedLayout />
            </ProtectedRoute>
          }
        >
          <Route path={ROUTES.home} element={<Navigate to={ROUTES.dashboard} replace />} />
          <Route path={ROUTES.dashboard} element={<DashboardPage />} />
          <Route path={ROUTES.resume} element={<ResumePage />} />
          <Route path={ROUTES.interviews} element={<InterviewsPage />} />
          <Route path={ROUTES.newInterview} element={<NewInterviewPage />} />
          <Route path={ROUTES.interview()} element={<InterviewRunPage />} />
          <Route path={ROUTES.report()} element={<ReportPage />} />
          <Route path={ROUTES.history} element={<HistoryPage />} />
          <Route path={ROUTES.profile} element={<ProfilePage />} />
        </Route>

        <Route path={ROUTES.notFound} element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
}
