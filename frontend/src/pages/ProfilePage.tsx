import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import client, { ApiError, unwrap } from "@/services/apiClient";
import { userApi } from "@/services/api";
import { useAuth } from "@/contexts/AuthContext";
import { Card, Button, Spinner } from "@/components/ui";

interface Preferences {
  target_role: string;
  experience_years: number | null;
  expected_salary_min: number | null;
  expected_salary_max: number | null;
  preferred_interview_type: string;
}

const prefsApi = {
  get: () => unwrap<Preferences>(client.get("/candidate-profile")),
  create: (p: Partial<Preferences>) => unwrap<Preferences>(client.post("/candidate-profile", p)),
  update: (p: Partial<Preferences>) => unwrap<Preferences>(client.patch("/candidate-profile", p)),
};

export function ProfilePage() {
  const { user, refresh } = useAuth();
  const [fullName, setFullName] = useState(user?.full_name ?? "");
  const [savingName, setSavingName] = useState(false);

  const [hasPrefs, setHasPrefs] = useState(false);
  const [loadingPrefs, setLoadingPrefs] = useState(true);
  const [targetRole, setTargetRole] = useState("");
  const [experience, setExperience] = useState("");
  const [savingPrefs, setSavingPrefs] = useState(false);

  useEffect(() => {
    prefsApi
      .get()
      .then((p) => {
        setHasPrefs(true);
        setTargetRole(p.target_role);
        setExperience(p.experience_years?.toString() ?? "");
      })
      .catch(() => setHasPrefs(false))
      .finally(() => setLoadingPrefs(false));
  }, []);

  const saveName = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingName(true);
    try {
      await userApi.updateProfile(fullName);
      await refresh();
      toast.success("Profile updated.");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Update failed.");
    } finally {
      setSavingName(false);
    }
  };

  const savePrefs = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingPrefs(true);
    const payload: Partial<Preferences> = {
      target_role: targetRole,
      experience_years: experience ? Number(experience) : null,
    };
    try {
      if (hasPrefs) await prefsApi.update(payload);
      else await prefsApi.create(payload);
      setHasPrefs(true);
      toast.success("Preferences saved.");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Save failed.");
    } finally {
      setSavingPrefs(false);
    }
  };

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Profile</h1>

      <Card>
        <h2 className="mb-4 font-semibold text-slate-900">Account</h2>
        <form onSubmit={saveName} className="space-y-4">
          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">Email</span>
            <input className="input bg-slate-50" value={user?.email ?? ""} disabled />
          </label>
          <label className="block">
            <span className="mb-1 block text-sm font-medium text-slate-700">Full name</span>
            <input
              className="input"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              minLength={2}
              required
            />
          </label>
          <Button type="submit" loading={savingName}>
            Save
          </Button>
        </form>
      </Card>

      <Card>
        <h2 className="mb-4 font-semibold text-slate-900">Career preferences</h2>
        {loadingPrefs ? (
          <Spinner />
        ) : (
          <form onSubmit={savePrefs} className="space-y-4">
            <label className="block">
              <span className="mb-1 block text-sm font-medium text-slate-700">Target role</span>
              <input
                className="input"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                minLength={2}
                maxLength={100}
                required
                placeholder="e.g. Backend Developer"
              />
            </label>
            <label className="block">
              <span className="mb-1 block text-sm font-medium text-slate-700">Years of experience</span>
              <input
                type="number"
                min={0}
                max={50}
                className="input"
                value={experience}
                onChange={(e) => setExperience(e.target.value)}
              />
            </label>
            <Button type="submit" loading={savingPrefs}>
              {hasPrefs ? "Update preferences" : "Create preferences"}
            </Button>
          </form>
        )}
      </Card>
    </div>
  );
}
