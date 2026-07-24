# AI Career Interview Platform — Backend

FastAPI backend for the AI Career Interview Platform. Built as a **layered
modular monolith** (API → Service → Repository → Database) per
[`docs/03-architecture/backend-architecture.md`](../docs/03-architecture/backend-architecture.md).

## Stack

| Layer          | Technology                              |
| -------------- | --------------------------------------- |
| Framework      | FastAPI + Uvicorn                       |
| Language       | Python 3.13+ (runs on 3.11+)            |
| Validation     | Pydantic v2 / pydantic-settings         |
| ORM            | SQLAlchemy 2.0 (async) + asyncpg        |
| Migrations     | Alembic                                 |
| Database       | PostgreSQL                              |
| Auth           | Google OAuth 2.0 + JWT                  |
| AI             | Groq (LLM + Whisper)                    |
| Storage        | Local filesystem or S3-compatible (R2)  |

## Project layout

```
backend/
├── app/
│   ├── api/v1/          # Versioned routers (thin; no business logic)
│   ├── core/            # Config, logging, error codes, request context
│   ├── database/        # Declarative base + async session/engine
│   ├── dependencies/    # FastAPI dependency providers
│   ├── exceptions/      # Domain exceptions + centralised handlers
│   ├── middleware/      # Request context / access logging
│   ├── models/          # SQLAlchemy ORM models
│   ├── repositories/    # Persistence layer (CRUD only)
│   ├── schemas/         # Pydantic request/response models
│   ├── services/        # Business logic / orchestration
│   ├── ai/              # Prompts, LLM/RAG/evaluation services (provider-agnostic)
│   ├── auth/            # OAuth + JWT
│   ├── utils/           # Cross-cutting helpers
│   └── main.py          # Application factory + entrypoint
├── tests/               # unit / integration / api
├── alembic/             # Migration environment
└── requirements*.txt
```

## Local development

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv/Scripts/activate            # Windows
# source .venv/bin/activate       # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 3. Configure environment
cp .env.example .env.local        # then fill in real values

# 4. Run the API
uvicorn app.main:app --reload
```

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/api/v1/health

## Testing

Tests run against an in-memory SQLite database (no Postgres or external
credentials required):

```bash
pytest              # run the suite
pytest --cov=app    # with coverage
```

## Conventions

- **Configuration** flows exclusively through `app.core.config.settings`; no
  module reads `os.environ` directly.
- **Errors**: services raise domain exceptions from `app.exceptions`; handlers
  serialise them into the standard envelope. Never raise bare `HTTPException`
  from the service layer.
- **Responses** use the `SuccessResponse` / `ErrorResponse` envelopes in
  `app.schemas.common`.
- Business logic lives **only** in the service layer; repositories never
  contain business rules; the API layer never contains either.

See [`docs/02-tech-stack/coding-standards.md`](../docs/02-tech-stack/coding-standards.md)
for the full standard.
