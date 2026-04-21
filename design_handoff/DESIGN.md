# House Maintenance Tracker — Design Reference

> Last updated: April 21, 2026
> Based on design iteration session in Claude Projects.
>
> **Implementation path: Option A** — design realised in Streamlit with `@st.dialog` modals standing in for right-edge slide-over panels (~80% visual parity). The React prototypes in `hmt-shared.jsx` / `hmt-app.jsx` remain the visual reference only — the live app is `app.py`.

---

## 1. Vision

A personal home maintenance command centre for a 1-bedroom residence, with a clear path toward a **multi-unit / building management platform**. The app centralises device inventory, maintenance history, task scheduling, and AI-powered maintenance guidance.

Future state: property managers onboard buildings, create "typical maintenance plans" per unit type, and individual owners/tenants clone and customise those plans for their own unit.

---

## 2. Design Decisions

### 2.1 Navigation
- **Left sidebar** (not top tabs) — scales better as features grow; supports future property/unit switcher at the top of the nav
- Nav items: Dashboard · Devices · History · Schedules · Integrations · Roadmap
- Sidebar footer: user profile card + Sign out button
- Active item: highlighted with `#2a3659` background on dark `#13192b` sidebar
- Property switcher placeholder sits above the nav list (static "Squamish Home" until multi-property lands in Phase 4)

### 2.2 Visual Language
| Token | Value |
|---|---|
| Font | DM Sans (400/600/700/800) |
| Background | `#f8f7f5` (warm off-white) |
| Sidebar | `#13192b` (deep navy) |
| Accent | `#e8823a` (warm amber) |
| AI accent | `#8b5cf6` (violet) |
| Border | `#e5e5e3` |
| Card bg | `#ffffff` |
| Radius | 8–12px |

### 2.3 Status Colour System
| Status | Badge bg | Dot colour | Meaning |
|---|---|---|---|
| overdue | `#fef2f2` / `#dc2626` | `#ef4444` | Past due date |
| today | `#fff7ed` / `#c2410c` | `#f97316` | Due today |
| soon | `#fffbeb` / `#b45309` | `#f59e0b` | Within 7 days |
| upcoming | `#eff6ff` / `#1d4ed8` | `#3b82f6` | 8–30 days |
| ok | `#f0fdf4` / `#15803d` | `#22c55e` | 30+ days out |

### 2.4 Card accent strip
Cards use a left `border` accent in the status dot colour when a task is overdue or due soon — draws attention without heavy colour fills.

---

## 3. Page Structure

### Dashboard
- **Stats row** (4 cards): Active Devices · Overdue · Due This Week · YTD Spend
- **Left column**: task groups — Needs Attention → Due This Week → Later This Month. Each task has inline "✓ Done" (expands quick-log form) + "⏭ Skip"
- **Right column (top)**: AI Chat Assistant — context-aware, knows all devices and current schedule state
- **Right column (bottom)**: Recent Activity feed (last 5 entries)
- **Coming Soon** section removed from Dashboard — lives in roadmap below

### Devices
- Card grid (auto-fill, min 280px)
- Each card: device name, model, category pill, status badge, last service date
- Clicking a card opens a **slide-over side panel** (no page navigation)
- Device panel contains:
  - Specs grid (model, serial, purchased, warranty, total spend, YTD spend, next due, last service)
  - Notes block (amber highlight if present)
  - Service types list — each card is clickable → opens a nested side panel
  - Maintenance history (last 6 entries)
  - Delete device (with cascade warning)
- **Photo upload** is reserved for the "Add Device" flow only — not on existing device panels

### Service Type Panel (nested in Device panel)
- Edit form: name (required), frequency (required), part numbers (optional), notes (optional)
- Schedule status block (next due, status badge, times done)
- AI Tools: Find Parts + Find Tutorial — both use live Claude calls
- History specific to this service type
- Delete with confirmation

### History (formerly Maintenance)
- Log of all maintenance events
- Filterable by device
- Shows running total spend
- Due tasks surfaced as quick-fill shortcuts at top
- Inline "New Entry" form with device selector + date + task + cost + notes

### Schedules
- Grouped by urgency: Overdue → This Week → This Month → Later
- Each row: task name, status badge, device, frequency, Calendar sync indicator
- Pause / Resume toggle per schedule
- Calendar sync badge (🗓 Synced) shown inline

### Integrations (formerly Alerts)
- Google Calendar: target selector (all or single device), push button, force re-create toggle, live linked / not-yet-pushed counts
- Email alerts removed from scope (confirmed out of MVP)
- Future tiles: Gemini CSV import (walkthrough-to-inventory), IoT auto-detection, Amazon.ca auto-order

### Roadmap (new view)
- Three phase cards (Phase 1 Now / Phase 2 Next / Phase 3 Future) rendered from the same checklist as §7 below
- Purpose: single surface for communicating what ships next without leaving the app — replaces the removed "Coming Soon" block on the dashboard

---

## 4. UX Principles Applied

1. **Action-first dashboard** — overdue and due-soon tasks are the first thing you see, with one-click completion
2. **No page navigation for details** — everything opens in a slide-over panel (Esc to close)
3. **Minimal clicks** — "✓ Done" expands an inline form rather than navigating away
4. **AI at point of need** — Find Parts / Find Tutorial appear next to each service type, not on a separate AI page
5. **Required vs optional clearly labelled** — asterisk (*) on required fields, "(optional)" suffix on optional
6. **Destructive actions protected** — two-step confirmation for all deletes with cascade warnings
7. **Status always visible** — every schedule and device card shows its urgency at a glance

