# House Maintenance Tracker — TODO

## Critical Path — Next Wave

- [ ] **Bug Fix (App Access):** Diagnose why web UI cannot be opened in incognito windows
- [ ] **Bug Fix (Refresh Loop):** Fix project details page refresh-loop issue
- [ ] **Storage Decision:** Decide on durable storage for photo uploads (S3 vs. Neon BYTEA)
- [ ] **AI Scoping:** Detail `src/ai.py` wrapper and prompt caching strategy
- [ ] **Cross-Browser Testing:** Manual CSS testing on Streamlit Cloud (Chrome, Safari, Firefox)

## In Progress

- [ ] Roadmap view checklist in `src/ui.py` — see DESIGN.md phases

## Parked — Awaiting Decisions

| Item | Blocker | Revisit |
|------|---------|---------|
| Wave 5 AI + Integrations | Storage decision + scoping of Canadian part SKU lookup | After storage decided |
| "+ Add Device" tile | Needs custom Streamlit component | Phase 2 |
| Photo upload | Depends on storage decision | After storage decided |
| Slide-over panel | Needs custom component or design revision | Phase 2 |

## Backlog — Future Phases

- [ ] Google Calendar integration (OAuth token in secrets)
- [ ] Gemini CSV import for bulk device entry
- [ ] IoT device detection integration
- [ ] Auto-order replacement parts from Amazon
- [ ] Unified `tasks` table (v2 backend refactor)
