# Design Handoff: House Maintenance Tracker UI

> Created: April 20, 2026  
> Designed in: Claude Projects (HTML prototype)  
> Target codebase: `Segey-P/house-maintenance-tracker` (Python / Streamlit → to be migrated or extended)

---

## Overview

This handoff package contains a **high-fidelity HTML prototype** of a redesigned House Maintenance Tracker web app. The current app is built in Streamlit (`app.py`). The goal of this prototype is to:

1. Define the target UI design before re-implementation
2. Iterate on UX and feature ideas before committing to backend changes
3. Serve as a reference for a full React (or Streamlit component) implementation

The prototype uses **React + Babel (in-browser)** and is fully interactive with sample data. It is a **design reference, not production code** — the developer's task is to recreate these screens in the target environment using its established patterns.

---

## Fidelity

**High-fidelity.** The prototype has:
- Final colours, typography, spacing, and component shapes
- Working interactions (slide-over panels, inline forms, AI calls via Claude)
- Realistic sample data seeded from the actual app's data model

Recreate the UI pixel-faithfully using the codebase's framework of choice.

---

## Design System

### Colours
| Token | Value | Usage |
|---|---|---|
| Background | `#f8f7f5` | Page background |
| Sidebar bg | `#13192b` | Left nav |
| Sidebar active | `#2a3659` | Active nav item |
| Accent | `#e8823a` | Primary buttons, highlights |
| Accent hover | `#d4722f` | Button hover |
| AI accent | `#8b5cf6` | AI feature buttons + badges |
| Border | `#e5e5e3` | Card/input borders |
| Card bg | `#ffffff` | Cards |
| Muted text | `#9ca3af` | Labels, captions |
| Body text | `#374151` | Body copy |
| Heading | `#1c1c1e` | Titles |

### Status colours (badge + accent strip system)
| Status | Background | Text | Dot / Strip |
|---|---|---|---|
| overdue | `#fef2f2` | `#dc2626` | `#ef4444` |
| today | `#fff7ed` | `#c2410c` | `#f97316` |
| soon (≤7d) | `#fffbeb` | `#b45309` | `#f59e0b` |
| upcoming (≤30d) | `#eff6ff` | `#1d4ed8` | `#3b82f6` |
| ok (>30d) | `#f0fdf4` | `#15803d` | `#22c55e` |
| neutral | `#f4f4f5` | `#52525b` | `#d1d5db` |

### Typography
- **Font family**: DM Sans (Google Fonts) — weights 400, 600, 700, 800
- **Page title**: 20px / 700
- **Card title**: 14–15px / 700
- **Body**: 13px / 400
- **Caption/label**: 11–12px / 600, uppercase + letter-spacing for section labels
- **Stat numbers**: 28px / 800

### Spacing & Shape
- **Card border radius**: 12px (outer), 8px (inner elements)
- **Button border radius**: 8px
- **Card shadow**: `0 1px 4px rgba(0,0,0,0.04)` at rest, `0 4px 16px rgba(0,0,0,0.08)` on hover
- **Sidebar width**: 220px, sticky, full viewport height
- **Main content padding**: 32px 36px
- **Max content width**: 1100px

---

## Screens / Views

### 1. Dashboard
**Purpose**: Action-first overview. User sees what needs attention immediately and can complete tasks in-place.

**Layout**: Full-width main area
- **Stats row**: 4-column grid, equal width cards. Each card: label (11px uppercase, `#9ca3af`), value (28px/800).
  - Active Devices · Overdue (red bg if >0) · Due This Week (amber bg if >0) · YTD Spend
- **Two-column grid** below stats: `1fr 380px` gap 20px
  - **Left**: Task groups (Needs Attention → Due This Week → Later This Month). Each group has a coloured dot + uppercase label + count. Tasks are `<Card>` with left accent strip.
    - Task card: task name (14px/600) + status badge, device name + model (12px, muted). Right side: "✓ Done" (primary button) + "⏭ Skip" (ghost)
    - Clicking "✓ Done" expands an inline form below the task: cost input + notes input + "Mark Done" + "Cancel"
  - **Right column**:
    - **AI Chat widget** (top): header with ✦ icon + "AI Assistant" + Beta badge. Message bubbles: user = amber bg right-aligned, assistant = `#f8f7f5` left-aligned. Input + Send button at bottom. Height 180px scrollable.
    - **Recent Activity** (below chat): card list, 5 entries. Columns: device name / task (left), date + cost (right).

