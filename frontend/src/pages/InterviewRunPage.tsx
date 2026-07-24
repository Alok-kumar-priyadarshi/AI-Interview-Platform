import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import toast from "react-hot-toast";
import { CheckCircle2, Play, Keyboard, Mic } from "lucide-react";
import { interviewApi, reportApi } from "@/services/api";
import { ApiError } from "@/services/apiClient";
import { Card, Spinner, ErrorState, Button, Badge } from "@/components/ui";
import { VoiceRecorder } from "@/components/VoiceRecorder";
import { InterviewerPanel } from "@/components/InterviewerPanel";
import { useSpeech } from "@/hooks/useSpeech";
import { ROUTES } from "@/constants/routes";
import type { CurrentQuestion, InterviewSummary } from "@/types/api";

type Phase = "loading" | "ready" | "question" | "finished" | "error";
type AnswerMode = "text" | "voice";

const GREETING = "Hello! I'm your AI interviewer. Let's begin.";

export function InterviewRunPage() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const speech = useSpeech();

  const [phase, setPhase] = useState<Phase>("loading");
  const [interview, setInterview] = useState<InterviewSummary | null>(null);
  const [question, setQuestion] = useState<CurrentQuestion | null>(null);
  const [answer, setAnswer] = useState("");
  const [answerMode, setAnswerMode] = useState<AnswerMode>("text");
  const [busy, setBusy] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const greeted = useRef(false);

  const speakQuestion = useCallback(
    (q: CurrentQuestion, withGreeting: boolean) => {
      const prefix = withGreeting ? `${GREETING} ` : "";
      speech.speak(`${prefix}Question ${q.sequence}. ${q.question}`, interview?.interviewer_voice);
    },
    [speech, interview?.interviewer_voice],
  );

  const loadCurrent = useCallback(async () => {
    try {
      const q = await interviewApi.currentQuestion(id);
      setQuestion(q);
      setAnswer("");
      setPhase("question");
    } catch {
      setPhase("finished");
    }
  }, [id]);

  const init = useCallback(async () => {
    try {
      const iv = await interviewApi.get(id);
      setInterview(iv);
      setAnswerMode(iv.mode === "voice" ? "voice" : "text");
      if (iv.status === "completed") {
        navigate(ROUTES.report(id), { replace: true });
      } else if (iv.status === "in_progress") {
        await loadCurrent();
      } else if (iv.status === "ready" || iv.status === "created") {
        setPhase("ready");
      } else {
        setErrorMsg(`This interview is ${iv.status} and cannot be run.`);
        setPhase("error");
      }
    } catch (err) {
      setErrorMsg(err instanceof ApiError ? err.message : "Failed to load interview.");
      setPhase("error");
    }
  }, [id, navigate, loadCurrent]);

  useEffect(() => {
    void init();
  }, [init]);

  // Speak each new question aloud (greeting once, on the first question).
  useEffect(() => {
    if (phase === "question" && question) {
      const withGreeting = !greeted.current && question.sequence === 1;
      greeted.current = true;
      speakQuestion(question, withGreeting);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [question, phase]);

  const start = async () => {
    setBusy(true);
    try {
      await interviewApi.start(id);
      await loadCurrent();
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not start.");
    } finally {
      setBusy(false);
    }
  };

  const submitText = async () => {
    if (!question || answer.trim().length === 0) return;
    setBusy(true);
    try {
      await interviewApi.submitAnswer(id, question.question_id, answer.trim());
      await loadCurrent();
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not submit answer.");
    } finally {
      setBusy(false);
    }
  };

  const submitVoice = async (audio: Blob) => {
    if (!question) return;
    try {
      await interviewApi.submitVoiceAnswer(id, question.question_id, audio);
      toast.success("Answer transcribed.");
      await loadCurrent();
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not submit voice answer.");
    }
  };

  const finish = async () => {
    setBusy(true);
    speech.cancel();
    try {
      await interviewApi.complete(id);
      toast.success("Interview completed. Generating your report…");
      const ref = await reportApi.forInterview(id);
      navigate(ROUTES.report(ref.report_id));
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Could not complete.");
      setBusy(false);
    }
  };

  const switchMode = (mode: AnswerMode) => {
    speech.cancel(); // don't talk over the candidate
    setAnswerMode(mode);
  };

  if (phase === "loading") return <Spinner label="Loading interview…" />;
  if (phase === "error") return <ErrorState message={errorMsg} onRetry={init} />;

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">{interview?.title}</h1>
        <p className="text-sm text-slate-500">
          {interview?.difficulty} · {interview?.total_questions} questions
        </p>
      </div>

      {phase === "ready" && (
        <Card className="space-y-4 text-center">
          <p className="text-slate-600">
            Your interviewer is ready. Questions are read aloud — make sure your sound is on.
          </p>
          <Button onClick={start} loading={busy}>
            <Play className="h-4 w-4" /> Start interview
          </Button>
        </Card>
      )}

      {phase === "question" && question && (
        <Card className="space-y-5">
          <InterviewerPanel
            speaking={speech.speaking}
            muted={speech.muted}
            supported={speech.supported}
            onReplay={() => speakQuestion(question, false)}
            onToggleMute={speech.toggleMute}
          />

          <div className="rounded-lg bg-slate-50 p-4">
            <div className="mb-2 flex flex-wrap items-center gap-2">
              <Badge tone="blue">Question {question.sequence}</Badge>
              <Badge>{question.category}</Badge>
              <Badge tone="amber">{question.difficulty}</Badge>
            </div>
            <p className="text-lg font-medium text-slate-900">{question.question}</p>
          </div>

          {/* Answer mode toggle — both voice and text are always available. */}
          <div className="inline-flex rounded-lg border border-slate-200 p-1">
            <ModeButton
              active={answerMode === "text"}
              onClick={() => switchMode("text")}
              icon={<Keyboard className="h-4 w-4" />}
              label="Type"
            />
            <ModeButton
              active={answerMode === "voice"}
              onClick={() => switchMode("voice")}
              icon={<Mic className="h-4 w-4" />}
              label="Speak"
            />
          </div>

          {answerMode === "text" ? (
            <div className="space-y-3">
              <textarea
                className="input min-h-[10rem]"
                placeholder="Type your answer…"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                onFocus={() => speech.cancel()}
                aria-label="Your answer"
              />
              <div className="flex justify-end">
                <Button onClick={submitText} loading={busy} disabled={answer.trim().length === 0}>
                  Submit answer
                </Button>
              </div>
            </div>
          ) : (
            <VoiceRecorder onSubmit={submitVoice} onStart={speech.cancel} disabled={busy} />
          )}
        </Card>
      )}

      {phase === "finished" && (
        <Card className="text-center">
          <CheckCircle2 className="mx-auto mb-3 h-10 w-10 text-green-500" aria-hidden />
          <p className="mb-4 text-slate-700">You've answered all questions.</p>
          <Button onClick={finish} loading={busy}>
            Complete &amp; view report
          </Button>
        </Card>
      )}
    </div>
  );
}

function ModeButton({
  active,
  onClick,
  icon,
  label,
}: {
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`inline-flex items-center gap-2 rounded-md px-4 py-1.5 text-sm font-medium transition-colors ${
        active ? "bg-brand-600 text-white" : "text-slate-600 hover:bg-slate-100"
      }`}
      aria-pressed={active}
    >
      {icon}
      {label}
    </button>
  );
}
