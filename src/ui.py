"""Shared UI primitives — see design_handoff/DESIGN.md §2.3 for status system."""
from typing import Optional


# Status colour system — design §2.3
STATUS_STYLES = {
    "overdue":  {"bg": "#fef2f2", "color": "#dc2626", "border": "#fecaca", "dot": "#ef4444"},
    "today":    {"bg": "#fff7ed", "color": "#c2410c", "border": "#fed7aa", "dot": "#f97316"},
    "soon":     {"bg": "#fffbeb", "color": "#b45309", "border": "#fde68a", "dot": "#f59e0b"},
    "upcoming": {"bg": "#eff6ff", "color": "#1d4ed8", "border": "#bfdbfe", "dot": "#3b82f6"},
    "ok":       {"bg": "#f0fdf4", "color": "#15803d", "border": "#bbf7d0", "dot": "#22c55e"},
    "neutral":  {"bg": "#f4f4f5", "color": "#52525b", "border": "#e4e4e7", "dot": "#d1d5db"},
    "purple":   {"bg": "#f5f3ff", "color": "#6d28d9", "border": "#ddd6fe", "dot": "#8b5cf6"},
    "blue":     {"bg": "#eff6ff", "color": "#1d4ed8", "border": "#bfdbfe", "dot": "#3b82f6"},
}


def status_info(days: Optional[int]) -> dict:
    if days is None:
        return {"label": "No schedule", "status": "neutral"}
    if days < 0:
        return {"label": f"{abs(days)}d overdue", "status": "overdue"}
    if days == 0:
        return {"label": "Due today", "status": "today"}
    if days <= 7:
        return {"label": f"In {days}d", "status": "soon"}
    if days <= 30:
        return {"label": f"In {days}d", "status": "upcoming"}
    return {"label": f"In {days}d", "status": "ok"}


def badge_html(status: str, label: str) -> str:
    s = STATUS_STYLES.get(status, STATUS_STYLES["neutral"])
    return (
        f'<span style="display:inline-block;font-size:11px;font-weight:600;'
        f'letter-spacing:0.03em;padding:2px 8px;border-radius:20px;'
        f'background:{s["bg"]};color:{s["color"]};border:1px solid {s["border"]};">'
        f"{label}</span>"
    )


def stat_card_html(label: str, value: str, tone: str = "neutral") -> str:
    """Design §3 Dashboard stat row. Tone tints bg/value colour for urgency."""
    tones = {
        "neutral": {"bg": "#ffffff", "color": "#1c1c1e"},
        "danger":  {"bg": "#fef2f2", "color": "#dc2626"},
        "warn":    {"bg": "#fffbeb", "color": "#b45309"},
    }
    t = tones.get(tone, tones["neutral"])
    return (
        f'<div style="background:{t["bg"]};border:1px solid #e5e5e3;border-radius:12px;'
        f'padding:16px 20px;box-shadow:0 1px 4px rgba(0,0,0,0.04);">'
        f'<div style="font-size:11px;font-weight:600;color:#9ca3af;'
        f'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">{label}</div>'
        f'<div style="font-size:28px;font-weight:800;color:{t["color"]};'
        f'letter-spacing:-0.02em;line-height:1;">{value}</div>'
        f"</div>"
    )
