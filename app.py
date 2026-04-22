"""House Maintenance Tracker — Streamlit Web UI."""
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from src.db import init_db
from src import inventory as inv
from src import history as hist
from src import scheduler as sched
from src import services as svcs
from src.models import Device, MaintenanceLog, Schedule, ServiceType
from src.scheduler import days_until_due
from src.ui import STATUS_STYLES, badge_html, stat_card_html, status_info
from utils.auth import logout_button, require_password

CATEGORIES = ["Major Appliances", "Kitchen Appliances", "Laundry Systems", "Plumbing & Water", "Safety & Electrical"]
FREQ_ALIASES = {7: "Weekly", 14: "Bi-weekly", 30: "Monthly", 60: "Every 2 months",
                90: "Quarterly", 120: "Every 4 months", 180: "Semi-annual", 365: "Annual"}
LIMIT_OPTIONS = [10, 25, 50, 100]

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="House Maintenance Tracker",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

require_password()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800&display=swap');

html, body, [class*="st-"], button, input, textarea, select {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Remove Streamlit top chrome. `display: none` (not `visibility: hidden`) so
   the header stops reserving space — previously the invisible sticky header
   was clipping the top of the content below. */
header, footer { display: none !important; }
#MainMenu { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1100px; }

/* Sidebar-expand chevron (shown when the sidebar is collapsed). Style it as
   an amber pill so it's always findable on any background, regardless of
   which Streamlit version renders it inside or outside the header. */
button[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapsedControl"],
button[kind="headerNoPadding"][data-testid*="Collapsed"] {
    background: #e8823a !important;
    color: #ffffff !important;
    border: 1px solid #d4722f !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.14) !important;
    top: 12px !important; left: 12px !important;
    padding: 6px 10px !important;
    z-index: 999 !important;
}
[data-testid="stSidebarCollapsedControl"] svg,
button[data-testid="stSidebarCollapsedControl"] svg {
    color: #ffffff !important; fill: #ffffff !important; stroke: #ffffff !important;
}

/* Headings */
h1, h2, h3 { color: #1c1c1e; letter-spacing: -0.01em; }

/* Metric cards — design §2.2 stat row */
div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e5e5e3;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
div[data-testid="metric-container"] > label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
    color: #9ca3af;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: 800;
    color: #1c1c1e;
    letter-spacing: -0.02em;
}

/* Primary button — amber accent */
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: #e8823a;
    border-color: #e8823a;
    color: #ffffff;
    font-weight: 600;
    border-radius: 8px;
}
.stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background: #d4722f;
    border-color: #d4722f;
    color: #ffffff;
}

/* Secondary / ghost buttons */
.stButton > button[kind="secondary"], .stFormSubmitButton > button[kind="secondary"] {
    background: #f8f7f5;
    border: 1px solid #e5e5e3;
    color: #374151;
    font-weight: 600;
    border-radius: 8px;
}
.stButton > button[kind="secondary"]:hover {
    background: #f0f0ee;
    border-color: #d1d5db;
    color: #1c1c1e;
}

/* Tab bar */
div[data-testid="stTabs"] > div:first-child button {
    font-size: 13px;
    padding: 0.55rem 1.1rem;
    font-weight: 600;
}
div[data-testid="stTabs"] > div:first-child button[aria-selected="true"] {
    color: #e8823a;
}

/* Containers (bordered) — act as design's Card */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px !important;
    border-color: #e5e5e3 !important;
    background: #ffffff;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* Sidebar — dark navy per design §2.1. Width left at the Streamlit default
   so the collapse animation behaves correctly (hard-coding it previously
   interfered with the open/closed transition). */
section[data-testid="stSidebar"] {
    background: #13192b !important;
    border-right: 1px solid #1e2a42;
}
section[data-testid="stSidebar"] > div { padding-top: 8px; }
section[data-testid="stSidebar"] * { color: #e2e8f0; }
section[data-testid="stSidebar"] hr,
section[data-testid="stSidebar"] [data-testid="stHorizontalRule"] { border-color: #1e2a42 !important; background: #1e2a42 !important; }
/* Collapse-sidebar (X) button inside the expanded sidebar */
section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] svg {
    fill: #e2e8f0 !important; stroke: #e2e8f0 !important;
}

/* Sidebar buttons — nav items */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent;
    border: none;
    color: #94a3b8 !important;
    font-weight: 400;
    font-size: 13px;
    text-align: left;
    justify-content: flex-start;
    padding: 9px 12px;
    border-radius: 8px;
    width: 100%;
    box-shadow: none;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #1c2540;
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #2a3659 !important;
    color: #ffffff !important;
    font-weight: 600;
    border: none;
}

