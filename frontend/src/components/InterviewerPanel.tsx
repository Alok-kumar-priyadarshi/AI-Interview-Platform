import { Bot, Volume2, VolumeX, RotateCcw } from "lucide-react";

interface InterviewerPanelProps {
  speaking: boolean;
  muted: boolean;
  supported: boolean;
  onReplay: () => void;
  onToggleMute: () => void;
}

/**
 * The "interviewer" persona: an avatar that animates while the question is being
 * spoken, with replay and mute controls. Makes the session feel like a real
 * interviewer talking to the candidate.
 */
export function InterviewerPanel({
  speaking,
  muted,
  supported,
  onReplay,
  onToggleMute,
}: InterviewerPanelProps) {
  return (
    <div className="flex items-center gap-4">
      <div className="relative">
        {speaking && (
          <span className="absolute inset-0 animate-ping rounded-full bg-brand-400 opacity-60" />
        )}
        <div
          className={`relative flex h-14 w-14 items-center justify-center rounded-full ${
            speaking ? "bg-brand-600" : "bg-slate-700"
          }`}
        >
          <Bot className="h-7 w-7 text-white" aria-hidden />
        </div>
      </div>

      <div className="flex-1">
        <p className="font-semibold text-slate-900">AI Interviewer</p>
        <p className="text-sm text-slate-500" aria-live="polite">
          {!supported
            ? "Voice narration is not supported in this browser."
            : muted
              ? "Muted — questions are shown as text."
              : speaking
                ? "Speaking…"
                : "Ready"}
        </p>
      </div>

      {supported && (
        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={onReplay}
            disabled={muted}
            className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 disabled:opacity-40"
            title="Replay question"
            aria-label="Replay question"
          >
            <RotateCcw className="h-5 w-5" />
          </button>
          <button
            type="button"
            onClick={onToggleMute}
            className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"
            title={muted ? "Unmute" : "Mute"}
            aria-label={muted ? "Unmute interviewer" : "Mute interviewer"}
          >
            {muted ? <VolumeX className="h-5 w-5" /> : <Volume2 className="h-5 w-5" />}
          </button>
        </div>
      )}
    </div>
  );
}