### 2. Devices
**Purpose**: Browse and manage household device inventory.

**Layout**:
- Filter bar: search input (flex 1) + category dropdown + "Show archived" checkbox
- Device grid: `repeat(auto-fill, minmax(280px, 1fr))` gap 12px
- Last card: dashed "Add Device" placeholder

**Device card**:
- Left accent strip (status colour)
- Top row: device name (14px/700) + model (11px muted) | status badge (right)
- Category pill: `background: catColor+'18'`, `color: catColor`, `border: catColor+'30'`
- Warranty expiring badge if within the year
- Footer row: "Last: MM/YY" | "Open ↗" (amber, 600)

**Device Side Panel** (slide-over, 520px wide):
- Header: device name + category subtitle + ✕ close
- Device image (140px tall, object-fit cover, rounded 10px)
- 4-column specs grid: Model · Serial · Purchased · Warranty · Total Spend · YTD Spend · Next Due · Last Service
- Notes block (amber bg `#fffbeb`, border `#fde68a`) if notes present
- Service Types section header + "+ Add" button
- Add service type form (collapsible): Name* · Frequency* · First due date · Part numbers · Notes
- Service type cards (clickable → opens nested panel):
  - Name + frequency badge + status badge
  - Part numbers (if any)
  - AI buttons: "✦ Find Parts" + "▶ Find Tutorial"
- Maintenance history (last 6 entries): date / task / cost columns
- Delete device button (ghost red) → confirmation block

**Service Type Side Panel** (nested, same 520px):
- Status block: Next Due · Status badge · Times Done
- Edit form: Name* · Frequency* · Part numbers (optional) · Notes (optional) + Save
- AI Tools: Find Parts + Find Tutorial
- History for this service type
- Delete with confirmation

### 3. History (formerly Maintenance)
**Purpose**: Log and browse all maintenance events.

**Layout**:
- Header: "Maintenance" + "+ Log Entry" button
- Due tasks prompt bar (amber bg) if tasks due ≤7d — chips per task that pre-fill the form
- Log entry form (collapsible): device selector + date + task* + cost + notes
- Filter bar: device dropdown + entry count + total spend metric
- Log list: Card per entry — date (70px) / task + device (flex) / cost (right)

### 4. Schedules
**Purpose**: View and manage all maintenance schedules.

**Layout**:
- Header + "Show paused" checkbox + "+ Manual" button
- Groups: Overdue · This Week · This Month · Later
- Each group: coloured dot + label + count
- Schedule row card (left accent strip): task name + status badge + Calendar sync badge | Pause/Resume button
- Footer: device name · frequency · due date

### 5. Alerts
**Purpose**: Configure integrations and trigger notifications.

**Layout**: 2-column grid (max 760px), 3rd row full-width
- **Google Calendar card**: setup/connect description + Synced/Pending counts + "Push to Calendar" button
- **Email Alerts card**: description + day-window slider + task count preview + "Send Alert" button
- **AI Assistant teaser** (full-width dashed card): icon + title + Coming Soon badge + description

---

## Interactions & Behaviour

| Interaction | Behaviour |
|---|---|
| Click device card | Opens slide-over DevicePanel (right edge, 520px, backdrop dims) |
| Click service type card | Opens nested ServiceTypePanel (same width, stacks on top) |
| Esc key | Closes topmost open panel |
| Backdrop click | Closes topmost open panel |
| "✓ Done" on task | Expands inline QuickComplete form below the task card |
| "Mark Done" submit | Adds log entry, advances schedule due date, shows toast |
| "⏭ Skip" | Advances schedule due date without logging |
| "⏸ Pause" on schedule | Sets `is_active = false`, row shows ⏸ prefix |
| Delete (any entity) | Two-step: ghost red button → confirmation block with "Yes, delete" + "Cancel" |
| AI button (Find Parts / Find Tutorial) | Calls Claude API, shows spinner, renders result in purple block with dismiss |
| AI Chat send | Appends user bubble, calls Claude with context, appends assistant bubble |
| Property switcher (sidebar top) | (Future) — chevron indicates dropdown coming |
| Toast | Bottom-centre fixed pill, auto-dismisses after 3s |

