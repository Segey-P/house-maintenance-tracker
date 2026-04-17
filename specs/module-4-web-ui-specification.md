# Module 4: Web UI Specification

## 1. Objective

Provide a browser-based interface for managing all aspects of the House Maintenance Tracker without requiring CLI access.

## 2. Technology

Streamlit (`app.py`). Run with: `streamlit run app.py`

**Deployment targets:**

| Env | URL pattern | Auth |
|---|---|---|
| Local dev | `http://localhost:8501` | None |
| Streamlit Community Cloud (primary) | `https://<app>.streamlit.app` | bcrypt password via `st.secrets` (same pattern as Project Hub) |

Data storage for the cloud deployment must be compatible with an ephemeral filesystem: use a persisted backend (SQLite in a GitHub-committed file, or a free-tier hosted database like Turso/Supabase) rather than relying on local disk writes.

## 3. Tab Structure

### 3.1 Dashboard

Read-only overview. Refreshes on every load.

| Element | Detail |
| :--- | :--- |
| Metric cards | Active devices, Overdue count, Due This Week, Total Spend (CAD) |
| Upcoming Tasks | Next 10 schedules within 60 days, status badge colour-coded |
| Recent Activity | Last 8 maintenance log entries |

### 3.2 Inventory

Full CRUD for devices.

| Action | Mechanism |
| :--- | :--- |
| View | Filterable table (by category, archived flag) |
| Add | Expandable form — all device fields |
| Edit | Selectbox → pre-populated form → Save Changes |
| Archive | Toggle button — hides device but preserves history |
| Delete | Two-click confirmation → hard delete with cascade |
| Photo Upload | Disabled placeholder; reserved for Phase 2 AI identification |

### 3.3 History / Expenses

Full CRUD for maintenance log entries.

| Action | Mechanism |
| :--- | :--- |
| View | Filterable by device; configurable row limit; running total shown |
| Add | Expandable form — device, date, task, cost, sourcing, notes |
| Edit | Selectbox → pre-populated form → Save Changes |
| Delete | Two-click confirmation |

### 3.4 Schedules

Full management of maintenance schedules.

| Action | Mechanism |
| :--- | :--- |
| View | Table with status badge, frequency, calendar link indicator |
| Add | Expandable form — device, task, first due date, frequency |
| Edit | Selectbox → pre-populated form → Save Changes |
| Activate / Deactivate | Toggle button |
| Delete | Two-click confirmation |

### 3.5 Notifications

Triggers for Google Calendar and Gmail integrations.

| Element | Detail |
| :--- | :--- |
| Calendar Push | Device filter (all or specific), force re-push toggle, Push button |
| Calendar Status | Live count of linked vs. unlinked schedules |
| Email Alerts | Day window slider (1–30), live preview of affected tasks, Send button |

## 4. UX Conventions

- Two-click confirmation for all destructive actions (delete).
- Forms use `st.form` with `clear_on_submit=True` to reset after save.
- `st.rerun()` called after all mutations to reflect updated state immediately.
- Notification imports are lazy (inside button handlers) to avoid startup errors if Google token is missing.
- Status badges: ⛔ overdue · 🔴 due today · 🟡 within 7d · 🟢 future.
