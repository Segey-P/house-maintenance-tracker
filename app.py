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
from src.models import Device, MaintenanceLog, Schedule
from src.scheduler import days_until_due
from utils.auth import logout_button  # require_password imported but disabled during dev

CATEGORIES = ["Major Appliances", "Laundry Systems", "Plumbing & Water", "Safety & Electrical"]
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

# TODO: re-enable password before sharing app publicly
# require_password()

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
    st.markdown("## 🏠 Maintenance\nTracker")
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
            st.info("No maintenance history yet. Log your first task in the History tab.")



# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DEVICES
# ══════════════════════════════════════════════════════════════════════════════

@st.dialog("Device Details", width="large")
def _device_dialog(device: Device):
    st.markdown(f"### {device.name}")
    st.caption(device.category + (" · Archived" if device.is_archived else ""))

    dm1, dm2, dm3 = st.columns(3)
    dm1.metric("Service Interval", _freq(device.maintenance_frequency_days) if device.maintenance_frequency_days else "—")
    dm2.metric("Total Spend", _money(hist.total_cost(device.id)))
    dm3.metric("Warranty Expiry", device.warranty_expiry or "—")
    st.divider()

    with st.form("device_detail_form"):
        fa1, fa2 = st.columns(2)
        ed_name   = fa1.text_input("Device name *", value=device.name)
        ed_cat    = fa2.selectbox("Category *", CATEGORIES, index=CATEGORIES.index(device.category))
        fb1, fb2  = st.columns(2)
        ed_model  = fb1.text_input("Model", value=device.model or "")
        ed_serial = fb2.text_input("Serial number", value=device.serial_number or "")
        ed_parts  = st.text_input("Part numbers (comma-separated)", value=", ".join(device.part_numbers))
        fc1, fc2, fc3 = st.columns(3)
        ed_freq   = fc1.number_input("Interval (days)", min_value=1, value=device.maintenance_frequency_days or 180)
        try:    pd_val = date.fromisoformat(device.purchase_date) if device.purchase_date else None
        except: pd_val = None
        ed_pdate  = fc2.date_input("Purchase date", value=pd_val)
        try:    we_val = date.fromisoformat(device.warranty_expiry) if device.warranty_expiry else None
        except: we_val = None
        ed_wexp   = fc3.date_input("Warranty expiry", value=we_val)
        ed_notes  = st.text_area("Notes", value=device.notes or "", height=70)
        fe1, fe2  = st.columns(2)
        ed_tut    = fe1.text_input("Tutorial URL", value=device.resource_links.get("tutorial", ""))
        ed_pur    = fe2.text_input("Purchase URL", value=device.resource_links.get("purchase", ""))

        if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
            if not ed_name:
                st.error("Device name is required.")
            else:
                device.name     = ed_name
                device.category = ed_cat
                device.model    = ed_model or None
                device.serial_number = ed_serial or None
                device.part_numbers  = [p.strip() for p in ed_parts.split(",") if p.strip()]
                device.maintenance_frequency_days = int(ed_freq)
                device.purchase_date  = str(ed_pdate) if ed_pdate else None
                device.warranty_expiry = str(ed_wexp) if ed_wexp else None
                device.notes          = ed_notes or None
                device.resource_links = {k: v for k, v in [("tutorial", ed_tut), ("purchase", ed_pur)] if v}
                inv.update_device(device)
                st.toast("Device updated.", icon="✅")
                st.rerun()

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
                d_parts  = st.text_input("Part numbers", placeholder="Comma-separated, e.g. DA29-00020B, WF3CB")
                c1, c2, c3 = st.columns(3)
                d_freq   = c1.number_input("Service interval (days) *", min_value=1, value=180)
                d_pdate  = c2.date_input("Purchase date", value=None)
                d_wexp   = c3.date_input("Warranty expiry", value=None)
                d_notes  = st.text_area("Notes", height=70, placeholder="Tips, BC code requirements, etc.")
                e1, e2   = st.columns(2)
                d_tutorial = e1.text_input("Tutorial URL", placeholder="YouTube link")
                d_purchase = e2.text_input("Purchase URL", placeholder="Amazon.ca link")
                fc1, fc2 = st.columns(2)
                submitted = fc1.form_submit_button("Save Device", type="primary", use_container_width=True)
                cancelled = fc2.form_submit_button("Cancel", use_container_width=True)

            if submitted:
                if not d_name:
                    st.error("Device name is required.")
                else:
                    links = {k: v for k, v in [("tutorial", d_tutorial), ("purchase", d_purchase)] if v}
                    inv.add_device(Device(
                        name=d_name, category=d_cat,
                        model=d_model or None, serial_number=d_serial or None,
                        part_numbers=[p.strip() for p in d_parts.split(",") if p.strip()],
                        maintenance_frequency_days=int(d_freq),
                        purchase_date=str(d_pdate) if d_pdate else None,
                        warranty_expiry=str(d_wexp) if d_wexp else None,
                        notes=d_notes or None, resource_links=links,
                    ))
                    st.session_state.show_inv_add = False
                    st.toast("Device added.", icon="✅")
                    st.rerun()
            if cancelled:
                st.session_state.show_inv_add = False
                st.rerun()

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
        # Table header
        hcols = st.columns([3, 2, 2, 1, 1])
        for col, label in zip(hcols, ["Name", "Category", "Interval", "Spend", ""]):
            col.markdown(f"**{label}**")
        st.divider()
        for d in devs:
            rc = st.columns([3, 2, 2, 1, 1])
            rc[0].write(("🗄 " if d.is_archived else "") + d.name)
            rc[1].write(d.category)
            rc[2].write(_freq(d.maintenance_frequency_days) if d.maintenance_frequency_days else "—")
            rc[3].write(_money(hist.total_cost(d.id)))
            if rc[4].button("Open ↗", key=f"dev_open_{d.id}", use_container_width=True):
                _device_dialog(d)
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

    if st.session_state.get("show_hist_add"):
        with st.container(border=True):
            st.markdown("**New Expense Entry**")
            with st.form("add_log_form", clear_on_submit=True):
                log_devs    = inv.list_devices()
                dev_map     = {f"{d.name}  —  {d.category}": d.id for d in log_devs}
                la1, la2    = st.columns(2)
                log_dev_sel = la1.selectbox("Device *", list(dev_map.keys()))
                log_date    = la2.date_input("Completion date", value=date.today())
                log_task    = st.text_input("Task performed *", placeholder="e.g. Replaced furnace filter")
                lb1, lb2    = st.columns(2)
                log_cost    = lb1.number_input("Cost (CAD)", min_value=0.0, value=0.0,
                                               step=0.01, format="%.2f")
                log_sourcing = lb2.text_input("Sourcing", placeholder="Vendor or URL")
                log_notes   = st.text_area("Notes", height=60,
                                           placeholder="Installation tips for next time")
                lc1, lc2    = st.columns(2)
                l_submitted = lc1.form_submit_button("Save Entry", type="primary", use_container_width=True)
                l_cancelled = lc2.form_submit_button("Cancel", use_container_width=True)

            if l_submitted:
                if not log_task:
                    st.error("Task description is required.")
                else:
                    hist.add_log(MaintenanceLog(
                        device_id=dev_map[log_dev_sel],
                        task_performed=log_task,
                        completion_date=str(log_date),
                        cost_cad=float(log_cost),
                        sourcing_info=log_sourcing or None,
                        notes=log_notes or None,
                    ))
                    st.session_state.show_hist_add = False
                    st.toast("Expense logged.", icon="✅")
                    st.rerun()
            if l_cancelled:
                st.session_state.show_hist_add = False
                st.rerun()

    # Filters + spend total
    all_devs_h   = inv.list_devices(include_archived=True)
    dev_flt_opts = {"All devices": None} | {f"{d.name}": d.id for d in all_devs_h}
    hf1, hf2, hf3 = st.columns([3, 1, 1])
    dev_flt_sel  = hf1.selectbox("Device", list(dev_flt_opts.keys()),
                                  key="hist_dev_flt", label_visibility="collapsed")
    hist_limit   = hf2.selectbox("Show", LIMIT_OPTIONS, index=1,
                                  key="hist_limit", label_visibility="collapsed",
                                  format_func=lambda x: f"Last {x}")
    flt_dev_id   = dev_flt_opts[dev_flt_sel]
    hf3.metric("Total Spend", _money(hist.total_cost(flt_dev_id)))

    logs = hist.list_logs(device_id=flt_dev_id, limit=hist_limit)

    if logs:
        df = pd.DataFrame([
            {
                "Date":    l.completion_date,
                "Device":  l.device_name,
                "Task":    l.task_performed,
                "Cost":    _money(l.cost_cad),
                "Sourcing": l.sourcing_info or "—",
                "Notes":   l.notes or "—",
            }
            for l in logs
        ])
        st.dataframe(df, hide_index=True, width=1100)
    else:
        st.info("No entries yet. Log your first maintenance expense above.")

    # Edit / Delete
    with st.expander("✏️ Edit / Delete Entry"):
        all_logs = hist.list_logs(limit=100)
        log_opts = {f"{l.completion_date}  ·  {l.device_name}  ·  {l.task_performed}": l
                    for l in all_logs}
        sel_log  = st.selectbox("Select entry", ["— select —"] + list(log_opts.keys()),
                                key="edit_log_sel")

        if sel_log != "— select —":
            el = log_opts[sel_log]
            with st.form("edit_log_form"):
                ela1, ela2 = st.columns(2)
                el_task    = ela1.text_input("Task performed", value=el.task_performed)
                try:    el_date_val = date.fromisoformat(el.completion_date)
                except: el_date_val = date.today()
                el_date    = ela2.date_input("Completion date", value=el_date_val)
                elb1, elb2 = st.columns(2)
                el_cost    = elb1.number_input("Cost (CAD)", min_value=0.0,
                                               value=float(el.cost_cad), step=0.01, format="%.2f")
                el_src     = elb2.text_input("Sourcing", value=el.sourcing_info or "")
                el_notes   = st.text_area("Notes", value=el.notes or "", height=60)

                if st.form_submit_button("Save Changes", type="primary"):
                    el.task_performed  = el_task
                    el.completion_date = str(el_date)
                    el.cost_cad        = float(el_cost)
                    el.sourcing_info   = el_src or None
                    el.notes           = el_notes or None
                    hist.update_log(el)
                    st.toast("Entry updated.", icon="✅")
                    st.rerun()

            if st.button("Delete Entry", type="secondary", key="del_log_btn"):
                _delete_dialog(f"{el.completion_date} · {el.task_performed}", "log", el.id)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SCHEDULES
