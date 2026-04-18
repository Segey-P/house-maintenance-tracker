# House Maintenance Tracker — TODO

## In Progress

- [ ] Update app.py UI for service types: device popup services section, maintenance log with service type selector, schedules tab cleanup

## Next Up

- [ ] Re-enable password gate before sharing app publicly (`utils/auth.py` — uncomment `require_password()` in `app.py`)
- [ ] Download schedule as checklist (CSV or PDF export of upcoming tasks from Schedules tab)

## Backlog

- [ ] Google Calendar integration — store OAuth token in Streamlit secrets for cloud use
- [ ] Email alerts — maintenance reminders to user inbox

## Done

- [x] Provision Neon PostgreSQL database
- [x] Deploy to Streamlit Community Cloud (`house-maintenance-tracker.streamlit.app`)
- [x] Add database credentials and password hash to Streamlit secrets
- [x] Build core UI: Dashboard, Devices, Maintenance, Schedules, Notifications tabs
- [x] Service types data model: new schema, CRUD module, updated schedules and maintenance_log
