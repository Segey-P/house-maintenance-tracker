# House Maintenance Tracker — TODO

## In Progress

UI redesign from `design_handoff/` — see DESIGN.md for full spec.

### Wave 0 — Drop-ins (done in this session)
- [x] Theme tokens in `.streamlit/config.toml` (amber primary, warm off-white bg)
- [x] DM Sans font + redesigned global CSS (cards, metrics, buttons, tabs)
- [x] Rename tabs: Maintenance → History, Notifications → Integrations
- [x] Remove "Coming Soon" block from Dashboard (moves to Roadmap view in Wave 5)
- [x] Fix Google Calendar push crash (`dev.part_numbers` / `dev.resource_links` no longer exist on Device; pull from service type instead)

## Next Up

Stack decision: **Option A** — Streamlit + `@st.dialog` modals (~80% visual parity). Archive feature stays in DB + UI (design's removal treated as a design error). Anthropic API approved for Wave 5.

### Wave 1 — Sidebar nav + shell (done)
- [x] Replace `st.tabs` with sidebar-driven view picker (dark navy sidebar per design)
- [x] `src/ui.py` with `status_info`, `badge_html`, `stat_card_html` helpers
- [x] User profile + Sign out in sidebar footer
- [x] Property switcher placeholder (static Squamish Home)
- [x] Roadmap view stub (Phase 1/2/3 from DESIGN.md)

### Wave 2 — Dashboard refactor (done)
- [x] 4-card tinted stat row (Overdue red, Due-this-week amber)
- [x] Task groups (Needs Attention / Due This Week / Later This Month)
- [x] Inline ✓ Done + ⏭ Skip + ⏸ Pause with expand-below quick-log form
- [x] Recent Activity as card list (5 entries)

### Wave 3 — Devices redesign (done)
- [x] Card grid (3-col `st.columns` — Streamlit can't emit true CSS auto-fill)
- [x] Accent strip + status badge + category pill + warranty-expiring badge
- [x] Device dialog: 4-col specs row + 4-col metrics row, amber notes block
- [x] Nested service type cards retained (cleanup deferred if needed)
- [x] Inline delete confirmation (replaces `_delete_dialog` modal for device)
- [x] Category spend on device cards (Total + YTD)
- [ ] Dashed "+ Add Device" tile — deferred to Wave 6 (needs custom component)
- Archive: keeps working in DB + UI (design's removal = design error)

### Wave 4 — History + Schedules refactor (done)
- [x] History: flat card list, date/category/from-to filters, amber due-tasks banner with chip row
- [x] Schedules: urgency-grouped (Overdue / This Week / This Month / Later + Paused) with 🗓 Synced badge
- [x] Inline Pause/Resume on schedule rows (new `activate_schedule` helper in scheduler.py)

### Wave 5 — AI + Integrations + Roadmap (parked — needs more scoping)
User flagged: think through these features in more detail before implementing. Re-open when the product spec for each is clearer.
- [ ] Add `anthropic` to `requirements.txt`; `ANTHROPIC_API_KEY` in Streamlit secrets
- [ ] `src/ai.py` wrapper (Claude Haiku 4.5 default; enable prompt caching on chat system context)
- [ ] Find Parts + Find Tutorial buttons on each service type card — open questions: how specific can Haiku be on Canadian part SKUs? do we surface Amazon.ca referral links?
- [ ] Dashboard AI Chat widget (context: devices, overdue, due-this-week) — open questions: context window budget, cache strategy, how chatty is useful vs. noise
- [ ] Integrations: Connect/Disconnect pill + Synced/Unsynced tile counts
- [ ] Account card (email — needs storage decision)
- [ ] Roadmap view full polish (Phase 1/2/3 checklist from DESIGN.md — stub is live)

### Wave 6 — Stretch
- [ ] Custom slide-over panel component (true right-edge drawer)
- [ ] Photo upload on Add Device (needs storage; Streamlit Cloud fs is ephemeral)
- [x] Download schedule as CSV/PDF checklist (CSV ⬇ button in Schedules header)

### Known UI gaps (live app)
- [ ] **Browser-test every wave.** The fixes so far have all been pushed without a live browser verification (sandbox has no Streamlit). This already bit us twice with the sidebar/header CSS. Before merging the next wave, run `streamlit run app.py` somewhere with a browser.

## Backlog

- [ ] Google Calendar integration — store OAuth token in Streamlit secrets for cloud use. Maybe transition to individual reminders instead
- [ ] Gemini CSV import — structured CSV format that Gemini can produce from a camera walkthrough, importable via the UI (devices + service types in one file). See `scripts/seed_data.sql` as schema reference.
- [ ] IoT device detection integration
- [ ] Auto-order replacement parts from Amazon when service is due
- [ ] Unified `tasks` table (schedules + history combined) — v2 backend change

## Done

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
