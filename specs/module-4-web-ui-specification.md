# Module 4: Web UI Specification

## 1. Objective

Provide a browser-based interface for managing all aspects of the House Maintenance Tracker without requiring CLI access.

## 2. Technology

Streamlit (`app.py`). Run with: `streamlit run app.py`

**Deployment targets:**

| Env | URL pattern | Auth |
|---|---|---|
| Local dev | `http://localhost:8501` | bcrypt password via `st.secrets` (same pattern as Streamlit Cloud) |
| Streamlit Community Cloud (primary) | `https://house-maintenance-tracker.streamlit.app` | bcrypt password via `st.secrets` |

Data lives in a Neon PostgreSQL database (see Module 3). The Streamlit Cloud filesystem is ephemeral, so no local-disk storage is used.

## 3. Navigation

The UI uses a **dark-navy left sidebar** (per `design_handoff/DESIGN.md §2.1`), not top tabs. View state is held in `st.session_state.nav` and defaults to `dashboard`.

**Sidebar layout (top → bottom):**
1. Property switcher placeholder — static "Squamish Home · Squamish, BC" card
2. Nav list: Dashboard · Devices · History · Schedules · Integrations · Roadmap
3. User card + Sign out button (pinned to the footer)

The Dashboard nav item shows an inline red overdue-count badge when one or more schedules are past due.

Shared UI primitives live in `src/ui.py`:

| Helper | Use |
|---|---|
| `status_info(days)` | Returns `{label, status}` for a day delta (overdue / today / soon / upcoming / ok / neutral) |
| `badge_html(status, label)` | Inline pill HTML using the design's status colour system |
| `stat_card_html(label, value, tone)` | Tinted dashboard stat card (tones: `neutral` / `danger` / `warn`) |

## 4. Views

### 4.1 Dashboard

Read-only overview. Refreshes on every load.

| Element | Detail |
| :--- | :--- |
| Metric cards | Active devices, Overdue count, Due This Week, Spent This Year (CAD) |
| Upcoming Tasks | Next 10 schedules within 60 days, status badge colour-coded |
| Recent Activity | Last 8 maintenance log entries |

Wave 2 will replace the metric row with tinted stat cards (danger/warn tones) and the tables with grouped task cards + inline ✓ Done / ⏭ Skip actions.

### 4.2 Devices

Full CRUD for devices. Opening any device launches the `_device_dialog` modal.

| Action | Mechanism |
| :--- | :--- |
| View | Row list, filterable by category; "Show archived" checkbox |
| Add | "＋ Add Device" button → expandable form; on save the device dialog auto-opens so service types can be added immediately |
| Edit | Per-row "Open ↗" → modal with form → Save Changes |
| Service types | Managed inside the device dialog — add / edit / delete, each with name, interval, part numbers, tutorial URL, purchase URL, notes |
| Archive / Restore | Toggle button inside the device dialog — hides device but preserves history |
| Delete | Two-click confirmation via `_delete_dialog` → hard delete with cascade |
| Photo Upload | Reserved for Phase 2 AI identification (not yet implemented) |

### 4.3 History

Full CRUD for maintenance log entries. Entries may optionally link to a service type on the selected device.

| Action | Mechanism |
| :--- | :--- |
| View | Grouped by device in expanders; filterable by device; configurable row limit (10/25/50/100); running total shown |
| Add | "＋ Log Entry" button → expandable form — device, service type, date, task, cost, sourcing, notes |
| Complete Due Task | "Due & Overdue Tasks" banner with inline ✅ Log / ⏭ Skip / ⏸ Pause actions per schedule |
| Edit | Per-entry "Open ↗" → modal with form → Save Changes |
| Delete | From inside the entry modal → two-click confirmation |

### 4.4 Schedules

Full management of maintenance schedules. Schedules are normally created automatically when a service type is added to a device.

| Action | Mechanism |
| :--- | :--- |
| View | Grouped by device in expanders with overdue/due-soon/on-track badges |
| Add | "＋ Add Manual" button (manual schedule without a service type) |
| Edit | Per-row "Open ↗" → modal with form → Save Changes |
| Pause / Resume | Toggled from the per-row modal; paused schedules skipped by calendar push |
| Delete | From inside the schedule modal → two-click confirmation |

### 4.5 Integrations

Triggers for the Google Calendar integration. Previously named "Notifications". Email alerts were removed from scope.

| Element | Detail |
| :--- | :--- |
| Calendar Push | Device filter (all or specific), force re-push toggle, Push button |
| Calendar Status | Live count of linked vs. not-yet-pushed schedules |
| Event payload | Device name, task, due date, frequency, part numbers + tutorial + purchase URLs pulled from the schedule's service type |

### 4.6 Roadmap

Read-only view showing Phase 1 (Now) / Phase 2 (Next) / Phase 3 (Future) feature checklists. Replaces the "Coming Soon" block that previously lived on the Dashboard. Source of truth: `design_handoff/DESIGN.md §7`.

## 5. UX Conventions

- Destructive actions use the `_delete_dialog` modal → two-click confirmation.
- All detail views (log entry / schedule / device) open in `@st.dialog` modals. The design's right-edge slide-over panels are approximated by centred modals under Option A.
- Forms use `st.form` with `clear_on_submit=True` where appropriate so they reset after save.
- `st.rerun()` is called after mutations to reflect updated state immediately.
- Integration imports are lazy (inside button handlers) to avoid startup errors if Google credentials are missing.
- Status badges: `src/ui.py::badge_html` renders the design §2.3 colour system (overdue / today / soon / upcoming / ok / neutral). Legacy emoji fallback (`⛔ 🔴 🟡 🟢`) still used inside dataframes where inline HTML is not supported.
