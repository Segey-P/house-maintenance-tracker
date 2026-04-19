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
/* Hide Streamlit chrome */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* Metric card borders */
div[data-testid="metric-container"] {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem 1.25rem;
}
div[data-testid="metric-container"] > label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
}
div[data-testid="metric-container"] > div {
    font-size: 1.8rem;
    font-weight: 700;
}

/* Tighter tab bar */
div[data-testid="stTabs"] > div:first-child button {
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
}

/* Sidebar section headers */
.sidebar-stat { font-size: 0.85rem; color: #64748b; margin: 0; }
.sidebar-val  { font-size: 1rem; font-weight: 600; margin: 0 0 0.5rem; }
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

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🏠 Squamish Home")
    st.caption(f"📅 {date.today().strftime('%B %d, %Y')}  ·  Squamish, BC")
    st.divider()

    _all_sched  = sched.list_schedules()
    _overdue    = [s for s in _all_sched if days_until_due(s.next_due_date) < 0]
    _due_week   = [s for s in _all_sched if 0 <= days_until_due(s.next_due_date) <= 7]
    _all_devs   = inv.list_devices()

    if _overdue:
        st.error(f"⛔ {len(_overdue)} task(s) overdue")
    elif _due_week:
        st.warning(f"⚠️ {len(_due_week)} task(s) due this week")
    else:
        st.success("✅ All tasks on schedule")

    st.divider()
    st.markdown('<p class="sidebar-stat">Active devices</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-val">{len(_all_devs)}</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-stat">Total spend</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sidebar-val">{_money(hist.total_cost())}</p>', unsafe_allow_html=True)

    if _overdue:
        st.divider()
        st.markdown("**Overdue tasks**")
        for s in _overdue:
            d = abs(days_until_due(s.next_due_date))
            st.markdown(f"• {s.device_name} · {d}d ago")

    if _due_week:
        st.divider()
        st.markdown("**Due this week**")
        for s in _due_week:
            d = days_until_due(s.next_due_date)
            label = "today" if d == 0 else f"in {d}d"
            st.markdown(f"• {s.device_name} · {label}")

    st.divider()
    logout_button()

# ── Page header ───────────────────────────────────────────────────────────────

st.markdown("# 🏠 Squamish Home")
st.caption("House Maintenance Tracker")
st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────

tabs = st.tabs(["📊 Dashboard", "📱 Devices", "🔧 Maintenance", "📅 Schedules", "🔔 Notifications"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 0 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

with tabs[0]:
    devices     = inv.list_devices()
    all_sched   = sched.list_schedules()
    overdue     = [s for s in all_sched if days_until_due(s.next_due_date) < 0]
    due_week    = [s for s in all_sched if 0 <= days_until_due(s.next_due_date) <= 7]
    total_spend = hist.total_cost()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Devices", len(devices))
    c2.metric("Overdue", len(overdue),
              delta=f"action needed" if overdue else None,
              delta_color="inverse")
    c3.metric("Due This Week", len(due_week),
              delta=f"upcoming" if due_week else None,
              delta_color="off")
    c4.metric("Spent This Year", _money(hist.total_cost_this_year()))

    st.divider()
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Upcoming Tasks")
        upcoming = sched.get_due_schedules(days_ahead=60) or all_sched[:8]
        if upcoming:
            df = pd.DataFrame([
                {
                    "Device":   s.device_name,
                    "Task":     s.task_description,
                    "Due":      s.next_due_date,
                    "Status":   _status(days_until_due(s.next_due_date)),
                }
                for s in upcoming[:10]
            ])
            st.dataframe(_style_schedule(df), hide_index=True, width=680)
        else:
            st.info("No upcoming tasks in the next 60 days.")

    with col_r:
        st.subheader("Recent Activity")
        logs = hist.list_logs(limit=8)
        if logs:
            df = pd.DataFrame([
                {
                    "Date":   l.completion_date,
                    "Device": l.device_name,
                    "Task":   l.task_performed,
                    "Cost":   _money(l.cost_cad),
                }
                for l in logs
            ])
            st.dataframe(df, hide_index=True, width=680)
        else:
            st.info("No maintenance history yet. Log your first task in the Maintenance tab.")

    st.divider()
    st.subheader("🚧 Coming Soon")
    st.markdown("""
- **Download schedule** — export upcoming tasks as a printable checklist
- **Google Calendar sync** — push schedules as recurring calendar events
- **Photo import** — identify appliance from photo, auto-fill specs
""")



# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DEVICES
# ══════════════════════════════════════════════════════════════════════════════

@st.dialog("Device Details", width="large")
def _device_dialog(device: Device):
    st.markdown(f"### {device.name}")
    st.caption(device.category + (" · Archived" if device.is_archived else ""))

    recent_logs = hist.list_logs(device_id=device.id, limit=10)
    last_svc = recent_logs[0] if recent_logs else None

    dm1, dm2, dm3 = st.columns(3)
    dm1.metric("Total Spend", _money(hist.total_cost(device.id)))
    dm2.metric("Warranty Expiry", device.warranty_expiry or "—")
    if last_svc:
        dm3.metric("Last Service", last_svc.completion_date)
        dm3.caption(last_svc.service_type_name or last_svc.task_performed[:30])
    else:
        dm3.metric("Last Service", "—")
    st.divider()

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
    ga1, ga2, ga3 = st.columns([1, 1, 3])
    with ga1:
        arch_label = "Restore" if device.is_archived else "Archive"
        if st.button(arch_label, key=f"dlg_arch_{device.id}", use_container_width=True):
            inv.unarchive_device(device.id) if device.is_archived else inv.archive_device(device.id)
            st.toast(f"Device {'restored' if device.is_archived else 'archived'}.", icon="📦")
            st.rerun()
    with ga2:
        if st.button("Delete", key=f"dlg_del_{device.id}", type="secondary", use_container_width=True):
            _delete_dialog(device.name, "device", device.id)


with tabs[1]:
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
        hcols = st.columns([3, 2, 1, 1])
        for col, label in zip(hcols, ["Name", "Category", "Spend", ""]):
            col.markdown(f"<span style='font-size:0.75rem;text-transform:uppercase;color:#64748b;font-weight:600;letter-spacing:0.05em'>{label}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:4px 0 8px'>", unsafe_allow_html=True)
        for d in devs:
            with st.container():
                rc = st.columns([3, 2, 1, 1])
                name_text = f"{'🗄 ' if d.is_archived else ''}{d.name}"
                rc[0].markdown(f"**{name_text}**")
                rc[1].markdown(f"<span style='font-size:0.85rem;color:#475569'>{d.category}</span>", unsafe_allow_html=True)
                rc[2].markdown(f"<span style='font-size:0.85rem'>{_money(hist.total_cost(d.id))}</span>", unsafe_allow_html=True)
                if rc[3].button("Open ↗", key=f"dev_open_{d.id}", use_container_width=True):
                    _device_dialog(d)
            st.markdown("<hr style='margin:2px 0;border-color:#f1f5f9'>", unsafe_allow_html=True)
    else:
        st.info("No devices found. Add your first device above.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MAINTENANCE
# ══════════════════════════════════════════════════════════════════════════════

with tabs[2]:
    hh1, hh2 = st.columns([5, 1])
    hh1.subheader("Maintenance")
    if hh2.button("＋ Log Expense", type="primary", use_container_width=True, key="hist_add_toggle"):
        st.session_state.show_hist_add = not st.session_state.get("show_hist_add", False)
        st.session_state.pop("prefill_log", None)

    # ── Due Tasks ─────────────────────────────────────────────────────────────
    action_items = sched.get_due_schedules(days_ahead=7)
    if action_items:
        with st.container(border=True):
            st.markdown("**Due & Overdue Tasks**")
            for s in action_items:
                rc1, rc2, rc3, rc4 = st.columns([4, 1, 1, 1])
                rc1.markdown(
                    f"**{s.device_name}**  ·  {s.task_description}  ·  "
                    f"<span style='font-size:0.85rem'>{_status(days_until_due(s.next_due_date))}</span>",
                    unsafe_allow_html=True,
                )
                if rc2.button("✅ Log", key=f"due_log_{s.id}", use_container_width=True):
                    st.session_state["prefill_log"] = {
                        "device_id": s.device_id,
                        "task": s.task_description,
                        "schedule_id": s.id,
                        "service_type_id": s.service_type_id,
                    }
                    st.session_state.show_hist_add = True
                    st.rerun()
                if rc3.button("⏭ Skip", key=f"due_skip_{s.id}", use_container_width=True):
                    new_date = sched.advance_schedule(s.id)
                    st.toast(f"Skipped — next due {new_date}", icon="⏭")
                    st.rerun()
                if rc4.button("⏸ Pause", key=f"due_pause_{s.id}", use_container_width=True):
                    sched.deactivate_schedule(s.id)
                    st.toast("Schedule paused. Re-activate from Schedules tab.", icon="⏸")
                    st.rerun()
        st.divider()

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

    # ── Log list ──────────────────────────────────────────────────────────────
    all_devs_h   = inv.list_devices(include_archived=True)
    dev_flt_opts = {"All devices": None} | {d.name: d.id for d in all_devs_h}
    hf1, hf2, hf3 = st.columns([3, 1, 1])
    dev_flt_sel  = hf1.selectbox("Device", list(dev_flt_opts.keys()),
                                  key="hist_dev_flt", label_visibility="collapsed")
    hist_limit   = hf2.selectbox("Show", LIMIT_OPTIONS, index=1,
                                  key="hist_limit", label_visibility="collapsed",
                                  format_func=lambda x: f"Last {x}")
    flt_dev_id   = dev_flt_opts[dev_flt_sel]
    hf3.metric("Total Spend", _money(hist.total_cost(flt_dev_id)))

    logs = hist.list_logs(device_id=flt_dev_id, limit=hist_limit)

    if not logs:
        st.info("No entries yet. Log your first maintenance expense above.")
    else:
        from collections import defaultdict
        log_by_device: dict = defaultdict(list)
        for l in logs:
            log_by_device[l.device_name].append(l)

        for dev_name, dev_logs in log_by_device.items():
            total_dev = sum(l.cost_cad for l in dev_logs)
            with st.expander(
                f"**{dev_name}** — {len(dev_logs)} entr{'y' if len(dev_logs) == 1 else 'ies'}"
                f"  ·  {_money(total_dev)}",
                expanded=(flt_dev_id is not None),
            ):
                hcols = st.columns([1, 3, 2, 1, 1])
                for col, lbl in zip(hcols, ["Date", "Task", "Service Type", "Cost", ""]):
                    col.markdown(
                        f"<span style='font-size:0.75rem;text-transform:uppercase;"
                        f"color:#64748b;font-weight:600;letter-spacing:0.05em'>{lbl}</span>",
                        unsafe_allow_html=True,
                    )
                st.markdown("<hr style='margin:4px 0 8px'>", unsafe_allow_html=True)
                for l in dev_logs:
                    rc = st.columns([1, 3, 2, 1, 1])
                    rc[0].caption(l.completion_date)
                    rc[1].markdown(f"<span style='font-size:0.85rem'>{l.task_performed}</span>",
                                   unsafe_allow_html=True)
                    rc[2].caption(l.service_type_name or "—")
                    rc[3].caption(_money(l.cost_cad) if l.cost_cad else "—")
                    if rc[4].button("Open ↗", key=f"log_open_{l.id}", use_container_width=True):
                        _log_dialog(l)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SCHEDULES
# ══════════════════════════════════════════════════════════════════════════════

with tabs[3]:
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
        # Group by device
        from collections import defaultdict
        by_device: dict = defaultdict(list)
        for s in all_scheds:
            by_device[s.device_name].append(s)

        for dev_name, dev_scheds in by_device.items():
            overdue_cnt = sum(1 for s in dev_scheds if days_until_due(s.next_due_date) < 0)
            due_soon_cnt = sum(1 for s in dev_scheds if 0 <= days_until_due(s.next_due_date) <= 7)
            if overdue_cnt:
                badge = f"⛔ {overdue_cnt} overdue"
            elif due_soon_cnt:
                badge = f"🟡 {due_soon_cnt} due this week"
            else:
                badge = "🟢 on track"
            with st.expander(f"**{dev_name}** — {len(dev_scheds)} schedule(s) · {badge}",
                             expanded=bool(overdue_cnt)):
                hcols = st.columns([3, 1, 1, 1])
                for col, lbl in zip(hcols, ["Task", "Next Due", "Status", ""]):
                    col.markdown(
                        f"<span style='font-size:0.75rem;text-transform:uppercase;"
                        f"color:#64748b;font-weight:600;letter-spacing:0.05em'>{lbl}</span>",
                        unsafe_allow_html=True,
                    )
                st.markdown("<hr style='margin:4px 0 8px'>", unsafe_allow_html=True)
                for s in dev_scheds:
                    rc = st.columns([3, 1, 1, 1])
                    task_label = s.task_description
                    if not s.is_active:
                        task_label = f"⏸ {task_label}"
                    rc[0].markdown(task_label)
                    rc[1].markdown(f"<span style='font-size:0.85rem'>{s.next_due_date}</span>",
                                   unsafe_allow_html=True)
                    rc[2].markdown(f"<span style='font-size:0.85rem'>"
                                   f"{_status(days_until_due(s.next_due_date))}</span>",
                                   unsafe_allow_html=True)
                    if rc[3].button("Open ↗", key=f"sched_open_{s.id}", use_container_width=True):
                        _schedule_dialog(s)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — NOTIFICATIONS
# ══════════════════════════════════════════════════════════════════════════════

with tabs[4]:
    st.subheader("Notifications")

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
                        try:
                            eid = create_calendar_event(
                                device_name=dev.name, task_description=s.task_description,
                                due_date=s.next_due_date, frequency_days=s.frequency_days,
                                part_numbers=dev.part_numbers, resource_links=dev.resource_links,
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
