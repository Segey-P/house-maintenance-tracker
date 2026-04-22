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
| Stat row | Active devices · Overdue (danger tint) · Due This Week (warn tint) · Spent This Year (CAD) |
| Task groups | Needs Attention (overdue + today) · Due This Week (1–7d) · Later This Month (8–30d) — each card has inline ✓ Done / ⏭ Skip / ⏸ Pause; ✓ Done expands a quick-log form that writes the log and advances the schedule atomically |
| Recent Activity | Last 5 log entries as bordered cards (date, device, task, cost) |

### 4.2 Devices

Full CRUD for devices. Opening any device launches the `_device_dialog` modal.

| Action | Mechanism |
| :--- | :--- |
| View | 3-column card grid. Each card: status-coloured accent strip, name + model, category/status/warranty pills, Total + YTD spend, Open ↗ |
| Filter | Category filter + "Show archived" checkbox |
| Add | "＋ Add Device" button → expandable form; on save the device dialog auto-opens so service types can be added immediately |
| Edit | Per-card "Open ↗" → modal with 4-col specs grid + 4-col metrics grid + amber notes block; edit form in a collapsed expander |
| Service types | Managed inside the device dialog — add / edit / delete, each with name, interval, part numbers, tutorial URL, purchase URL, notes |
| Archive / Restore | Toggle button inside the device dialog — hides device but preserves history |
| Delete | Inline two-click confirmation inside the device dialog (replaces `_delete_dialog` for devices); `_delete_dialog` retained for logs + schedules |
| Photo Upload | Reserved for Phase 2 AI identification (not yet implemented — needs ephemeral-safe storage) |

### 4.3 History

Full CRUD for maintenance log entries. Entries may optionally link to a service type on the selected device.

| Action | Mechanism |
| :--- | :--- |
| View | Flat bordered-card list (date · device · task · cost · service-type), sorted by completion date |
| Filter bar | Device · Category · Date From · Date To · Limit (10/25/50/100). Category resolved through device lookup. Filtered Entries + Spend totals pinned to the right |
| Due Tasks banner | Compact amber chip row (3-wide) above the list; clicking a chip prefills the log form and opens it |
| Add | "＋ Log Entry" button → expandable form — device, service type, date, task, cost, sourcing, notes |
| Edit | Per-entry "Open ↗" → modal with form → Save Changes |
| Delete | From inside the entry modal → two-click confirmation |

### 4.4 Schedules

Full management of maintenance schedules. Schedules are normally created automatically when a service type is added to a device.

| Action | Mechanism |
| :--- | :--- |
| View | Urgency-grouped cards: Overdue · This Week · This Month · Later · Paused. Each card shows device + task + frequency + next-due metadata with a status badge and `🗓 Synced` pill when pushed |
| Add | "＋ Add Manual" button (manual schedule without a service type) |
| Pause / Resume | Inline ⏸ Pause / ▶ Resume button on every row; paused schedules skipped by calendar push |
| Edit | Per-row "Open ↗" → modal with form → Save Changes |
| Delete | From inside the schedule modal → two-click confirmation |
| Export | ⬇ CSV button in the view header — downloads all schedules (active + paused) sorted by next due date |

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
