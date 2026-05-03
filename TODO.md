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
- [ ] multi-user experience
- [ ] Secure User Authentication: Private sign-up/login for neighbors using Supabase Auth.

Master Building Blueprint: A central library of pre-defined maintenance tasks specific to your building's infrastructure.

One-Click Import: A feature allowing neighbors to instantly copy the master blueprint into their private personal dashboard.

Dynamic Due-Date Calculator: Automated reminders based on the last date a task (like an HRV filter change) was completed.

Parts & Specs Wiki: A shared directory of exact filter sizes, lightbulb types, and battery models used throughout the 100 units.

Vetted Contractor Directory: A list of plumbers and electricians who have successfully performed work in the building.

Service Expense Tracker: A log to record costs of repairs for investment tracking or potential tax deductions.

Home Health PDF Generator: A one-button export of all maintenance history to show prospective buyers during a resale.

Photo Evidence Log: Cloud storage for uploading photos of receipts and "before/after" shots of serviced equipment.

Retail Quick-Links: Direct links to Canadian retailers (Home Depot, Amazon) for the specific parts listed in the specs.

Building-Wide Alerts: A shared calendar for annual inspections, fire alarm testing, or scheduled water shut-offs.
