# Module 2: Maintenance History Ledger

## 1. Objective

Maintain a complete historical record of all maintenance activities for budgeting, warranty verification, and future reference. All records are manageable via both the Web UI and CLI.

## 2. Log Data Structure

| Field | Description |
| :--- | :--- |
| Completion Date | Date the maintenance was performed |
| Device Reference | FK to the inventory item |
| Service Type Reference | FK to service type; NULL if the entry is manual / ad-hoc |
| Task Performed | Description of the work (e.g., "Replaced HVAC Filter") |
| Cost (CAD) | Expenditure on parts, tools, or professional service |
| Sourcing Info | Vendor or URL where replacement parts were found |
| Notes | Observations or installation tips for next time |

## 3. UI Operations

All log actions live in the **History** view (sidebar nav).

| Action | Mechanism |
| :--- | :--- |
| View | Flat bordered-card list (date · device · task · cost · service-type), sorted by completion date. Filter bar: Device · Category · Date From · Date To · Limit (10/25/50/100). Filtered Entries + Spend totals pinned top-right |
| Add | "＋ Log Entry" button top-right → inline form above the list |
| Complete Due Task | Compact amber chip row (3-wide) above the list; clicking a chip prefills the log form and advances the schedule on save |
| Edit | Per-entry "Open ↗" → `@st.dialog` modal with pre-populated form → Save Changes |
| Delete | From inside the entry modal → two-click confirmation |

## 4. CLI Operations

```
python main.py history list [--device ID] [--limit N]
python main.py history add   # interactive prompts
```

## 5. Workflow

1. Task completed → user clicks "＋ Log Entry" in the History view (or `history add` via CLI)
2. Logs date, cost, sourcing, notes linked to device (and optionally a service type)
3. If the entry was launched from the Due & Overdue Tasks banner, the associated schedule's next due date advances automatically on save
4. Entry appended to history; spend totals update in real time

## 6. Spend Tracking

- Per-device total shown inside the device dialog (Devices view)
- Global and per-device totals shown in the History view filter bar and on the Dashboard stat row
- Future: cost analytics dashboard with trend charts (Phase 2)
