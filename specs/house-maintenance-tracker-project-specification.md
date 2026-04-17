# House Maintenance Tracker - Project Specification

## 1. Project Overview

The House Maintenance Tracker is a comprehensive digital solution designed to streamline the management and upkeep of household systems and appliances. By centralizing device data, maintenance history, and scheduling, the system ensures longevity of household assets and minimizes the risk of unexpected failures. This project is specifically optimized for a one-bedroom residence to maintain simplicity and high utility.

**Status:** Active — CLI and Web UI operational.

## 2. Core Modules

### 2.1 Module 1: Inventory Management

The inventory serves as the primary database for all household assets. Each entry is categorized to facilitate quick retrieval of information.

* **Categories:**
  * **Major Appliances:** Refrigerator, Oven/Stove, Dishwasher, Range Hood.
  * **Laundry Systems:** Washer, Dryer.
  * **Plumbing & Water:** Water heater, filtration systems, faucets.
  * **Safety & Electrical:** Smoke detectors, carbon monoxide alarms, HVAC systems, electrical panel.

* **Device Attributes:**

| Attribute | Description |
| :--- | :--- |
| Device Name | Common name (e.g., "Main Fridge") |
| Category | One of the four defined categories |
| Model / Serial Number | Manufacturer specifications for identification |
| Part Numbers | Specific part IDs for consumables (e.g., filters, bulbs) |
| Maintenance Frequency | Recommended interval for service in days |
| Resource Links | Direct links to YouTube tutorials and purchase pages |
| Purchase Date | Date of acquisition |
| Warranty Expiry | Warranty end date |
| Notes | Free-form tips and observations |
| Is Archived | Soft-delete flag — archived devices are hidden but data is preserved |

* **UI Operations:** Add, Edit, Archive/Unarchive, Delete (hard delete with cascade).
* **Future (Phase 2):** Photo upload → AI visual identification of make/model → auto-populate specs and maintenance interval.

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

### 2.3 Module 3: Scheduling & Notification Engine

Automates maintenance reminders and calendar management.

* **Google Calendar Integration:** Push recurring all-day events to the user's primary calendar. Events include task description, part numbers, purchase and tutorial links.
* **Email Alerts:** Structured HTML email to `sergey.pochikovskiy@gmail.com` with device details, due status, part numbers, vendor links, and YouTube tutorial.
* **Schedule Management:** Add, edit, activate/deactivate, delete schedules via UI or CLI.
* **Due date logic:** Static intervals (days) from last completion; advance-on-completion workflow supported.

### 2.4 Module 4: Web UI

Streamlit-based single-page application accessible at `http://localhost:8501`.

* **Dashboard tab:** Key metrics (active devices, overdue count, due this week, total spend), upcoming tasks table, recent activity feed.
* **Inventory tab:** Filterable device table; Add / Edit / Archive / Delete forms; photo upload placeholder (Phase 2).
* **History tab:** Filterable expense log; Add / Edit / Delete entries; running spend total.
* **Schedules tab:** Full schedule table with status badges; Add / Edit / Activate-Deactivate / Delete; calendar link status.
* **Notifications tab:** Google Calendar push (per device or all, with force re-push option); Email alert trigger with configurable day window and live preview of recipients.

## 3. Technical Stack

| Layer | Technology |
| :--- | :--- |
| Storage | SQLite (`data/house_maintenance.db`) |
| Backend | Python 3.9+, dataclasses |
| CLI | Click |
| Web UI | Streamlit |
| Notifications | Google Calendar API v3, Gmail API v1 |
| Auth | OAuth 2.0 — token stored in `config/credentials/token.json` |

## 4. Roadmap & Future Enhancements

### 4.1 AI-Driven Visual Identification (Phase 2)

Photo upload in the Inventory UI → vision model identifies make/model → auto-populates device attributes and suggests maintenance intervals.

### 4.2 Cost Analytics Dashboard

Spending trends over time, per-category breakdown, appliance replacement cost projections.