# ══════════════════════════════════════════════════════════════════════════════

with tabs[3]:
    sh1, sh2 = st.columns([5, 1])
    sh1.subheader("Maintenance Schedules")
    if sh2.button("＋ Add Schedule", type="primary", use_container_width=True, key="sched_add_toggle"):
        st.session_state.show_sched_add = not st.session_state.get("show_sched_add", False)

    if st.session_state.get("show_sched_add"):
        with st.container(border=True):
            st.markdown("**New Schedule**")
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

    if all_scheds:
        df = pd.DataFrame([
            {
                "Device":   s.device_name,
                "Task":     s.task_description,
                "Next Due": s.next_due_date,
                "Status":   _status(days_until_due(s.next_due_date)),
                "Repeats":  _freq(s.frequency_days),
                "Active":   "✅" if s.is_active else "⏸ Paused",
                "Calendar": "🗓 Linked" if s.calendar_event_id else "Not linked",
            }
            for s in all_scheds
        ])
        st.dataframe(_style_schedule(df), hide_index=True, width=1100)
    else:
        st.info("No schedules found.")

    with st.expander("✏️ Edit / Manage Schedule"):
        all_s_list = sched.list_schedules(active_only=False)
        s_opts     = {f"{s.device_name}  ·  {s.task_description}  ({s.next_due_date})": s
                      for s in all_s_list}
        sel_s      = st.selectbox("Select schedule", ["— select —"] + list(s_opts.keys()),
                                  key="edit_s_sel")

        if sel_s != "— select —":
            es = s_opts[sel_s]
            with st.form("edit_sched_form"):
                es_task  = st.text_input("Task description", value=es.task_description)
                esa1, esa2 = st.columns(2)
                try:    es_due_val = date.fromisoformat(es.next_due_date)
                except: es_due_val = date.today()
                es_due   = esa1.date_input("Next due date", value=es_due_val)
                es_freq  = esa2.number_input("Frequency (days)", min_value=1, value=es.frequency_days)
                es_active = st.checkbox("Active", value=es.is_active)

                if st.form_submit_button("Save Changes", type="primary"):
                    es.task_description = es_task
                    es.next_due_date    = str(es_due)
                    es.frequency_days   = int(es_freq)
                    es.is_active        = es_active
                    sched.update_schedule(es)
                    st.toast("Schedule updated.", icon="✅")
                    st.rerun()

            sg1, sg2, sg3 = st.columns([2, 2, 4])
            with sg1:
                tog = "▶ Activate" if not es.is_active else "⏸ Pause"
                if st.button(tog, key="tog_sched", use_container_width=True):
                    es.is_active = not es.is_active
                    sched.update_schedule(es)
                    st.rerun()
            with sg2:
                if st.button("Delete", type="secondary", key="del_sched", use_container_width=True):
                    _delete_dialog(f"{es.device_name} · {es.task_description}", "schedule", es.id)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — NOTIFICATIONS
# ══════════════════════════════════════════════════════════════════════════════

with tabs[4]:
    st.subheader("Notifications")

    # ── Google Calendar ───────────────────────────────────────────────────────
    cal_col, future_col = st.columns(2)
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

    # ── Future Features ───────────────────────────────────────────────────────
    # TODO: re-enable password gate before sharing app publicly (utils/auth.py → require_password)
    # TODO: download schedule as a checklist (PDF or CSV export of upcoming tasks)
    # TODO: email alerts — send maintenance reminders to user email
    with future_col:
        with st.container(border=True):
            st.markdown("### 🚧 Coming Soon")
            st.markdown("""
- **Download schedule** — export upcoming tasks as a printable checklist
- **Email alerts** — maintenance reminders sent to your inbox
- **Google Calendar sync** — push schedules as recurring calendar events
- **Photo import** — identify appliance from photo, auto-fill specs
""")
