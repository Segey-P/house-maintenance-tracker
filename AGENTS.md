# Agent Context — House Maintenance Tracker

See `/AI_workspace/AGENTS.md` for workspace-level context. See `specs/` for full module specifications.

## What This Project Is

A home maintenance tracker for a one-bedroom residence. Tracks appliances, maintenance history, scheduled service, and a web UI for CRUD operations. Designed for Canadian context (CAD currency, local regulations where relevant).

## Deployment

Primary target: **Streamlit Community Cloud**, password-protected (same pattern as Project Management Hub). Local dev remains supported.

Data storage in the cloud deployment must tolerate an ephemeral filesystem — do not rely on local disk writes for persistent data.

## Rules

1. Read all files in `specs/` before making changes.
2. Follow spec file naming convention: `[type]-[kebab-topic].md`.
3. Module specs define what should be built — update Status sections only, don't rewrite to match what was built.
