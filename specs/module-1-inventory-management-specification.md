# Module 1: Inventory Management

## 1. Objective

Maintain a complete registry of all household systems and appliances. Each device record is the source of truth for maintenance scheduling, spend tracking, and notification content.

**Status:** Active — full CRUD implemented in `src/inventory.py`; Web UI in Inventory tab; CLI via `main.py`.

## 2. Categories

| Category | Examples |
| :--- | :--- |
| Major Appliances | Refrigerator, Oven/Stove, Dishwasher, Range Hood |
| Laundry Systems | Washer, Dryer |
| Plumbing & Water | Water heater, filtration systems, faucets |
| Safety & Electrical | Smoke detectors, CO alarms, HVAC systems, electrical panel |

## 3. Device Attributes

| Attribute | Type | Description |
| :--- | :--- | :--- |
| Device Name | Text (required) | Common name, e.g. "Main Fridge" |
| Category | Enum (required) | One of the four categories above |
| Model | Text | Manufacturer model number |
| Serial Number | Text | Unit-specific serial for warranty/service |
| Part Numbers | List[Text] | Consumable part IDs (comma-separated in UI) |
| Maintenance Frequency | Integer (days, required) | Recommended service interval |
| Resource Links | Dict | `tutorial` (YouTube URL) and `purchase` (Amazon.ca URL) |
| Purchase Date | ISO Date | Date of acquisition |
| Warranty Expiry | ISO Date | Warranty end date |
| Notes | Text | Free-form tips, BC code requirements, observations |
| Is Archived | Boolean | Soft-delete — hidden from default views, data preserved |

## 4. UI Operations

| Action | Mechanism |
| :--- | :--- |
| View | Filterable table (by category, archived flag); per-device spend shown inline |
| Add | "+ Add Device" toggle button → inline form with all fields |
| Edit | "Edit / Manage Device" expander → selectbox → pre-populated form → Save Changes |
| Archive / Restore | Toggle button — preserves all linked history and schedules |
| Delete | Two-click modal confirmation → hard delete with cascade to history and schedules |
| Photo Upload | Disabled placeholder; reserved for Phase 2 AI identification |

## 5. CLI Operations

```
python main.py inventory list [--category CAT] [--archived]
python main.py inventory add   # interactive prompts
python main.py inventory edit  ID
python main.py inventory archive ID
python main.py inventory delete ID
```

## 6. Data Storage

SQLite table `devices` in `data/house_maintenance.db`. Foreign key constraints enforced; cascade delete propagates to `maintenance_log` and `schedules`.

**Cloud note:** On Streamlit Community Cloud the filesystem is ephemeral. For persistent storage across deployments, commit the database file to the repo (acceptable for single-user, low-write workload) or migrate to a hosted backend (Turso, Supabase free tier).

## 7. Future — Phase 2

Photo upload in the Inventory UI → vision model identifies make/model → auto-populates device attributes and suggests maintenance intervals.
