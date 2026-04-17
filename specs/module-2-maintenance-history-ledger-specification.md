# Module 2: Maintenance History Ledger

## 1. Objective

Maintain a complete historical record of all maintenance activities for budgeting, warranty verification, and future reference. All records are manageable via both the Web UI and CLI.

## 2. Log Data Structure

| Field | Description |
| :--- | :--- |
| Completion Date | Date the maintenance was performed |
| Device Reference | FK to the inventory item |
| Task Performed | Description of the work (e.g., "Replaced HVAC Filter") |
| Cost (CAD) | Expenditure on parts, tools, or professional service |
| Sourcing Info | Vendor or URL where replacement parts were found |
| Notes | Observations or installation tips for next time |

## 3. UI Operations

| Action | Mechanism |
| :--- | :--- |
| View | Filterable by device; configurable row limit (10/25/50/100); running spend total shown inline |
| Add | "+ Log Expense" button top-right → inline form above table |
| Edit | "Edit / Delete Entry" expander → selectbox → pre-populated form |
| Delete | Modal confirmation dialog |

## 4. CLI Operations

```
python main.py history list [--device ID] [--limit N]
python main.py history add   # interactive prompts
```

## 5. Workflow

1. Task completed → user clicks "+ Log Expense" in History tab (or `history add` via CLI)
2. Logs date, cost, sourcing, notes linked to device
3. After logging, optionally advance the associated schedule's next due date
4. Entry appended to history; spend totals update in real time

## 6. Spend Tracking

- Per-device total available on device detail view (Inventory tab)
- Global total shown in History tab filter bar and Dashboard metric card
- Future: cost analytics dashboard with trend charts (Phase 2)
