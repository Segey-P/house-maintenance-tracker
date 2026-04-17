# Module 3: Scheduling and Notification Engine

## 1. Objective

Automate maintenance interval tracking and deliver timely reminders via Google Calendar and Gmail. Schedules are fully manageable through both the Web UI and CLI.

## 2. Notification Channels

| Channel | Detail |
| :--- | :--- |
| Google Calendar | Recurring all-day events pushed to primary calendar. RFC 5545 RRULE set by frequency. |
| Gmail | HTML email to `sergey.pochikovskiy@gmail.com` with device details, urgency badge, parts list, purchase link, tutorial link. |

## 3. Notification Content

Each alert includes:

- Device name and category
- Task description
- Due date with urgency label (Overdue / Due today / In Nd)
- Required part numbers
- Purchase link (Amazon.ca or specified vendor)
- YouTube tutorial link

## 4. Schedule Data Structure

| Field | Description |
| :--- | :--- |
| Device Reference | FK to inventory item |
| Task Description | What needs to be done |
| Next Due Date | ISO date of next occurrence |
| Frequency (days) | Repeat interval — displayed as readable alias where applicable |
| Is Active | Paused schedules are hidden from default view and skipped in alerts |
| Calendar Event ID | Google Calendar event ID once pushed; NULL if not yet linked |

## 5. Frequency Aliases

| Days | Label |
| :--- | :--- |
| 7 | Weekly |
| 30 | Monthly |
| 90 | Quarterly |
| 180 | Semi-annual |
| 365 | Annual |

## 6. UI Operations

| Action | Mechanism |
| :--- | :--- |
| View | Full schedule table with status badges and calendar link status |
| Add | "+ Add Schedule" button top-right → inline form |
| Edit | "Edit / Manage Schedule" expander → selectbox → pre-populated form |
| Pause / Resume | Toggle button — paused schedules excluded from alerts |
| Delete | Modal confirmation dialog |
| Push Calendar | Notifications tab → Push to Calendar (per device or all; force re-push option) |
| Email Alerts | Notifications tab → slider for day window → live preview → Send |

## 7. CLI Operations

```
python main.py schedule list [--all]
python main.py schedule due [--days N]
python main.py notify push [--device ID] [--force]
python main.py notify check [--days N]
```

## 8. Interval Logic

- **Static:** Based on manufacturer recommendation (e.g., every 90 days for furnace filter)
- **Advance on completion:** After logging a history entry, user is prompted to advance the schedule's next due date by the frequency interval
- **Seasonal tasks:** Currently handled as static intervals; seasonal automation is a future enhancement

## 9. Auth

OAuth 2.0 via `setup_auth.py`. Token stored at `config/credentials/token.json` (gitignored).  
Required Google APIs: **Google Calendar API v3**, **Gmail API v1** — must be enabled in the same Cloud project as the OAuth client.
