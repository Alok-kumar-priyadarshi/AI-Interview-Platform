# Conversational Interview Experience

**Document ID:** ARC-011

**Version:** 1.0.0

**Status:** Approved

**Priority:** High

**Last Updated:** 2026-07-24

---

# Purpose

This document specifies the **conversational interview experience** — the core
product interaction in which an AI interviewer *speaks* each question aloud
while it is displayed on screen, and the candidate answers by **voice or text**,
switchable at any point.

It complements:

- `ai-architecture.md` (question generation, evaluation)
- `frontend-architecture.md` (Voice Interview Flow)
- `../02-tech-stack/technology-overview.md` (TTS = Browser SpeechSynthesis,
  STT = Groq Whisper)

---

# Experience Overview

```text
Start interview
      ↓
Interviewer greets the candidate (spoken)
      ↓
For each question:
    Question is DISPLAYED  +  SPOKEN aloud (Text-to-Speech)
      ↓
    Candidate answers  →  Type (text)  OR  Speak (record → transcribe)
      ↓
    Answer submitted → next question
      ↓
Complete → evaluation + report
```

The session should feel like a real interviewer talking to the candidate, not a
form to fill in.

---

# Text-to-Speech (Interviewer Voice)

- Implemented client-side with the **browser SpeechSynthesis API** — no server
  round trip, no audio storage, works offline in the browser.
- The interviewer **greets** the candidate once at the start, then reads each
  question ("Question N. …").
- **Voice selection** honours the candidate's `preferred_interviewer_voice`
  (male/female) from the candidate profile / interview configuration, resolved
  to the closest available system voice.
- Controls: **Replay** (re-read the current question) and **Mute** (persisted).
  When narration is unsupported or muted, the question remains fully usable as
  text (accessibility requirement).
- Narration is cancelled automatically when the candidate starts typing or
  recording, so the interviewer never talks over the candidate.

No backend change is required for narration — the question text returned by
`GET /interviews/{id}/questions/current` is spoken directly.

---

# Dual-Mode Answering

Both answer modes are available for **every** question, regardless of the
interview's configured mode (the configured mode only sets the default):

## Text

- `POST /interviews/{id}/answers` with `{ question_id, answer }`.

## Voice

- The browser records audio via **MediaRecorder**.
- `POST /interviews/{id}/answers/voice` (multipart: `question_id`, `audio`).
- The backend stores the audio and transcribes it with **Groq Whisper**
  (`GROQ_TRANSCRIPTION_MODEL`), persisting the transcript on the answer.
- `GET /interviews/{id}/answers/{answer_id}/transcript` returns the transcript.

Evaluation consumes the text answer or the transcription transparently, so voice
and text answers are scored identically.

---

# Sequencing & Rules

- Exactly one active question at a time; answered in order.
- One answer per question (Version 1).
- Server remains the source of truth for progression and timing.

---

# Accessibility

- Narration is an enhancement, never a requirement — every question is legible
  as text and every control is keyboard-reachable and screen-reader labelled.
- A mute control is always available and its state persists.

---

# Future Enhancements

- Streaming/low-latency neural TTS (server-side) for a more natural voice.
- Real-time partial transcription while the candidate speaks.
- Adaptive follow-up questions based on the spoken answer.
- Interviewer persona/expressions and barge-in (interrupt) support.

---

# Related Documents

- `ai-architecture.md`
- `frontend-architecture.md`
- `../05-api-design/answers.md`
- `../05-api-design/questions.md`

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-24 | Initial conversational interview experience specification |
