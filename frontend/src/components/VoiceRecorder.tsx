import { useRef, useState } from "react";
import { Mic, Square, RotateCcw } from "lucide-react";
import toast from "react-hot-toast";
import { Button } from "@/components/ui";

interface VoiceRecorderProps {
  onSubmit: (audio: Blob) => Promise<void>;
  onStart?: () => void;
  disabled?: boolean;
}

/** Records a spoken answer via MediaRecorder and submits the resulting blob. */
export function VoiceRecorder({ onSubmit, onStart, disabled }: VoiceRecorderProps) {
  const [recording, setRecording] = useState(false);
  const [blob, setBlob] = useState<Blob | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const start = async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      toast.error("Recording is not supported in this browser.");
      return;
    }
    onStart?.(); // stop the interviewer talking over the candidate
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorder.ondataavailable = (e) => e.data.size > 0 && chunksRef.current.push(e.data);
      recorder.onstop = () => {
        setBlob(new Blob(chunksRef.current, { type: "audio/webm" }));
        stream.getTracks().forEach((t) => t.stop());
      };
      recorder.start();
      recorderRef.current = recorder;
      setRecording(true);
      setBlob(null);
    } catch {
      toast.error("Microphone permission denied.");
    }
  };

  const stop = () => {
    recorderRef.current?.stop();
    setRecording(false);
  };

  const submit = async () => {
    if (!blob) return;
    setSubmitting(true);
    try {
      await onSubmit(blob);
      setBlob(null);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4 rounded-lg border border-dashed border-slate-300 p-6">
      {recording ? (
        <Button variant="danger" onClick={stop}>
          <Square className="h-4 w-4" /> Stop recording
        </Button>
      ) : blob ? (
        <div className="flex flex-col items-center gap-3">
          <audio controls src={URL.createObjectURL(blob)} className="w-full" />
          <div className="flex gap-2">
            <Button variant="ghost" onClick={start} disabled={submitting}>
              <RotateCcw className="h-4 w-4" /> Re-record
            </Button>
            <Button onClick={submit} loading={submitting}>
              Submit answer
            </Button>
          </div>
        </div>
      ) : (
        <Button onClick={start} disabled={disabled}>
          <Mic className="h-4 w-4" /> Start recording
        </Button>
      )}
      {recording && (
        <p className="flex items-center gap-2 text-sm text-red-500">
          <span className="h-2 w-2 animate-pulse rounded-full bg-red-500" /> Recording…
        </p>
      )}
    </div>
  );
}
