import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { LayoutDashboard, FileText, MessageSquare, History, User, LogOut, Sparkles } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { ROUTES } from "@/constants/routes";

const NAV = [
  { to: ROUTES.dashboard, label: "Dashboard", icon: LayoutDashboard },
  { to: ROUTES.resume, label: "Resume", icon: FileText },
  { to: ROUTES.interviews, label: "Interviews", icon: MessageSquare },
  { to: ROUTES.history, label: "History", icon: History },
  { to: ROUTES.profile, label: "Profile", icon: User },
];

export function AuthenticatedLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate(ROUTES.login, { replace: true });
  };

  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[16rem_1fr]">
      <aside className="hidden border-r border-slate-200 bg-white lg:flex lg:flex-col">
        <div className="flex items-center gap-2 px-6 py-5">
          <Sparkles className="h-6 w-6 text-brand-600" aria-hidden />
          <span className="font-bold text-slate-900">InterviewAI</span>
        </div>
        <nav className="flex-1 space-y-1 px-3" aria-label="Main navigation">
          {NAV.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive ? "bg-brand-50 text-brand-700" : "text-slate-600 hover:bg-slate-100"
                }`
              }
            >
              <Icon className="h-4 w-4" aria-hidden />
              {label}
            </NavLink>
          ))}
        </nav>
        <button
          onClick={handleLogout}
          className="m-3 flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100"
        >
          <LogOut className="h-4 w-4" aria-hidden />
          Sign out
        </button>
      </aside>

      <div className="flex flex-col">
        <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3">
          <span className="font-semibold text-slate-800 lg:hidden">InterviewAI</span>
          <div className="ml-auto flex items-center gap-3">
            {user?.profile_picture_url ? (
              <img src={user.profile_picture_url} alt="" className="h-8 w-8 rounded-full" />
            ) : (
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-100 text-sm font-semibold text-brand-700">
                {user?.full_name?.charAt(0) ?? "?"}
              </div>
            )}
            <span className="hidden text-sm text-slate-600 sm:block">{user?.full_name}</span>
          </div>
        </header>
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
