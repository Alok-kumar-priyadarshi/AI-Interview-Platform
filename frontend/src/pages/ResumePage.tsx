import { useRef, useState } from "react";
import toast from "react-hot-toast";
import { Upload, Trash2, Star, FileText } from "lucide-react";
import { resumeApi } from "@/services/api";
import { useAsync } from "@/hooks/useAsync";
import { ApiError } from "@/services/apiClient";
import { Card, Spinner, ErrorState, EmptyState, Button, Badge } from "@/components/ui";

const ACCEPTED = ".pdf,.docx,.txt";
const MAX_BYTES = 10 * 1024 * 1024;

export function ResumePage() {
  const { data, loading, error, reload } = useAsync(() => resumeApi.list(), []);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    if (file.size > MAX_BYTES) {
      toast.error("Maximum file size is 10 MB.");
      return;
    }
    setUploading(true);
    setProgress(0);
    try {
      await resumeApi.upload(file, setProgress);
      toast.success("Resume uploaded and analyzed.");
      reload();
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const remove = async (id: string) => {
    try {
      await resumeApi.remove(id);
      toast.success("Resume deleted.");
      reload();
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Delete failed.");
    }
  };

  const setDefault = async (id: string) => {
    await resumeApi.setDefault(id);
    reload();
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Resumes</h1>

      <Card>
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED}
          className="sr-only"
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        />
        <div className="flex flex-col items-center gap-3 py-6 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-100">
            <Upload className="h-6 w-6 text-brand-600" aria-hidden />
          </div>
          <p className="font-medium text-slate-800">Upload a resume</p>
          <p className="text-sm text-slate-500">PDF, DOCX, or TXT — up to 10 MB.</p>
          <Button onClick={() => inputRef.current?.click()} loading={uploading}>
            {uploading ? `Uploading ${progress}%` : "Choose file"}
          </Button>
        </div>
      </Card>

      {loading ? (
        <Spinner />
      ) : error ? (
        <ErrorState message={error} onRetry={reload} />
      ) : !data || data.length === 0 ? (
        <EmptyState title="No resumes yet" hint="Upload your first resume to get started." />
      ) : (
        <div className="space-y-3">
          {data.map((resume) => (
            <Card key={resume.id} className="flex items-center gap-4">
              <FileText className="h-6 w-6 shrink-0 text-slate-400" aria-hidden />
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <p className="truncate font-medium text-slate-800">{resume.file_name}</p>
                  {resume.is_default && <Badge tone="blue">Default</Badge>}
                  <Badge tone={resume.status === "completed" ? "green" : resume.status === "failed" ? "red" : "amber"}>
                    {resume.status}
                  </Badge>
                </div>
                <p className="text-xs text-slate-400">
                  Uploaded {new Date(resume.uploaded_at).toLocaleDateString()}
                </p>
              </div>
              {!resume.is_default && (
                <Button variant="ghost" size="sm" onClick={() => setDefault(resume.id)}>
                  <Star className="h-4 w-4" /> Default
                </Button>
              )}
              <Button variant="ghost" size="sm" onClick={() => remove(resume.id)}>
                <Trash2 className="h-4 w-4 text-red-500" />
              </Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
