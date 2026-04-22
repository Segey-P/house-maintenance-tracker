# Module 3: Scheduling and Integrations Engine

## 1. Objective

Automate maintenance interval tracking and deliver calendar-based reminders via Google Calendar. Schedules are fully manageable through both the Web UI and CLI.

## 2. Integrations

| Channel | Detail |
| :--- | :--- |
| Google Calendar | Recurring all-day events pushed to primary calendar. RFC 5545 RRULE set by frequency. |

Email alerts were part of earlier scope and have since been removed. Proactive notifications are likely to return as per-task reminders attached to calendar events, or as a separate AI-driven channel — see `TODO.md` backlog.

## 3. Calendar Event Payload

Each event includes:

- Device name and category
- Task description (from the schedule)
- Due date with frequency as an RRULE
- Required part numbers (from the linked service type)
- Purchase link (from the linked service type — typically Amazon.ca)
- YouTube tutorial link (from the linked service type)

If a schedule has no linked service type, the part numbers and resource links are simply omitted from the event description.

## 4. Schedule Data Structure

| Field | Description |
| :--- | :--- |
| Device Reference | FK to inventory item |
| Service Type Reference | FK to service type; NULL for manual schedules |
| Task Description | What needs to be done |
| Next Due Date | ISO date of next occurrence |
| Frequency (days) | Repeat interval — displayed as readable alias where applicable |
| Is Active | Paused schedules are hidden from default view and skipped in calendar pushes |
| Calendar Event ID | Google Calendar event ID once pushed; NULL if not yet linked |

## 5. Frequency Aliases

| Days | Label |
| :--- | :--- |
| 7 | Weekly |
| 14 | Bi-weekly |
| 30 | Monthly |
| 60 | Every 2 months |
| 90 | Quarterly |
| 120 | Every 4 months |
| 180 | Semi-annual |
| 365 | Annual |

## 6. UI Operations

Schedules are typically **auto-created** when a service type is added to a device. Manual schedules are supported for ad-hoc tasks.

| Action | Mechanism |
| :--- | :--- |
| View | Urgency-grouped cards: Overdue · This Week · This Month · Later · Paused. Each card shows device + task + frequency + next-due metadata with a status badge and `🗓 Synced` pill when pushed |
| Add | Schedules view → "＋ Add Manual" → inline form (device, task, first due date, frequency) |
| Edit | Per-row "Open ↗" → `@st.dialog` modal → Save Changes |
| Pause / Resume | Inline ⏸ Pause / ▶ Resume button on every card — paused schedules excluded from calendar pushes |
| Delete | From inside the schedule modal → two-click confirmation |
| Export | ⬇ CSV button in the Schedules view header — downloads all schedules (active + paused) sorted by next due date |
| Push Calendar | Integrations view → Push to Calendar (per device or all; force re-push option) |
| Complete Due Task | History view → Due Tasks chip banner → prefills log form + advances schedule on save |

## 7. CLI Operations

```
python main.py schedule list [--all]
python main.py schedule due [--days N]
python main.py notify push [--device ID] [--force]
```

## 8. Interval Logic

- **Static:** Based on manufacturer recommendation (e.g., every 90 days for furnace filter)
- **Advance on completion:** After logging a history entry against a schedule, the schedule's next due date advances by `frequency_days`
- **Seasonal tasks:** Currently handled as static intervals; seasonal automation is a future enhancement

## 9. Auth

OAuth 2.0 via `setup_auth.py`. Token stored at `config/credentials/token.json` (gitignored).
Required Google APIs: **Google Calendar API v3** — must be enabled in the same Cloud project as the OAuth client.

Cloud deployment note: the current OAuth token is a local-dev-only artefact. Running calendar push on Streamlit Community Cloud requires the token to be surfaced via `st.secrets`; see `TODO.md` backlog.
