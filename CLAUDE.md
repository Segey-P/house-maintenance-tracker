# Claude Context — House Maintenance Tracker

## User Profile

- **Role:** Senior IT Consultant (Banking sector), Canadian (Squamish, BC — Pacific Time)
- **Style:** Direct, precise, no softening. Tables and bullet points.
- **Technical level:** Not a developer — use plain language when explaining options.
- **Workflow:** Cloud-first via Claude Code web, mobile access via Claude app.
- **Units:** Metric (cm, kg, °C). Currency: CAD.

## What This Project Is

Home maintenance tracker for a one-bedroom residence. Tracks appliances, maintenance history, scheduled service, and a web UI for CRUD. Canadian context.

## Before Making Changes

1. Read all files in `specs/` — they are authoritative.
2. Read `AGENTS.md` (agent-neutral mirror of this file).

## Deployment

Primary target: **Streamlit Community Cloud**, password-protected (same bcrypt + `st.secrets` pattern as Project Management Hub). Local dev still supported.

Data storage for the cloud deployment must tolerate an ephemeral filesystem — do not rely on local disk writes.

## Rules

- Follow spec file naming: `[type]-[kebab-topic].md`.
- Module specs define what should be built — update Status sections only, don't rewrite to match what was built.
