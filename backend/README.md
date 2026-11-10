# NEXTORA backend foundation

This branch introduces the backend foundation as a separate service. The companion source package is provided as `NEXTORA_Production_MVP_Backend.zip` in the project handoff.

## Stack
- FastAPI API
- PostgreSQL database
- SQLAlchemy ORM
- Argon2 password hashing and short-lived JWT access tokens
- Public/private communities, membership requests, moderator approvals and community posts

## Important deployment boundary
The current Vercel project hosts the static website only. It is not a suitable place to run this persistent FastAPI/PostgreSQL service. The API must be deployed as a separate service and connected to a managed PostgreSQL database. Set the API's `DATABASE_URL`, a unique high-entropy `JWT_SECRET`, `ENVIRONMENT=production`, and the exact website origin in `CORS_ORIGINS` using the hosting provider's secret/environment settings. Never commit secrets.

## Local run
1. Extract the backend source package.
2. Copy `.env.example` to `.env` and replace both secrets.
3. Run `docker compose up --build`.
4. Open `http://localhost:8000/docs` and `http://localhost:8000/health`.

## Current MVP scope
Open registration, login, profiles, follow/block, posts, hybrid/latest/following feed, reactions, comments, search, reports, and initial public/private communities. Community membership endpoints are an initial implementation and require more integration testing and database migrations before public use.

## Before public launch
Email verification, password recovery, refresh-token rotation/revocation, Alembic migrations, admin RBAC, rate limiting/bot protection, moderation operations, privacy/terms, backups/monitoring, media safety, and an independent security/privacy review remain necessary. The hybrid feed is a simple recency/following blend, not a machine-learning recommender. Do not enable public registration until these launch controls are complete.