/* Property switcher block */
.hmt-prop-switch {
    margin: 8px 12px 12px;
    padding: 10px 12px;
    border-radius: 10px;
    background: #1c2540;
    border: 1px solid #2a3659;
    display: flex;
    align-items: center;
    gap: 10px;
}
.hmt-prop-switch .icon {
    width: 32px; height: 32px; border-radius: 8px; background: #e8823a;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    color: white; font-size: 16px; font-weight: 800;
}
.hmt-prop-switch .prop-name { font-size: 13px; font-weight: 700; color: #f1f5f9; line-height: 1.2; }
.hmt-prop-switch .prop-sub  { font-size: 10px; color: #64748b; margin-top: 1px; }

/* Sidebar footer user card */
.hmt-user {
    margin: 12px;
    padding: 8px 10px;
    border-radius: 8px;
    background: transparent;
    display: flex; align-items: center; gap: 10px;
    border-top: 1px solid #1e2a42;
    padding-top: 14px;
}
.hmt-user .avatar {
    width: 28px; height: 28px; border-radius: 50%; background: #2a3659;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; color: #94a3b8; flex-shrink: 0;
}
.hmt-user .name { font-size: 12px; font-weight: 600; color: #e2e8f0; }
.hmt-user .role { font-size: 10px; color: #475569; }

/* Sidebar-level nav-count badge (for overdue) */
.hmt-nav-badge {
    background: #ef4444; color: #fff; font-size: 10px; font-weight: 700;
    border-radius: 20px; padding: 1px 6px; margin-left: 4px;
}

/* Category pill — design §2.3 neutral pill variant */
.hmt-pill {
    display: inline-block; font-size: 11px; font-weight: 600;
    letter-spacing: 0.03em; padding: 2px 8px; border-radius: 20px;
    background: #f4f4f5; color: #52525b; border: 1px solid #e4e4e7;
}

/* Device dialog specs grid label/value pair */
.hmt-spec-label {
    font-size: 11px; color: #9ca3af; text-transform: uppercase;
    letter-spacing: 0.04em; font-weight: 600;
}
.hmt-spec-value {
    font-size: 14px; color: #1c1c1e; font-weight: 600; margin-top: 2px;
}

/* Amber notes block — design §3 device detail */
.hmt-notes {
    background: #fffbeb; border: 1px solid #fde68a; border-left: 3px solid #f59e0b;
    border-radius: 8px; padding: 10px 14px; color: #78350f; font-size: 13px;
    line-height: 1.5; margin: 8px 0 12px;
}
</style>
""", unsafe_allow_html=True)

init_db()

# ── Helpers ───────────────────────────────────────────────────────────────────

def _status(days: int) -> str:
    if days < 0:   return f"⛔ {abs(days)}d overdue"
    if days == 0:  return "🔴 Due today"
    if days <= 7:  return f"🟡 {days}d"
    if days <= 30: return f"🟠 {days}d"
    return         f"🟢 {days}d"

def _freq(days: int) -> str:
    alias = FREQ_ALIASES.get(days)
    return f"{alias} ({days}d)" if alias else f"{days} days"

def _money(val: float) -> str:
    return f"${val:,.2f}" if val else "—"

def _model(val) -> str:
    if not val or val.lower().startswith("check"):
        return "—"
    return val[:30] + "…" if len(val) > 30 else val

def _style_schedule(df: pd.DataFrame):
    def row_bg(row):
        s = row.get("Status", "")
        if "overdue" in s:
            return ["background-color: #fee2e2"] * len(row)
        if "Due today" in s or ("🟡" in s):
            return ["background-color: #fefce8"] * len(row)
        return [""] * len(row)
    return df.style.apply(row_bg, axis=1)


def _dash_task_group(label: str, schedules: list) -> None:
    """Dashboard task group — design §3 Needs-Attention / Due-Week / Later-Month."""
    if not schedules:
        return
    st.markdown(
        f"<h4 style='margin:18px 0 10px;color:#1c1c1e;font-size:14px;"
        f"text-transform:uppercase;letter-spacing:0.06em;font-weight:700;'>"
        f"{label}  <span style='color:#9ca3af;font-weight:500'>({len(schedules)})</span></h4>",
        unsafe_allow_html=True,
    )
    for s in schedules:
        days  = days_until_due(s.next_due_date)
        sinfo = status_info(days)
        with st.container(border=True):
            top1, top2 = st.columns([5, 3])
            top1.markdown(
                f"<div style='font-size:11px;color:#9ca3af;text-transform:uppercase;"
                f"letter-spacing:0.04em;font-weight:600'>{s.device_name}</div>"
                f"<div style='font-size:15px;font-weight:600;color:#1c1c1e;margin-top:2px'>"
                f"{s.task_description}</div>",
                unsafe_allow_html=True,
            )
            top2.markdown(
                f"<div style='text-align:right'>"
                + badge_html(sinfo["status"], sinfo["label"])
                + f"<div style='font-size:12px;color:#6b7280;margin-top:4px'>"
                f"Due {s.next_due_date}</div></div>",
                unsafe_allow_html=True,
            )

            log_key = f"dash_log_{s.id}"
            b1, b2, b3, _pad = st.columns([1, 1, 1, 3])
            if b1.button("✓ Done", key=f"dash_done_{s.id}", type="primary",
                         use_container_width=True):
                st.session_state[log_key] = True
                st.rerun()
            if b2.button("⏭ Skip", key=f"dash_skip_{s.id}", use_container_width=True):
                new_date = sched.advance_schedule(s.id)
                st.toast(f"Skipped — next due {new_date}", icon="⏭")
                st.rerun()
            if b3.button("⏸ Pause", key=f"dash_pause_{s.id}", use_container_width=True):
                sched.deactivate_schedule(s.id)
                st.toast("Schedule paused.", icon="⏸")
                st.rerun()

            if st.session_state.get(log_key):
                with st.form(f"dash_log_form_{s.id}", clear_on_submit=True, border=True):
                    st.markdown(f"**Log completion — {s.task_description}**")
                    la1, la2 = st.columns(2)
                    ld_date = la1.date_input("Completion date", value=date.today(),
                                             key=f"dash_log_date_{s.id}")
                    ld_cost = la2.number_input("Cost (CAD)", min_value=0.0, value=0.0,
                                               step=0.01, format="%.2f",
                                               key=f"dash_log_cost_{s.id}")
                    ld_notes = st.text_area("Notes", height=60, key=f"dash_log_notes_{s.id}")
                    lb1, lb2 = st.columns(2)
                    l_sub = lb1.form_submit_button("Save & Advance", type="primary",
                                                   use_container_width=True)
                    l_can = lb2.form_submit_button("Cancel", use_container_width=True)

                if l_sub:
                    hist.add_log(MaintenanceLog(
                        device_id=s.device_id,
                        service_type_id=s.service_type_id,
                        task_performed=s.task_description,
                        completion_date=str(ld_date),
                        cost_cad=float(ld_cost),
                        notes=ld_notes or None,
                    ))
                    new_date = sched.advance_schedule(s.id)
                    st.session_state.pop(log_key, None)
                    st.toast(f"Logged — next due {new_date}", icon="✅")
                    st.rerun()
                if l_can:
                    st.session_state.pop(log_key, None)
                    st.rerun()


def _device_card(d: Device, device_schedules: list) -> None:
    """Device grid card — design §3 Devices card."""
    upcoming = [s for s in device_schedules if s.is_active]
    next_sched = min(upcoming, key=lambda s: days_until_due(s.next_due_date)) if upcoming else None
    days_val = days_until_due(next_sched.next_due_date) if next_sched else None
    sinfo = status_info(days_val)
    dot_color = STATUS_STYLES[sinfo["status"]]["dot"]

    warranty_expiring = False
    if d.warranty_expiry:
        try:
            wdays = (date.fromisoformat(d.warranty_expiry) - date.today()).days
            warranty_expiring = 0 <= wdays <= 60
        except Exception:
            pass

    with st.container(border=True):
        st.markdown(
            f"<div style='height:4px;background:{dot_color};"
            f"margin:-16px -16px 12px -16px;border-radius:12px 12px 0 0'></div>",
            unsafe_allow_html=True,
        )
        archived_tag = (
            "<span class='hmt-pill' style='background:#fef2f2;color:#dc2626;"
            "border-color:#fecaca;margin-left:6px'>Archived</span>"
            if d.is_archived else ""
        )
        st.markdown(
            f"<div style='font-size:16px;font-weight:700;color:#1c1c1e'>"
            f"{d.name}{archived_tag}</div>"
            f"<div style='font-size:13px;color:#6b7280;margin-top:2px'>"
            f"{d.model or '—'}</div>",
            unsafe_allow_html=True,
        )

        pills = [f'<span class="hmt-pill">{d.category}</span>',
                 badge_html(sinfo["status"], sinfo["label"])]
        if warranty_expiring:
            pills.append(badge_html("soon", "Warranty expiring"))
        st.markdown(
            "<div style='margin-top:10px;display:flex;flex-wrap:wrap;gap:6px'>"
            + "".join(pills)
            + "</div>",
            unsafe_allow_html=True,
        )

        spend_total = hist.total_cost(d.id)
        spend_ytd   = hist.total_cost_this_year(d.id)
        st.markdown(
            f"<div style='margin-top:12px;display:flex;gap:18px'>"
            f"<div><div class='hmt-spec-label'>Spend</div>"
            f"<div class='hmt-spec-value'>{_money(spend_total)}</div></div>"
            f"<div><div class='hmt-spec-label'>YTD</div>"
            f"<div class='hmt-spec-value'>{_money(spend_ytd)}</div></div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        if st.button("Open ↗", key=f"dev_open_{d.id}", use_container_width=True):
            _device_dialog(d)


# ── Log-entry dialog ──────────────────────────────────────────────────────────

@st.dialog("Log Entry", width="large")
def _log_dialog(log: MaintenanceLog):
    st.markdown(f"### {log.device_name}")
    meta = log.completion_date
    if log.service_type_name:
        meta += f"  ·  {log.service_type_name}"
    st.caption(meta)

    dm1, dm2 = st.columns(2)
    dm1.metric("Cost", _money(log.cost_cad))
    dm2.metric("Task", log.task_performed[:40] + ("…" if len(log.task_performed) > 40 else ""))
    st.divider()

    dev_stypes = svcs.list_service_types(log.device_id)
    svc_map = {"— none / manual —": None} | {s.name: s.id for s in dev_stypes}
    svc_keys = list(svc_map.keys())
    cur_svc_idx = 0
    for i, (k, v) in enumerate(svc_map.items()):
        if v == log.service_type_id:
            cur_svc_idx = i
            break

    with st.form("edit_log_dlg_form"):
        el_svc  = st.selectbox("Service type", svc_keys, index=cur_svc_idx)
        ela1, ela2 = st.columns(2)
        el_task = ela1.text_input("Task performed", value=log.task_performed)
        try:    el_date_val = date.fromisoformat(log.completion_date)
        except: el_date_val = date.today()
        el_date = ela2.date_input("Completion date", value=el_date_val)
        elb1, elb2 = st.columns(2)
        el_cost = elb1.number_input("Cost (CAD)", min_value=0.0,
                                    value=float(log.cost_cad), step=0.01, format="%.2f")
        el_src  = elb2.text_input("Sourcing", value=log.sourcing_info or "")
        el_notes = st.text_area("Notes", value=log.notes or "", height=60)

        if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
            log.service_type_id = svc_map[el_svc]
            log.task_performed  = el_task
            log.completion_date = str(el_date)
            log.cost_cad        = float(el_cost)
            log.sourcing_info   = el_src or None
            log.notes           = el_notes or None
            hist.update_log(log)
            st.toast("Entry updated.", icon="✅")
            st.rerun()

    st.divider()
    ga1, ga2, ga3 = st.columns([1, 1, 3])
    with ga1:
        if st.button("Delete", type="secondary", key=f"ldlg_del_{log.id}", use_container_width=True):
            _delete_dialog(f"{log.completion_date} · {log.task_performed}", "log", log.id)


# ── Schedule dialog ───────────────────────────────────────────────────────────

@st.dialog("Schedule Details", width="large")
def _schedule_dialog(s: Schedule):
    st.markdown(f"### {s.device_name}  ·  {s.task_description}")
    st.caption(
        (f"Service type: {s.service_type_name}  · " if s.service_type_name else "")
        + ("✅ Active" if s.is_active else "⏸ Paused")
    )

    dm1, dm2, dm3 = st.columns(3)
    dm1.metric("Next Due", s.next_due_date)
    dm2.metric("Status", _status(days_until_due(s.next_due_date)))
    dm3.metric("Repeats", _freq(s.frequency_days))
    st.divider()

    with st.form("edit_sched_dlg_form"):
        es_task = st.text_input("Task description", value=s.task_description)
        esa1, esa2 = st.columns(2)
        try:    es_due_val = date.fromisoformat(s.next_due_date)
        except: es_due_val = date.today()
        es_due  = esa1.date_input("Next due date", value=es_due_val)
        es_freq = esa2.number_input("Frequency (days)", min_value=1, value=s.frequency_days)

        if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
            s.task_description = es_task
            s.next_due_date    = str(es_due)
            s.frequency_days   = int(es_freq)
            sched.update_schedule(s)
            st.toast("Schedule updated.", icon="✅")
            st.rerun()

    st.divider()
    ga1, ga2, ga3 = st.columns([1, 1, 3])
    with ga1:
        if st.button("Delete", type="secondary", key=f"sdlg_del_{s.id}", use_container_width=True):
            _delete_dialog(f"{s.device_name} · {s.task_description}", "schedule", s.id)


# ── Delete dialog ─────────────────────────────────────────────────────────────

@st.dialog("Confirm Delete")
def _delete_dialog(label: str, entity: str, entity_id: int):
    st.markdown(f"Delete **{label}**?")
    if entity == "device":
        st.caption("All linked maintenance history and schedules will also be deleted.")
    st.write("")
    c1, c2 = st.columns(2)
    if c1.button("Delete", type="primary", key="dlg_confirm", use_container_width=True):
        if entity == "device":
            inv.delete_device(entity_id)
        elif entity == "log":
            hist.delete_log(entity_id)
        elif entity == "schedule":
            sched.delete_schedule(entity_id)
        st.rerun()
    if c2.button("Cancel", key="dlg_cancel", use_container_width=True):
        st.rerun()


# ── Device dialog ─────────────────────────────────────────────────────────────

@st.dialog("Device Details", width="large")
def _device_dialog(device: Device):
    recent_logs = hist.list_logs(device_id=device.id, limit=10)
    last_svc = recent_logs[0] if recent_logs else None
    dev_schedules = [s for s in sched.list_schedules(active_only=False) if s.device_id == device.id]
    next_sched = min(
        [s for s in dev_schedules if s.is_active],
        key=lambda s: days_until_due(s.next_due_date),
        default=None,
    )

    head_pill = (
        f'<span class="hmt-pill">{device.category}</span>'
        + (' <span class="hmt-pill" style="background:#fef2f2;color:#dc2626;'
           'border-color:#fecaca;margin-left:6px">Archived</span>' if device.is_archived else "")
    )
    st.markdown(
        f"<div style='font-size:22px;font-weight:800;color:#1c1c1e'>{device.name}</div>"
        f"<div style='margin-top:4px'>{head_pill}</div>",
        unsafe_allow_html=True,
    )

    # ── Specs grid (row 1): Model · Serial · Purchased · Warranty ─────────────
    s1, s2, s3, s4 = st.columns(4)
    for col, label, value in [
        (s1, "Model",     device.model or "—"),
        (s2, "Serial",    device.serial_number or "—"),
        (s3, "Purchased", device.purchase_date or "—"),
        (s4, "Warranty",  device.warranty_expiry or "—"),
    ]:
        col.markdown(
            f"<div class='hmt-spec-label'>{label}</div>"
            f"<div class='hmt-spec-value'>{value}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Metrics row: Total · YTD · Next Due · Last Service ────────────────────
    m1, m2, m3, m4 = st.columns(4)
    next_due_val = next_sched.next_due_date if next_sched else "—"
    last_svc_val = last_svc.completion_date if last_svc else "—"
    for col, label, value in [
        (m1, "Total Spend",  _money(hist.total_cost(device.id))),
        (m2, "YTD Spend",    _money(hist.total_cost_this_year(device.id))),
        (m3, "Next Due",     next_due_val),
        (m4, "Last Service", last_svc_val),
    ]:
        col.markdown(
            f"<div class='hmt-spec-label'>{label}</div>"
            f"<div class='hmt-spec-value'>{value}</div>",
            unsafe_allow_html=True,
        )

    if device.notes:
        st.markdown(
            f"<div class='hmt-notes'><strong>Notes</strong><br>{device.notes}</div>",
            unsafe_allow_html=True,
        )

    # ── Edit form (collapsed by default to reduce dialog clutter) ─────────────
    with st.expander("✎ Edit device", expanded=False):
        with st.form("device_detail_form"):
            fa1, fa2 = st.columns(2)
            ed_name   = fa1.text_input("Device name *", value=device.name)
            ed_cat    = fa2.selectbox("Category *", CATEGORIES, index=CATEGORIES.index(device.category))
            fb1, fb2  = st.columns(2)
            ed_model  = fb1.text_input("Model", value=device.model or "")
            ed_serial = fb2.text_input("Serial number", value=device.serial_number or "")
            fc1, fc2  = st.columns(2)
            try:    pd_val = date.fromisoformat(device.purchase_date) if device.purchase_date else None
            except: pd_val = None
            ed_pdate  = fc1.date_input("Purchase date", value=pd_val)
            try:    we_val = date.fromisoformat(device.warranty_expiry) if device.warranty_expiry else None
            except: we_val = None
            ed_wexp   = fc2.date_input("Warranty expiry", value=we_val)
            ed_notes  = st.text_area("Notes", value=device.notes or "", height=70)

            if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
                if not ed_name:
                    st.error("Device name is required.")
                else:
                    device.name            = ed_name
                    device.category        = ed_cat
                    device.model           = ed_model or None
                    device.serial_number   = ed_serial or None
                    device.purchase_date   = str(ed_pdate) if ed_pdate else None
                    device.warranty_expiry = str(ed_wexp) if ed_wexp else None
                    device.notes           = ed_notes or None
                    inv.update_device(device)
                    st.toast("Device updated.", icon="✅")
                    st.rerun()

    # ── Service Types ──────────────────────────────────────────────────────────
    st.divider()
    sc1, sc2 = st.columns([4, 1])
    sc1.markdown("**Service Types**")
    add_key = f"show_st_add_{device.id}"
    if sc2.button("＋ Add", key=f"st_add_toggle_{device.id}", use_container_width=True):
        st.session_state[add_key] = not st.session_state.get(add_key, False)

    if st.session_state.get(add_key):
        with st.container(border=True):
            with st.form(f"add_st_form_{device.id}", clear_on_submit=True):
                st_name  = st.text_input("Service name *", placeholder="e.g. Filter Replacement")
                sta1, sta2 = st.columns(2)
                st_freq  = sta1.number_input("Repeat every (days) *", min_value=1, value=90)
                st_first_due = sta2.date_input("First due date *",
                                               value=date.today() + timedelta(days=90))
                stb1, stb2 = st.columns(2)
                st_parts = stb1.text_input("Part numbers", placeholder="Comma-separated")
                st_tut   = stb2.text_input("Tutorial URL")
                stc1, stc2 = st.columns(2)
                st_pur   = stc1.text_input("Purchase URL")
                st_notes = stc2.text_area("Notes", height=60)
                std1, std2 = st.columns(2)
                st_sub = std1.form_submit_button("Add Service Type", type="primary", use_container_width=True)
                st_can = std2.form_submit_button("Cancel", use_container_width=True)

            if st_sub:
                if not st_name:
                    st.error("Service name is required.")
                else:
                    svcs.add_service_type(
                        ServiceType(
                            device_id=device.id,
                            name=st_name,
                            frequency_days=int(st_freq),
                            part_numbers=[p.strip() for p in st_parts.split(",") if p.strip()],
                            tutorial_url=st_tut or None,
                            purchase_url=st_pur or None,
                            notes=st_notes or None,
                        ),
                        first_due_date=str(st_first_due),
                    )
                    st.session_state[add_key] = False
                    st.toast("Service type added.", icon="✅")
            if st_can:
                st.session_state[add_key] = False

    service_types = svcs.list_service_types(device.id)
    if service_types:
        for stype in service_types:
            with st.container(border=True):
                s1, s2, s3 = st.columns([4, 1, 1])
                s1.markdown(f"**{stype.name}**  ·  {_freq(stype.frequency_days)}")
                if stype.part_numbers:
                    s1.caption("Parts: " + ", ".join(stype.part_numbers))
                if stype.tutorial_url:
                    s1.caption(f"[Tutorial]({stype.tutorial_url})")
                edit_key = f"edit_st_{stype.id}"
                if s2.button("Edit", key=f"st_edit_{stype.id}", use_container_width=True):
                    st.session_state[edit_key] = not st.session_state.get(edit_key, False)
                if s3.button("Delete", key=f"st_del_{stype.id}", type="secondary", use_container_width=True):
                    svcs.delete_service_type(stype.id)
                    st.toast("Service type deleted.", icon="🗑")
                if st.session_state.get(edit_key):
                    with st.form(f"edit_st_form_{stype.id}"):
                        e_name  = st.text_input("Name", value=stype.name)
                        ea1, ea2 = st.columns(2)
                        e_freq  = ea1.number_input("Interval (days)", min_value=1, value=stype.frequency_days)
                        e_parts = ea2.text_input("Part numbers", value=", ".join(stype.part_numbers))
                        eb1, eb2 = st.columns(2)
                        e_tut   = eb1.text_input("Tutorial URL", value=stype.tutorial_url or "")
                        e_pur   = eb2.text_input("Purchase URL", value=stype.purchase_url or "")
                        e_notes = st.text_area("Notes", value=stype.notes or "", height=60)
                        if st.form_submit_button("Save", type="primary"):
                            stype.name          = e_name
                            stype.frequency_days = int(e_freq)
                            stype.part_numbers  = [p.strip() for p in e_parts.split(",") if p.strip()]
                            stype.tutorial_url  = e_tut or None
                            stype.purchase_url  = e_pur or None
                            stype.notes         = e_notes or None
                            svcs.update_service_type(stype)
                            st.session_state[edit_key] = False
                            st.toast("Service type updated.", icon="✅")
    else:
        st.caption("No service types yet. Add one to define maintenance intervals and parts.")

    # ── Maintenance History ────────────────────────────────────────────────────
    st.divider()
    with st.expander(f"🔧 Maintenance History ({len(recent_logs)} recent)"):
        if recent_logs:
            h1, h2, h3, h4 = st.columns([1, 3, 2, 1])
            for col, lbl in zip([h1, h2, h3, h4], ["Date", "Task", "Service Type", "Cost"]):
                col.markdown(
                    f"<span style='font-size:0.75rem;text-transform:uppercase;"
                    f"color:#64748b;font-weight:600;letter-spacing:0.05em'>{lbl}</span>",
                    unsafe_allow_html=True,
                )
            st.markdown("<hr style='margin:4px 0 8px'>", unsafe_allow_html=True)
            for l in recent_logs:
                rc = st.columns([1, 3, 2, 1])
                rc[0].caption(l.completion_date)
                rc[1].markdown(f"<span style='font-size:0.85rem'>{l.task_performed}</span>",
                               unsafe_allow_html=True)
                rc[2].caption(l.service_type_name or "—")
                rc[3].caption(_money(l.cost_cad) if l.cost_cad else "—")
        else:
            st.caption("No maintenance history yet.")

    st.divider()
    confirm_key = f"dev_confirm_del_{device.id}"
    ga1, ga2, _ = st.columns([1, 1, 3])
    with ga1:
        arch_label = "Restore" if device.is_archived else "Archive"
        if st.button(arch_label, key=f"dlg_arch_{device.id}", use_container_width=True):
            inv.unarchive_device(device.id) if device.is_archived else inv.archive_device(device.id)
            st.toast(f"Device {'restored' if device.is_archived else 'archived'}.", icon="📦")
            st.rerun()
    with ga2:
        if st.button("Delete", key=f"dlg_del_{device.id}", type="secondary", use_container_width=True):
            st.session_state[confirm_key] = True
            st.rerun()

    if st.session_state.get(confirm_key):
        with st.container(border=True):
            st.markdown(
                f"<div style='color:#991b1b;font-weight:600'>Delete {device.name}?</div>"
                f"<div style='color:#7f1d1d;font-size:13px;margin-top:2px'>"
                f"All linked maintenance history and schedules will also be deleted.</div>",
                unsafe_allow_html=True,
            )
            cc1, cc2, _ = st.columns([1, 1, 3])
            if cc1.button("Confirm Delete", key=f"dev_del_confirm_{device.id}",
                          type="primary", use_container_width=True):
                inv.delete_device(device.id)
                st.session_state.pop(confirm_key, None)
                st.rerun()
            if cc2.button("Cancel", key=f"dev_del_cancel_{device.id}",
                          use_container_width=True):
                st.session_state.pop(confirm_key, None)
                st.rerun()


# ── Sidebar nav (design §2.1) ─────────────────────────────────────────────────

NAV_ITEMS = [
    ("dashboard",    "⌂ Dashboard"),
    ("devices",      "⊞ Devices"),
    ("history",      "⚙ History"),
    ("schedules",    "◷ Schedules"),
    ("integrations", "◉ Integrations"),
    ("roadmap",      "◈ Roadmap"),
]

if "nav" not in st.session_state:
    st.session_state.nav = "dashboard"

_all_sched_sidebar = sched.list_schedules()
_overdue_count = sum(1 for s in _all_sched_sidebar if days_until_due(s.next_due_date) < 0)

with st.sidebar:
    st.markdown(
        '<div class="hmt-prop-switch">'
        '<div class="icon">🏠</div>'
        '<div><div class="prop-name">Squamish Home</div>'
        '<div class="prop-sub">Squamish, BC</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    for view_id, label in NAV_ITEMS:
        is_active = st.session_state.nav == view_id
        suffix = f"  ({_overdue_count})" if view_id == "dashboard" and _overdue_count else ""
        if st.button(
            label + suffix,
            key=f"nav_{view_id}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.nav = view_id
            st.rerun()

    st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="hmt-user">'
        '<div class="avatar">S</div>'
        '<div><div class="name">Sergey P.</div>'
        '<div class="role">Owner</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    logout_button()

nav = st.session_state.nav

# ══════════════════════════════════════════════════════════════════════════════
# VIEW — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

if nav == "dashboard":
    devices   = inv.list_devices()
    active    = sched.list_schedules()  # active_only=True by default
    overdue   = sorted([s for s in active if days_until_due(s.next_due_date) < 0],
                       key=lambda s: days_until_due(s.next_due_date))
    due_today = [s for s in active if days_until_due(s.next_due_date) == 0]
    due_week  = sorted([s for s in active if 1 <= days_until_due(s.next_due_date) <= 7],
                       key=lambda s: days_until_due(s.next_due_date))
    due_month = sorted([s for s in active if 7 < days_until_due(s.next_due_date) <= 30],
                       key=lambda s: days_until_due(s.next_due_date))
    this_week_count = len(overdue) + len(due_today) + len(due_week)

    # ── Stat row (design §3, tinted for urgency) ──────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(stat_card_html("Active Devices", str(len(devices))),
                unsafe_allow_html=True)
    c2.markdown(stat_card_html("Overdue", str(len(overdue)),
                               tone="danger" if overdue else "neutral"),
                unsafe_allow_html=True)
    c3.markdown(stat_card_html("Due This Week", str(len(due_today) + len(due_week)),
                               tone="warn" if (due_today or due_week) else "neutral"),
                unsafe_allow_html=True)
    c4.markdown(stat_card_html("Spent This Year", _money(hist.total_cost_this_year())),
                unsafe_allow_html=True)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])

    with col_l:
        if not (overdue or due_today or due_week or due_month):
            st.info("No tasks due in the next 30 days. 🎉")
        else:
            _dash_task_group("Needs Attention", overdue + due_today)
            _dash_task_group("Due This Week",   due_week)
            _dash_task_group("Later This Month", due_month)

    with col_r:
        st.markdown(
            "<h4 style='margin:0 0 12px;font-size:14px;text-transform:uppercase;"
            "letter-spacing:0.06em;font-weight:700;color:#1c1c1e'>Recent Activity</h4>",
            unsafe_allow_html=True,
        )
        logs = hist.list_logs(limit=5)
        if not logs:
            st.caption("No maintenance history yet.")
        else:
            for l in logs:
                with st.container(border=True):
                    st.markdown(
                        f"<div style='font-size:11px;color:#9ca3af;font-weight:600;"
                        f"text-transform:uppercase;letter-spacing:0.04em'>{l.completion_date}</div>"
                        f"<div style='font-size:14px;font-weight:600;color:#1c1c1e;"
                        f"margin:2px 0 1px'>{l.device_name}</div>"
                        f"<div style='font-size:13px;color:#4b5563'>{l.task_performed}</div>"
                        f"<div style='font-size:13px;color:#e8823a;font-weight:700;"
                        f"margin-top:4px'>{_money(l.cost_cad) if l.cost_cad else '—'}</div>",
                        unsafe_allow_html=True,
                    )



# ══════════════════════════════════════════════════════════════════════════════
# VIEW — DEVICES
# ══════════════════════════════════════════════════════════════════════════════

elif nav == "devices":
    ih1, ih2 = st.columns([5, 1])
    ih1.subheader("Devices")
    if ih2.button("＋ Add Device", type="primary", use_container_width=True, key="inv_add_toggle"):
        st.session_state.show_inv_add = not st.session_state.get("show_inv_add", False)

    if st.session_state.get("show_inv_add"):
        with st.container(border=True):
            st.markdown("**New Device**")
            with st.form("add_device_form", clear_on_submit=True):
                a1, a2 = st.columns(2)
                d_name   = a1.text_input("Device name *", placeholder="e.g. Main Fridge")
                d_cat    = a2.selectbox("Category *", CATEGORIES)
                b1, b2   = st.columns(2)
                d_model  = b1.text_input("Model", placeholder="e.g. WRF535SWHZ")
                d_serial = b2.text_input("Serial number")
                c1, c2   = st.columns(2)
                d_pdate  = c1.date_input("Purchase date", value=None)
                d_wexp   = c2.date_input("Warranty expiry", value=None)
                d_notes  = st.text_area("Notes", height=70, placeholder="Tips, BC code requirements, etc.")
                fc1, fc2 = st.columns(2)
                submitted = fc1.form_submit_button("Save Device", type="primary", use_container_width=True)
                cancelled = fc2.form_submit_button("Cancel", use_container_width=True)

            if submitted:
                if not d_name:
                    st.error("Device name is required.")
                else:
                    new_id = inv.add_device(Device(
                        name=d_name, category=d_cat,
                        model=d_model or None, serial_number=d_serial or None,
                        purchase_date=str(d_pdate) if d_pdate else None,
                        warranty_expiry=str(d_wexp) if d_wexp else None,
                        notes=d_notes or None,
                    ))
                    st.session_state.show_inv_add = False
                    st.session_state["open_device_id"] = new_id
                    st.rerun()
            if cancelled:
                st.session_state.show_inv_add = False
                st.rerun()

    # Auto-open dialog for a freshly created device so user can add service types immediately
    _open_id = st.session_state.pop("open_device_id", None)
    if _open_id:
        _new_dev = inv.get_device(_open_id)
        if _new_dev:
            _device_dialog(_new_dev)

    # Filters
    f1, f2 = st.columns([4, 1])
    cat_filter    = f1.selectbox("Filter by category", ["All categories"] + CATEGORIES,
                                  key="inv_cat", label_visibility="collapsed")
    show_archived = f2.checkbox("Show archived", key="inv_archived")

    devs = inv.list_devices(
        category=None if cat_filter == "All categories" else cat_filter,
        include_archived=show_archived,
    )

    if devs:
        # Pre-fetch all schedules once so each card can filter locally (avoids N queries)
        all_schedules = sched.list_schedules(active_only=False)
        sched_by_dev: dict = {}
        for s in all_schedules:
            sched_by_dev.setdefault(s.device_id, []).append(s)

        COLS = 3
        for i in range(0, len(devs), COLS):
            row = st.columns(COLS)
            for col, d in zip(row, devs[i:i + COLS]):
                with col:
                    _device_card(d, sched_by_dev.get(d.id, []))
    else:
        st.info("No devices found. Add your first device above.")


# ══════════════════════════════════════════════════════════════════════════════
# VIEW — HISTORY
# ══════════════════════════════════════════════════════════════════════════════

elif nav == "history":
    hh1, hh2 = st.columns([5, 1])
    hh1.subheader("Maintenance History")
    if hh2.button("＋ Log Entry", type="primary", use_container_width=True, key="hist_add_toggle"):
        st.session_state.show_hist_add = not st.session_state.get("show_hist_add", False)
        st.session_state.pop("prefill_log", None)

    # ── Due Tasks — amber banner with compact chip row (design §3 History) ────
    action_items = sched.get_due_schedules(days_ahead=7)
    if action_items:
        st.markdown(
            "<div style='background:#fffbeb;border:1px solid #fde68a;border-left:3px solid #f59e0b;"
            "border-radius:10px;padding:10px 14px;margin-bottom:14px'>"
            f"<div style='font-size:13px;font-weight:700;color:#78350f;margin-bottom:8px'>"
            f"Due & overdue ({len(action_items)}) — click a chip to prefill the log form</div>",
            unsafe_allow_html=True,
        )
        per_row = 3
        for row_start in range(0, len(action_items), per_row):
            row = action_items[row_start:row_start + per_row]
            cols = st.columns(per_row)
            for col, s in zip(cols, row):
                days = days_until_due(s.next_due_date)
                label = f"{s.device_name} · {s.task_description} · {status_info(days)['label']}"
                if col.button(label, key=f"due_chip_{s.id}", use_container_width=True):
                    st.session_state["prefill_log"] = {
                        "device_id": s.device_id,
                        "task": s.task_description,
                        "schedule_id": s.id,
                        "service_type_id": s.service_type_id,
                    }
                    st.session_state.show_hist_add = True
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Log Expense form ──────────────────────────────────────────────────────
    prefill           = st.session_state.get("prefill_log", {})
    prefill_dev_id    = prefill.get("device_id")
    prefill_task      = prefill.get("task", "")
    prefill_svc_id    = prefill.get("service_type_id")
    completing_sched  = prefill.get("schedule_id")

    if st.session_state.get("show_hist_add"):
        with st.container(border=True):
            header = "**Complete Task**" if completing_sched else "**New Expense Entry**"
            st.markdown(header)

            # Device selector is OUTSIDE the form so service types update reactively
            log_devs  = inv.list_devices()
            dev_map   = {f"{d.name}  —  {d.category}": d.id for d in log_devs}
            dev_keys  = list(dev_map.keys())
            default_dev_idx = 0
            if prefill_dev_id:
                for i, k in enumerate(dev_keys):
                    if dev_map[k] == prefill_dev_id:
                        default_dev_idx = i
                        break
            log_dev_sel    = st.selectbox("Device *", dev_keys,
                                          index=default_dev_idx, key="hist_log_device")
            selected_dev_id = dev_map[log_dev_sel]

            # Service types for the selected device
            dev_stypes = svcs.list_service_types(selected_dev_id)
            svc_map    = {"— none / manual —": None} | {s.name: s.id for s in dev_stypes}
            svc_keys   = list(svc_map.keys())
            default_svc_idx = 0
            if prefill_svc_id:
                for i, (k, v) in enumerate(svc_map.items()):
                    if v == prefill_svc_id:
                        default_svc_idx = i
                        break

            with st.form("add_log_form", clear_on_submit=True):
                la1, la2  = st.columns(2)
                log_svc   = la1.selectbox("Service type", svc_keys, index=default_svc_idx)
                log_date  = la2.date_input("Completion date", value=date.today())
                log_task  = st.text_input("Task performed *", value=prefill_task,
                                          placeholder="e.g. Replaced furnace filter")
                lb1, lb2  = st.columns(2)
                log_cost  = lb1.number_input("Cost (CAD)", min_value=0.0, value=0.0,
                                             step=0.01, format="%.2f")
                log_sourcing = lb2.text_input("Sourcing", placeholder="Vendor or URL")
                log_notes = st.text_area("Notes", height=60,
                                         placeholder="Installation tips for next time")
                lc1, lc2  = st.columns(2)
                l_submitted = lc1.form_submit_button("Save Entry", type="primary",
                                                     use_container_width=True)
                l_cancelled = lc2.form_submit_button("Cancel", use_container_width=True)

            if l_submitted:
                if not log_task:
                    st.error("Task description is required.")
                else:
                    hist.add_log(MaintenanceLog(
                        device_id=selected_dev_id,
                        service_type_id=svc_map[log_svc],
                        task_performed=log_task,
                        completion_date=str(log_date),
                        cost_cad=float(log_cost),
                        sourcing_info=log_sourcing or None,
                        notes=log_notes or None,
                    ))
                    if completing_sched:
                        new_date = sched.advance_schedule(completing_sched)
                        st.toast(f"Logged and schedule advanced to {new_date}.", icon="✅")
                    else:
                        st.toast("Expense logged.", icon="✅")
                    st.session_state.pop("prefill_log", None)
                    st.session_state.pop("hist_log_device", None)
                    st.session_state.show_hist_add = False
                    st.rerun()
            if l_cancelled:
                st.session_state.pop("prefill_log", None)
                st.session_state.pop("hist_log_device", None)
                st.session_state.show_hist_add = False
                st.rerun()

    # ── Filter bar ────────────────────────────────────────────────────────────
    all_devs_h    = inv.list_devices(include_archived=True)
    dev_flt_opts  = {"All devices": None} | {d.name: d.id for d in all_devs_h}
    dev_category  = {d.id: d.category for d in all_devs_h}

    hf1, hf2, hf3, hf4, hf5 = st.columns([2, 2, 2, 2, 2])
    dev_flt_sel   = hf1.selectbox("Device", list(dev_flt_opts.keys()),
                                   key="hist_dev_flt", label_visibility="collapsed")
    cat_flt_sel   = hf2.selectbox("Category", ["All categories"] + CATEGORIES,
                                   key="hist_cat_flt", label_visibility="collapsed")
    date_from     = hf3.date_input("From", value=None, key="hist_date_from",
                                    label_visibility="collapsed", format="YYYY-MM-DD")
    date_to       = hf4.date_input("To", value=None, key="hist_date_to",
                                    label_visibility="collapsed", format="YYYY-MM-DD")
    hist_limit    = hf5.selectbox("Show", LIMIT_OPTIONS, index=1,
                                   key="hist_limit", label_visibility="collapsed",
                                   format_func=lambda x: f"Last {x}")

    flt_dev_id = dev_flt_opts[dev_flt_sel]
    logs = hist.list_logs(device_id=flt_dev_id, limit=hist_limit)

    if cat_flt_sel != "All categories":
        logs = [l for l in logs if dev_category.get(l.device_id) == cat_flt_sel]
    if date_from:
        logs = [l for l in logs if l.completion_date >= str(date_from)]
    if date_to:
        logs = [l for l in logs if l.completion_date <= str(date_to)]

    filtered_spend = sum(l.cost_cad for l in logs)
    st.markdown(
        f"<div style='display:flex;justify-content:flex-end;gap:18px;margin:6px 0 10px'>"
        f"<div><span class='hmt-spec-label'>Entries</span> "
        f"<span class='hmt-spec-value' style='display:inline;margin-left:4px'>{len(logs)}</span></div>"
        f"<div><span class='hmt-spec-label'>Spend</span> "
        f"<span class='hmt-spec-value' style='display:inline;margin-left:4px;color:#e8823a'>"
        f"{_money(filtered_spend)}</span></div></div>",
        unsafe_allow_html=True,
    )

    # ── Flat card list ────────────────────────────────────────────────────────
    if not logs:
        st.info("No entries match the current filters.")
    else:
        for l in logs:
            with st.container(border=True):
                r1, r2, r3 = st.columns([4, 2, 1])
                r1.markdown(
                    f"<div style='font-size:11px;color:#9ca3af;text-transform:uppercase;"
                    f"letter-spacing:0.04em;font-weight:600'>"
                    f"{l.completion_date}  ·  {l.device_name}</div>"
                    f"<div style='font-size:15px;font-weight:600;color:#1c1c1e;margin-top:2px'>"
                    f"{l.task_performed}</div>"
                    + (f"<div style='font-size:12px;color:#6b7280;margin-top:2px'>"
                       f"{l.service_type_name}</div>" if l.service_type_name else ""),
                    unsafe_allow_html=True,
                )
                r2.markdown(
                    f"<div style='text-align:right'>"
                    f"<div class='hmt-spec-label'>Cost</div>"
                    f"<div class='hmt-spec-value' style='color:#e8823a'>"
                    f"{_money(l.cost_cad) if l.cost_cad else '—'}</div></div>",
                    unsafe_allow_html=True,
                )
                if r3.button("Open ↗", key=f"log_open_{l.id}", use_container_width=True):
                    _log_dialog(l)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW — SCHEDULES
# ══════════════════════════════════════════════════════════════════════════════

elif nav == "schedules":
    sh1, sh2 = st.columns([5, 1])
    sh1.subheader("Maintenance Schedules")
    if sh2.button("＋ Add Manual", type="secondary", use_container_width=True, key="sched_add_toggle"):
        st.session_state.show_sched_add = not st.session_state.get("show_sched_add", False)

    if st.session_state.get("show_sched_add"):
        with st.container(border=True):
            st.markdown("**New Manual Schedule**")
            st.caption("Schedules are normally created automatically when you add a service type to a device.")
            sched_devs    = inv.list_devices()
            sched_dev_map = {f"{d.name}  —  {d.category}": d for d in sched_devs}
            with st.form("add_sched_form", clear_on_submit=True):
                sa1, sa2 = st.columns(2)
                s_dev_sel = sa1.selectbox("Device *", list(sched_dev_map.keys()))
                s_freq    = sa2.number_input("Repeat every (days) *", min_value=1, value=90)
                s_task    = st.text_input("Task description *",
                                          placeholder="e.g. Replace furnace filter")
                s_due     = st.date_input("First due date",
                                          value=date.today() + timedelta(days=30))
                sc1, sc2  = st.columns(2)
                s_sub     = sc1.form_submit_button("Save Schedule", type="primary",
                                                   use_container_width=True)
                s_can     = sc2.form_submit_button("Cancel", use_container_width=True)

            if s_sub:
                if not s_task:
                    st.error("Task description is required.")
                else:
                    chosen = sched_dev_map[s_dev_sel]
                    sched.add_schedule(Schedule(
                        device_id=chosen.id,
                        task_description=s_task,
                        next_due_date=str(s_due),
                        frequency_days=int(s_freq),
                    ))
                    st.session_state.show_sched_add = False
                    st.toast("Schedule added.", icon="✅")
                    st.rerun()
            if s_can:
                st.session_state.show_sched_add = False
                st.rerun()

    sf1, _ = st.columns([3, 5])
    sched_show_all = sf1.checkbox("Show inactive schedules", key="sched_show_all")

    all_scheds = sched.list_schedules(active_only=not sched_show_all)

    if not all_scheds:
        st.info("No schedules yet. Add service types to a device to create schedules automatically.")
    else:
        # Urgency buckets (design §3 — Overdue / This Week / This Month / Later)
        buckets: dict[str, list] = {"Overdue": [], "This Week": [], "This Month": [], "Later": [], "Paused": []}
        for s in all_scheds:
            if not s.is_active:
                buckets["Paused"].append(s)
                continue
            d = days_until_due(s.next_due_date)
            if d < 0:       buckets["Overdue"].append(s)
            elif d <= 7:    buckets["This Week"].append(s)
            elif d <= 30:   buckets["This Month"].append(s)
            else:           buckets["Later"].append(s)

        for bucket in ("Overdue", "This Week", "This Month", "Later", "Paused"):
            rows = sorted(buckets[bucket], key=lambda s: days_until_due(s.next_due_date))
            if not rows:
                continue
            st.markdown(
                f"<h4 style='margin:18px 0 10px;color:#1c1c1e;font-size:14px;"
                f"text-transform:uppercase;letter-spacing:0.06em;font-weight:700;'>"
                f"{bucket}  <span style='color:#9ca3af;font-weight:500'>({len(rows)})</span></h4>",
                unsafe_allow_html=True,
            )
            for s in rows:
                days = days_until_due(s.next_due_date)
                sinfo = status_info(days) if s.is_active else {"status": "neutral", "label": "Paused"}
                with st.container(border=True):
                    r1, r2 = st.columns([5, 3])
                    r1.markdown(
                        f"<div style='font-size:11px;color:#9ca3af;text-transform:uppercase;"
                        f"letter-spacing:0.04em;font-weight:600'>{s.device_name}</div>"
                        f"<div style='font-size:15px;font-weight:600;color:#1c1c1e;margin-top:2px'>"
                        f"{s.task_description}</div>"
                        f"<div style='font-size:12px;color:#6b7280;margin-top:2px'>"
                        f"Every {_freq(s.frequency_days)} · Next {s.next_due_date}</div>",
                        unsafe_allow_html=True,
                    )
                    pills = [badge_html(sinfo["status"], sinfo["label"])]
                    if s.calendar_event_id:
                        pills.append(badge_html("blue", "🗓 Synced"))
                    r2.markdown(
                        "<div style='text-align:right;display:flex;justify-content:flex-end;"
                        "flex-wrap:wrap;gap:6px'>" + "".join(pills) + "</div>",
                        unsafe_allow_html=True,
                    )

                    b1, b2, _pad = st.columns([1, 1, 3])
                    if s.is_active:
                        if b1.button("⏸ Pause", key=f"sched_pause_{s.id}",
                                     use_container_width=True):
                            sched.deactivate_schedule(s.id)
                            st.toast("Schedule paused.", icon="⏸")
                            st.rerun()
                    else:
                        if b1.button("▶ Resume", key=f"sched_resume_{s.id}",
                                     use_container_width=True):
                            sched.activate_schedule(s.id)
                            st.toast("Schedule resumed.", icon="▶")
                            st.rerun()
                    if b2.button("Open ↗", key=f"sched_open_{s.id}",
                                 use_container_width=True):
                        _schedule_dialog(s)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW — INTEGRATIONS
# ══════════════════════════════════════════════════════════════════════════════

elif nav == "integrations":
    st.subheader("Integrations")

    # ── Google Calendar ───────────────────────────────────────────────────────
    cal_col, _ = st.columns(2)
    with cal_col:
        with st.container(border=True):
            st.markdown("### 🗓 Google Calendar")
            n_all_devs  = inv.list_devices()
            n_dev_opts  = {"All devices": None} | {d.name: d.id for d in n_all_devs}
            n_dev_sel   = st.selectbox("Target", list(n_dev_opts.keys()), key="notif_dev")
            n_force     = st.checkbox("Force re-create existing events", key="notif_force")

            linked   = [s for s in sched.list_schedules() if s.calendar_event_id]
            unlinked = [s for s in sched.list_schedules() if not s.calendar_event_id]
            st.caption(f"🗓 **{len(linked)}** linked  ·  ⬜ **{len(unlinked)}** not yet pushed")

            if st.button("Push to Calendar", type="primary", key="push_cal", use_container_width=True):
                from src.notifications import create_calendar_event
                to_push = sched.list_schedules(device_id=n_dev_opts[n_dev_sel])
                pushed = errors = 0
                with st.spinner("Pushing events…"):
                    for s in to_push:
                        if s.calendar_event_id and not n_force:
                            continue
                        dev = inv.get_device(s.device_id)
                        if not dev:
                            continue
                        # Part numbers + tutorial/purchase links live on the service type now,
                        # not the device. Pull them from the schedule's service type if any.
                        stype = svcs.get_service_type(s.service_type_id) if s.service_type_id else None
                        resource_links = {}
                        if stype:
                            if stype.tutorial_url:
                                resource_links["tutorial"] = stype.tutorial_url
                            if stype.purchase_url:
                                resource_links["purchase"] = stype.purchase_url
                        try:
                            eid = create_calendar_event(
                                device_name=dev.name, task_description=s.task_description,
                                due_date=s.next_due_date, frequency_days=s.frequency_days,
                                part_numbers=stype.part_numbers if stype else [],
                                resource_links=resource_links,
                                notes=dev.notes,
                            )
                            sched.set_calendar_event_id(s.id, eid)
                            pushed += 1
                        except Exception as e:
                            st.error(f"{dev.name}: {e}")
                            errors += 1
                if not errors:
                    st.toast(f"Pushed {pushed} event(s) to Google Calendar.", icon="🗓")
                else:
                    st.warning(f"Pushed {pushed}, failed {errors}.")
                st.rerun()

    # TODO: download schedule as a checklist (PDF or CSV export of upcoming tasks)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW — ROADMAP
# ══════════════════════════════════════════════════════════════════════════════

elif nav == "roadmap":
    st.subheader("Roadmap")
    st.caption("Where the Tracker is heading. Source of truth: `design_handoff/DESIGN.md §7`.")

    _phases = [
        ("Phase 1 — Now",    "#15803d", "#f0fdf4", [
            ("Device inventory with service types",     True),
            ("Maintenance history log",                 True),
            ("Schedule management",                     True),
            ("Google Calendar sync",                    True),
        ]),
        ("Phase 2 — Next",   "#2563eb", "#eff6ff", [
            ("AI-powered parts finder",                 False),
            ("AI-powered tutorial finder",              False),
            ("Dashboard AI chat assistant",             False),
            ("Photo upload → AI device identification", False),
            ("Amazon.ca parts linking (with referral)", False),
            ("Spend analytics & cost projections",      False),
            ("Download schedule as CSV/PDF",            False),
        ]),
        ("Phase 3 — Future", "#7c3aed", "#f5f3ff", [
            ("Multi-unit / building manager mode",      False),
            ("Shared maintenance templates per unit",   False),
            ("Individual unit owner accounts",          False),
            ("Service provider booking",                False),
        ]),
    ]

    for label, color, bg, features in _phases:
        with st.container(border=True):
            st.markdown(
                f'<span style="font-size:11px;font-weight:700;padding:3px 10px;'
                f'border-radius:20px;background:{bg};color:{color};">{label}</span>',
                unsafe_allow_html=True,
            )
            for name, done in features:
                icon = "✅" if done else "◯"
                color_txt = "#1c1c1e" if done else "#6b7280"
                st.markdown(
                    f'<div style="font-size:13px;color:{color_txt};padding:4px 0;">'
                    f'{icon} {name}</div>',
                    unsafe_allow_html=True,
                )
