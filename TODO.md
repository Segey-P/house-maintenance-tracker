# House Maintenance Tracker — TODO

## In Progress

_(nothing active)_

## Next Up

- [ ] Download schedule as checklist (CSV or PDF export of upcoming tasks from Schedules tab)

## Backlog

- [ ] Google Calendar integration — store OAuth token in Streamlit secrets for cloud use
- [ ] Gemini CSV import — structured CSV format that Gemini can produce from a camera walkthrough, importable via the UI (devices + service types in one file). See `scripts/seed_data.sql` as schema reference.

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