---

## 5. AI Feature Design

### Current (v1)
- **Find Parts** (per service type): Claude call with device model + task → returns part numbers, Amazon.ca links, CAD prices
- **Find Tutorial** (per service type): Claude call → returns YouTube search terms, 4–5 step guide, tools needed
- **AI Chat** (Dashboard): context-injected chat — knows all devices, overdue tasks, and due-this-week items

### Planned (v2+)
- **Photo → AI identification**: user snaps/uploads a photo of an appliance → vision model identifies make/model → auto-populates device specs and suggests maintenance schedule (in Add Device flow only)
- **Proactive parts suggestions**: AI surfaces replacement parts with referral links (Amazon.ca affiliate) without user triggering — monetisation opportunity
- **Proactive AI assistant**: chat-style, pushes alerts rather than waiting for questions; knows warranty status, upcoming tasks, seasonal reminders

---

## 6. Data Model Notes (from design session)

The current model separates **Schedules** (future) and **Maintenance History** (past). A unified **Tasks** concept was identified as the right long-term model:

```
Task = schedule instance that becomes a log entry when completed
     = "Schedules + History" combined into a single timeline
```

This would likely require:
- A `tasks` table with status: `upcoming | due | completed | skipped`
- History = tasks with `status = completed`
- Schedules = tasks with `status = upcoming | due`
- A dedicated **Tasks tab** (or renamed Maintenance tab) showing both future and past as a unified timeline

This is a **v2 data model change** — the current Streamlit backend would need migration.

---

## 7. Roadmap

### Phase 1 — Current (Streamlit MVP)
- [x] Device inventory CRUD
- [x] Service types split out of Device model
- [x] Maintenance history log
- [x] Schedule management
- [x] Google Calendar push (service-type-aware parts + links)
- [x] CLI interface
- [x] Postgres (Neon) storage, bcrypt password gate, Streamlit Cloud deploy
- [x] Email alerts removed from scope

### Phase 2 — UI Redesign (in flight — Option A, Streamlit)
**Wave 0 shipped**
- [x] Theme tokens (amber primary, warm off-white bg, DM Sans)
- [x] Tab rename (Maintenance → History, Notifications → Integrations)
- [x] Removed Coming Soon block from Dashboard
- [x] Fixed Calendar push bug (part numbers / resource links pulled from service type)

**Wave 1 shipped**
- [x] Sidebar nav replaces `st.tabs` (dark navy, amber-accented active state)
- [x] `src/ui.py` with status_info / badge_html / stat_card_html helpers
- [x] User profile + Sign out in sidebar footer
- [x] Property switcher placeholder
- [x] Roadmap view scaffold (Phase 1/2/3 cards)

**Waves 2–5 open**
- [ ] Dashboard refactor (stat tint row, task groups, inline ✓ Done / ⏭ Skip, Recent Activity card list)
- [ ] Devices redesign (card grid, redesigned dialog, nested service-type cards)
- [ ] History + Schedules refactor (flat card lists, urgency grouping, inline Pause/Resume)
- [ ] AI wiring (`anthropic` dependency, Find Parts, Find Tutorial, Dashboard Chat)
- [ ] Integrations visual refresh (Connect/Disconnect pill + synced/unsynced tile counts)
- [ ] Add Device flow with photo upload placeholder
- [ ] Mandatory/optional field labels on all forms
- [ ] Category spend on device cards

**Option A deltas from the prototype**
- Right-edge slide-overs → centred `@st.dialog` modals (Wave 6 may replace with a custom slide-over component)
- Archive **kept** in both DB and UI — the design's removal of archive is treated as a design error

### Phase 3 — AI & Automation
- [ ] Photo → AI appliance identification (Add Device flow)
- [ ] Proactive parts suggestions with Amazon.ca referral links
- [ ] Spend analytics dashboard (YTD trends, per-category, projections)
- [ ] PDF / CSV schedule export
- [ ] Unified Tasks data model (schedule + history combined)
- [ ] Mobile-optimised layout

### Phase 4 — Multi-Unit Platform
- [ ] Multi-property support (property switcher in sidebar)
- [ ] Building / property manager role
- [ ] "Typical maintenance plan" templates per unit type
- [ ] Individual owner/tenant accounts cloning building templates
- [ ] Shared vendor directory and parts library per building

---

## 8. Component Reference

| Component | File | Notes |
|---|---|---|
| Sidebar, Badge, Card, Btn, SidePanel, AIBlock | `hmt-shared.jsx` | Shared primitives |
| Dashboard, AIChatWidget, Devices, DevicePanel | `hmt-app.jsx` | Main views |
| ServiceTypePanel, Maintenance, Schedules, Notifications | `hmt-app.jsx` | Supporting views |

### Key shared components
- **`<AIBlock prompt label>`** — self-contained AI call button with loading/result/dismiss states
- **`<SidePanel open onClose title subtitle>`** — slide-over panel, Esc to close, backdrop click to close
- **`<Badge type>`** — status-colour-coded pill; types: overdue/today/soon/upcoming/ok/neutral/purple/blue
- **`<Card accent>`** — white card with optional left accent strip colour
