# House Maintenance Tracker — TODO

## Top 10 Prioritized Tasks
- [ ] **Bug Fix (App Access):** Diagnose why the web UI cannot be opened in incognito windows
- [ ] **Bug Fix (Project Details):** Fix project details page refresh-loop issue
- [ ] **Cross-Browser Testing:** Perform full manual testing of CSS on Streamlit Cloud
- [ ] **AI Scoping:** Detail the `src/ai.py` wrapper and prompt caching strategy
- [ ] **Integration Scoping:** Define the specific Canadian part SKU logic for AI lookup
- [ ] **Integrations UI:** Implement Connect/Disconnect pills for scheduled tasks
- [ ] **Schedules UI:** Finalize the roadmap view checklist in `src/ui.py`
- [ ] **Storage Decision:** Decide on durable storage for photo uploads (S3 vs. Neon BYTEA)
- [ ] **UI Component:** Build dashed "+ Add Device" tile for the device grid
- [ ] **Refactor Backend:** Plan unified `tasks` table (schedules + history combined)

---

## Future Considerations

### Wave 5 — AI + Integrations polish (parked — needs more scoping)
User flagged: think through these features in more detail before implementing. Re-open when the product spec for each is clearer.
- [ ] Add `anthropic` to `requirements.txt`; `ANTHROPIC_API_KEY` in Streamlit secrets
- [ ] `src/ai.py` wrapper (Claude Haiku 4.5 default; enable prompt caching on chat system context)
- [ ] Find Parts + Find Tutorial buttons on each service type card — open questions: how specific can Haiku be on Canadian part SKUs? do we surface Amazon.ca referral links?
- [ ] Dashboard AI Chat widget (context: devices, overdue, due-this-week) — open questions: context window budget, cache strategy, how chatty is useful vs. noise
- [ ] Integrations: Connect/Disconnect pill + Synced/Unsynced tile counts
- [ ] Account card (email — needs storage decision)
- [ ] Roadmap view full polish (Phase 1/2/3 checklist from DESIGN.md — stub is live)

### Wave 6 — Stretch (parked — needs custom component or storage decision)
- [ ] Dashed "+ Add Device" tile on the device grid (needs custom Streamlit component — `st.columns` can't emit CSS auto-fill)
- [ ] Custom slide-over panel component (true right-edge drawer — design §2.5; currently approximated by `@st.dialog` modals)
- [ ] Photo upload on Add Device — needs durable storage; Streamlit Cloud filesystem is ephemeral. Potential approach: S3-compatible bucket or Neon BYTEA. Ties into Phase 2 AI visual identification.

### Known UI gaps (live app)
- [ ] **Browser-test every wave.** Sandbox has no Streamlit, so CSS fixes have shipped without live browser verification (this bit us twice on the sidebar/header CSS). Before merging any future wave, run `streamlit run app.py` somewhere with a browser.

## Backlog

- [ ] Google Calendar integration — store OAuth token in Streamlit secrets for cloud use. Maybe transition to individual reminders instead
- [ ] Gemini CSV import — structured CSV format that Gemini can produce from a camera walkthrough, importable via the UI (devices + service types in one file). See `scripts/seed_data.sql` as schema reference.
- [ ] IoT device detection integration
- [ ] Auto-order replacement parts from Amazon when service is due
- [ ] Unified `tasks` table (schedules + history combined) — v2 backend change
