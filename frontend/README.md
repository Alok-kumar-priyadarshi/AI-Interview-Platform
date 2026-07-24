# AI Career Interview Platform — Frontend

React + Vite + TypeScript + Tailwind SPA for the AI Career Interview Platform,
built against the FastAPI backend (`/api/v1`).

## Stack

| Concern     | Choice                                    |
| ----------- | ----------------------------------------- |
| Framework   | React 19 + Vite                           |
| Language    | TypeScript (strict)                       |
| Styling     | Tailwind CSS                              |
| Routing     | React Router 7                            |
| HTTP        | Axios (centralised client + interceptors) |
| State       | React Context (auth)                      |
| Icons       | lucide-react                              |
| Toasts      | react-hot-toast                           |

## Structure

```
src/
├── components/     # Reusable UI (Button, Card, Spinner, states, Badge) + ProtectedRoute
├── contexts/       # AuthContext (session, useAuth)
├── hooks/          # useAsync (loading/error data fetching)
├── layouts/        # AuthenticatedLayout (nav shell)
├── pages/          # Route components (Login, Dashboard, Resume, Interview, Report, …)
├── routes/         # AppRouter
├── services/       # apiClient (axios + token refresh), tokenStore, typed api.ts
├── types/          # Shared API types
├── constants/      # routes
└── styles/         # Tailwind entry
```

## Auth flow (Google OAuth)

1. Login page links to the backend `GET /auth/google/login` (full-page nav; the
   backend sets a signed `oauth_state` cookie and redirects to Google).
2. Google redirects to `/auth/callback?code&state` on the frontend.
3. `AuthCallbackPage` forwards `code`+`state` to the backend callback (the state
   cookie is sent automatically), receives the JWT pair, stores it, and enters
   the app.
4. `apiClient` attaches the access token and transparently refreshes it once on
   `401` using the refresh token.

## Local development

```bash
npm install
cp .env.example .env.local      # set VITE_API_BASE_URL to your backend
npm run dev                     # http://localhost:5173
npm run build                   # typecheck + production build
```

The backend must allow the dev origin in `CORS_ALLOWED_ORIGINS` and use
`GOOGLE_REDIRECT_URI=http://localhost:5173/auth/callback`.
