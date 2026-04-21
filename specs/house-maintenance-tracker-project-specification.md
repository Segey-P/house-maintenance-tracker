# House Maintenance Tracker - Project Specification

## 1. Project Overview

The House Maintenance Tracker is a comprehensive digital solution designed to streamline the management and upkeep of household systems and appliances. By centralizing device data, maintenance history, and scheduling, the system ensures longevity of household assets and minimizes the risk of unexpected failures. This project is specifically optimized for a one-bedroom residence to maintain simplicity and high utility.

**Status:** Active — CLI and Web UI operational.

## 2. Core Modules

### 2.1 Module 1: Inventory Management

The inventory serves as the primary database for all household assets. Each entry is categorized to facilitate quick retrieval of information.

* **Categories:**
  * **Major Appliances:** Refrigerator, Oven/Stove, Dishwasher, Range Hood.
  * **Kitchen Appliances:** Small countertop appliances (kettle, toaster, microwave, coffee machine, etc.).
  * **Laundry Systems:** Washer, Dryer.
  * **Plumbing & Water:** Water heater, filtration systems, faucets.
  * **Safety & Electrical:** Smoke detectors, carbon monoxide alarms, HVAC systems, electrical panel.

* **Device Attributes:**

| Attribute | Description |
| :--- | :--- |
| Device Name | Common name (e.g., "Main Fridge") |
| Category | One of the five defined categories |
| Model / Serial Number | Manufacturer specifications for identification |
| Purchase Date | Date of acquisition |
| Warranty Expiry | Warranty end date |
| Notes | Free-form tips and observations |
| Is Archived | Soft-delete flag — archived devices are hidden but data is preserved |

* **Service Types (child of Device):** Part numbers, maintenance frequency, tutorial URL, purchase URL, and per-task notes now live on a `service_types` row rather than the device itself. One device can have many service types (e.g. fridge → water filter replacement, coil cleaning). Adding a service type auto-creates a schedule row.

| Service Type Attribute | Description |
| :--- | :--- |
| Device Reference | FK to the parent device |
| Name | Short label (e.g. "Water Filter Replacement") |
| Frequency (days) | Recommended interval for service in days |
| Part Numbers | Specific part IDs for consumables (filters, bulbs, etc.) |
| Tutorial URL | YouTube / instructional link |
| Purchase URL | Amazon.ca or other vendor link |
| Notes | Task-specific tips |

* **UI Operations:** Add, Edit, Archive/Unarchive, Delete (hard delete with cascade). Service types are managed inside the device dialog.
* **Future (Phase 2):** Photo upload → AI visual identification of make/model → auto-populate specs and suggest service types.

### 2.2 Module 2: Maintenance History Log

A ledger that records every maintenance event, providing a clear audit trail for the property and spend tracking.

* **Log Entry Fields:**

| Field | Description |
| :--- | :--- |
| Device Reference | FK to the inventory item |
| Task Performed | Description of work done |
| Completion Date | Date the task was finalized |
| Cost (CAD) | Expenses for parts, tools, or professional service |
| Sourcing Info | Vendor or URL where replacement parts were found |
| Notes | Installation tips or observations for future reference |

* **UI Operations:** Add, Edit, Delete.
* **Spend tracking:** Total cost aggregated per device and globally.

### 2.3 Module 3: Scheduling & Integrations Engine

Automates maintenance interval tracking and Google Calendar sync.

* **Google Calendar Integration:** Push recurring all-day events to the user's primary calendar. Event payload (task description, part numbers, purchase URL, tutorial URL) is pulled from the schedule's linked service type, not the device.
* **Schedule Management:** Add, edit, activate/deactivate, delete schedules via UI or CLI. Schedules are normally auto-created when a service type is added to a device; manual schedules are supported for one-off tasks.
* **Due date logic:** Static intervals (days) from last completion; advance-on-completion workflow supported.
* **Email alerts:** Removed from scope.

### 2.4 Module 4: Web UI

Streamlit-based single-page application deployed to Streamlit Community Cloud at `https://house-maintenance-tracker.streamlit.app`, gated by a bcrypt password from `st.secrets`.

Navigation is a dark-navy left sidebar (no top tabs). Views:

* **Dashboard:** Key metrics (active devices, overdue count, due this week, YTD spend), upcoming tasks table, recent activity feed.
* **Devices:** Filterable device list; Add / Edit / Archive / Delete via `_device_dialog`; service types managed inside the dialog; photo upload placeholder (Phase 2).
* **History:** Device-grouped expense log; Add / Edit / Delete entries; running spend total; Due & Overdue Tasks banner with inline Log / Skip / Pause actions.
* **Schedules:** Device-grouped schedule list with status badges; Add manual / Edit / Pause / Delete; calendar link status.
* **Integrations:** Google Calendar push (per device or all, with force re-push option). Email alerts removed.
* **Roadmap:** Phase 1 / 2 / 3 checklist mirroring `design_handoff/DESIGN.md §7`.

## 3. Technical Stack

| Layer | Technology |
| :--- | :--- |
| Storage | PostgreSQL (Neon) via `psycopg2`; connection string in `st.secrets["DATABASE_URL"]`, `sslmode=require` |
| Backend | Python 3.11+, dataclasses |
| CLI | Click |
| Web UI | Streamlit (amber accent `#e8823a`, DM Sans, dark-navy sidebar) |
| Integrations | Google Calendar API v3 |
| Auth (user) | bcrypt password via `st.secrets` |
| Auth (Google) | OAuth 2.0 — token stored in `config/credentials/token.json` for local dev; Streamlit Cloud integration pending backlog item |

## 4. Roadmap & Future Enhancements

### 4.1 AI-Driven Visual Identification (Phase 2)

Photo upload in the Inventory UI → vision model identifies make/model → auto-populates device attributes and suggests maintenance intervals.

### 4.2 Cost Analytics Dashboard

Spending trends over time, per-category breakdown, appliance replacement cost projections.