### Panel animation
- Slide in from right: `transform: translateX(width → 0)`, `transition: 0.25s cubic-bezier(0.4,0,0.2,1)`
- Backdrop: `opacity: 0 → 0.3`, `transition: 0.2s`

---

## State Management

```
App state (top-level):
  devices[]          — full device list
  serviceTypes[]     — all service types
  schedules[]        — all schedules (mutated on complete/skip/pause)
  logs[]             — maintenance log (prepended on new entry)
  nav                — current view ('dashboard'|'devices'|'maintenance'|'schedules'|'notifications')

Derived (computed):
  overdue            — schedules where daysUntil(next_due_date) < 0
  dueSoon            — schedules where daysUntil in [0,7]
  ytdSpend           — sum of log.cost_cad where completion_date >= current year
```

Key mutations:
- **Complete task**: add log entry → advance schedule `next_due_date += frequency_days`
- **Skip task**: advance schedule only, no log
- **Pause/resume**: toggle `schedule.is_active`
- **Delete device**: cascade delete service types, schedules, logs for that device

---

## AI Integration

The prototype uses `window.claude.complete()` (Claude Haiku via the design environment). In production, replace with your backend's Claude API calls.

### Find Parts
```
Prompt: "I need to do '{task}' on a {model}. What exact replacement parts? 
         List: part numbers, Amazon.ca links, CAD prices."
```

### Find Tutorial
```
Prompt: "How do I do '{task}' on a {model}? 
         YouTube search terms, 4-5 steps, tools needed."
```

### Chat Assistant (Dashboard)
```
System context injected: device list, overdue tasks, due-this-week tasks, location (Squamish BC).
Model: Claude Haiku. Keep responses concise and practical.
```

**Future monetisation note**: Find Parts should proactively include Amazon.ca affiliate referral links. This should be AI-driven (not just user-triggered) — the AI surfaces relevant parts with referral links proactively when viewing a service type.

---

## Data Model Notes

The current backend has separate `schedules` and `maintenance_logs` tables. A unified **Tasks** concept was identified as the right v2 model:

```
tasks table:
  id, device_id, service_type_id
  title, description
  status: 'upcoming' | 'due' | 'completed' | 'skipped'
  due_date, completed_date
  cost_cad, notes, sourcing_info
  frequency_days (for recurring tasks)
```

This would unify the History and Schedules views into a single timeline. **This is a v2 backend change** — do not implement in v1 without a migration plan.

---

## Files in this Package

| File | Purpose |
|---|---|
| `Home Maintenance Tracker.html` | Shell HTML — loads React + Babel, mounts app |
| `hmt-shared.jsx` | Shared primitive components: Badge, Card, Btn, SidePanel, AIBlock, Sidebar, etc. |
| `hmt-app.jsx` | All views + data: Dashboard, Devices, DevicePanel, ServiceTypePanel, Maintenance, Schedules, Notifications, App root |
| `DESIGN.md` | Design reference document (system, roadmap, decisions) |

---

## Roadmap Summary

| Phase | Status | Key deliverables |
|---|---|---|
| 1 — Streamlit MVP | ✅ Done | Inventory, history, schedules, calendar, email, CLI |
| 2 — UI Redesign | 🔄 In progress | React prototype (this package), action-first dashboard, AI tools |
| 3 — AI & Automation | 📋 Planned | Photo ID, proactive parts, spend analytics, Tasks data model |
| 4 — Multi-Unit Platform | 📋 Future | Building manager, unit templates, tenant accounts |

See `DESIGN.md` for full roadmap details.
