# Agent Context — House Maintenance Tracker

Mirrors `CLAUDE.md` for non-Claude agents.

## What This Project Is

Streamlit app to track home maintenance tasks, intervals, and costs. PostgreSQL backend.

## Rules

1. Read `TODO.md` before starting — source of truth for next actions.
2. Never commit secrets or credentials.
3. Push to `main` directly.
4. `TODO.md` is read by the Project Hub dashboard — keep it current and updated throughout the session.
5. Keep stack minimal: `streamlit`, `psycopg2`, `requests`.
6. Keep it simple. No premature abstractions.
7. Update specs in `specs/` at the end of every session and after any major change in requirements or behaviour.
