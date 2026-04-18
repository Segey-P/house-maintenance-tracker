from datetime import date, timedelta
from typing import Optional
from .db import get_connection
from .models import Schedule


def get_schedule(schedule_id: int) -> Optional[Schedule]:
    with get_connection() as conn:
        row = conn.execute(
            """SELECT s.*, d.name as device_name, st.name as service_type_name
               FROM schedules s
               JOIN devices d ON s.device_id = d.id
               LEFT JOIN service_types st ON s.service_type_id = st.id
               WHERE s.id = %s""",
            (schedule_id,),
        ).fetchone()
    return Schedule.from_row(row) if row else None


def list_schedules(device_id: Optional[int] = None, active_only: bool = True) -> list[Schedule]:
    with get_connection() as conn:
        query = """SELECT s.*, d.name as device_name, st.name as service_type_name
                   FROM schedules s
                   JOIN devices d ON s.device_id = d.id
                   LEFT JOIN service_types st ON s.service_type_id = st.id
                   WHERE 1=1"""
        params: list = []
        if active_only:
            query += " AND s.is_active = 1"
        if device_id:
            query += " AND s.device_id = %s"
            params.append(device_id)
        query += " ORDER BY s.next_due_date"
        rows = conn.execute(query, params).fetchall()
    return [Schedule.from_row(r) for r in rows]


def get_due_schedules(days_ahead: int = 7) -> list[Schedule]:
    cutoff = (date.today() + timedelta(days=days_ahead)).isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT s.*, d.name as device_name, st.name as service_type_name
               FROM schedules s
               JOIN devices d ON s.device_id = d.id
               LEFT JOIN service_types st ON s.service_type_id = st.id
               WHERE s.is_active = 1 AND s.next_due_date <= %s
               ORDER BY s.next_due_date""",
            (cutoff,),
        ).fetchall()
    return [Schedule.from_row(r) for r in rows]


def advance_schedule(schedule_id: int) -> str:
    schedule = get_schedule(schedule_id)
    if not schedule:
        raise ValueError(f"Schedule {schedule_id} not found")
    due = date.fromisoformat(schedule.next_due_date)
    new_due = (due + timedelta(days=schedule.frequency_days)).isoformat()
    with get_connection() as conn:
        conn.execute(
            "UPDATE schedules SET next_due_date = %s WHERE id = %s",
            (new_due, schedule_id),
        )
    return new_due


def set_calendar_event_id(schedule_id: int, event_id: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE schedules SET calendar_event_id = %s WHERE id = %s",
            (event_id, schedule_id),
        )


def update_schedule(schedule: Schedule) -> None:
    with get_connection() as conn:
        conn.execute(
            """UPDATE schedules SET
               task_description=%s, next_due_date=%s, frequency_days=%s, is_active=%s
               WHERE id=%s""",
            (schedule.task_description, schedule.next_due_date,
             schedule.frequency_days, int(schedule.is_active), schedule.id),
        )


def delete_schedule(schedule_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM schedules WHERE id = %s", (schedule_id,))


def deactivate_schedule(schedule_id: int) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE schedules SET is_active = 0 WHERE id = %s", (schedule_id,))


def days_until_due(next_due_date: str) -> int:
    return (date.fromisoformat(next_due_date) - date.today()).days
