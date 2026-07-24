import { useCallback, useEffect, useRef, useState } from "react";

const MUTE_KEY = "aci.tts_muted";

/**
 * Text-to-speech via the browser SpeechSynthesis API (docs/02-tech-stack —
 * "Text-to-Speech: Browser SpeechSynthesis API"). Lets the AI interviewer speak
 * questions aloud, with a voice chosen to match the candidate's preference and
 * a persisted mute toggle.
 */
export function useSpeech() {
  const supported = typeof window !== "undefined" && "speechSynthesis" in window;
  const [speaking, setSpeaking] = useState(false);
  const [muted, setMuted] = useState(() => localStorage.getItem(MUTE_KEY) === "1");
  const voicesRef = useRef<SpeechSynthesisVoice[]>([]);

  useEffect(() => {
    if (!supported) return;
    const load = () => {
      voicesRef.current = window.speechSynthesis.getVoices();
    };
    load();
    window.speechSynthesis.addEventListener("voiceschanged", load);
    return () => {
      window.speechSynthesis.removeEventListener("voiceschanged", load);
      window.speechSynthesis.cancel();
    };
  }, [supported]);

  const pickVoice = useCallback((preference?: string | null): SpeechSynthesisVoice | undefined => {
    const english = voicesRef.current.filter((v) => v.lang.toLowerCase().startsWith("en"));
    const pool = english.length ? english : voicesRef.current;
    if (!pool.length) return undefined;
    if (preference === "female") {
      return pool.find((v) => /female|zira|samantha|susan|aria|jenny|google us/i.test(v.name)) ?? pool[0];
    }
    if (preference === "male") {
      return pool.find((v) => /\bmale\b|david|daniel|george|mark|alex/i.test(v.name)) ?? pool[0];
    }
    return pool[0];
  }, []);

  const speak = useCallback(
    (text: string, preference?: string | null) => {
      if (!supported || muted || !text.trim()) return;
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      const voice = pickVoice(preference);
      if (voice) utterance.voice = voice;
      utterance.rate = 1;
      utterance.pitch = 1;
      utterance.onstart = () => setSpeaking(true);
      utterance.onend = () => setSpeaking(false);
      utterance.onerror = () => setSpeaking(false);
      window.speechSynthesis.speak(utterance);
    },
    [supported, muted, pickVoice],
  );

  const cancel = useCallback(() => {
    if (supported) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
    }
  }, [supported]);

  const toggleMute = useCallback(() => {
    setMuted((prev) => {
      const next = !prev;
      localStorage.setItem(MUTE_KEY, next ? "1" : "0");
      if (next) window.speechSynthesis.cancel();
      return next;
    });
  }, []);

  return { speak, cancel, speaking, muted, toggleMute, supported };
}
