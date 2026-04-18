# Claude Context — House Maintenance Tracker

## Project Overview

- **Status:** In Development
- **Repo:** github.com/Segey-P/house-maintenance-tracker
- **Purpose:** Track home maintenance tasks, intervals, and costs. Surfaces overdue items and logs historical work.
- **Stack:** Streamlit + PostgreSQL (psycopg2)
- **Deploy:** Streamlit Community Cloud

## User Profile

- **Role:** Senior IT Consultant (Banking sector), Canadian (Squamish, BC — Pacific Time)
- **Style:** Direct, precise, no softening. Tables and bullet points.
- **Technical level:** Not a developer — use plain language when explaining options.
- **Workflow:** Cloud-first via Claude Code web. Minimize local machine dependency.

## Before Making Changes

1. Read `TODO.md` — current next actions.
2. Read all files in `specs/` if present.
3. Never commit secrets or credentials.

## AI Agent Rules

1. Push directly to `main`.
2. Prefer editing existing files over creating new ones.
3. No unnecessary dependencies.
4. No comments explaining *what* code does — only *why*.
5. Keep it simple. No premature abstractions.
6. Keep `TODO.md` current and updated throughout the session.
7. Update specs in `specs/` at the end of every session and after any major change in requirements or behaviour.

## TODO.md Convention

`TODO.md` at repo root is the source of truth for what's next.
The Project Hub dashboard reads it automatically. Keep it current and updated throughout the session.

## Database

- PostgreSQL via psycopg2
- Connection string in `st.secrets["DATABASE_URL"]`
- Always use `sslmode=require` for cloud connections
