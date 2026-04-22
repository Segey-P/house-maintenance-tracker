# House Maintenance Tracker — TODO

## Next Up

Nothing active — the UI redesign (Waves 0–4) is merged and the Schedules CSV export shipped on top. Next direction TBD by user: either re-scope Wave 5 (AI features) or pick from the Future Considerations below.

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

## Done

### UI redesign (Option A — Streamlit + `@st.dialog` modals, ~80% visual parity vs `design_handoff/`)
- [x] Wave 0 — theme tokens, DM Sans, global CSS, tab rename (Maintenance→History, Notifications→Integrations), Google Calendar push crash fix
- [x] Wave 1 — sidebar nav shell (dark navy, nav list, property switcher placeholder, user footer), `src/ui.py` helpers, Roadmap view stub
- [x] Wave 2 — Dashboard tinted stat row + task groups (Needs Attention / Due This Week / Later This Month) + inline ✓ Done/⏭ Skip/⏸ Pause + quick-log form, Recent Activity card list
- [x] Wave 3 — Devices 3-col card grid, device dialog (4-col specs + 4-col metrics + amber notes), inline delete confirmation, category spend on cards
- [x] Wave 4 — History flat card list with filter bar + chip banner; Schedules urgency-grouped cards (Overdue/This Week/This Month/Later/Paused) with 🗓 Synced badge + inline Pause/Resume (`activate_schedule` helper)
- [x] Hotfix — header collapse + amber `stExpandSidebarButton` pill (playwright-verified against Streamlit 1.56)
- [x] Schedules ⬇ CSV export button in view header

### Platform + data model
- [x] Provision Neon PostgreSQL database
- [x] Deploy to Streamlit Community Cloud (`house-maintenance-tracker.streamlit.app`)
- [x] Add database credentials and password hash to Streamlit secrets
- [x] Build core UI: Dashboard, Devices, Maintenance, Schedules, Notifications tabs
- [x] Service types data model: new schema, CRUD module, updated schedules and maintenance_log
- [x] Service types UI: list, add, edit, delete inside device dialog
- [x] Fix Device add/edit TypeError (removed part_numbers, maintenance_frequency_days, resource_links from Device model)
- [x] Re-enable password gate (`require_password()` active in app.py)
- [x] Remove email alerts feature (dropped from backlog and Coming Soon)
- [x] Add Kitchen Appliances category
- [x] Household seed SQL created (`scripts/seed_data.sql`) — 15 devices, 27 service types
- [x] seed_data.py updated to current schema (no crash)
