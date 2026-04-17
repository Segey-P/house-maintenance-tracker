from typing import Optional
from .db import get_connection
from .models import MaintenanceLog


def add_log(log: MaintenanceLog) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO maintenance_log
               (device_id, task_performed, completion_date, cost_cad, sourcing_info, notes)
               VALUES (%s,%s,%s,%s,%s,%s)
               RETURNING id""",
            (
                log.device_id,
                log.task_performed,
                log.completion_date,
                log.cost_cad,
                log.sourcing_info,
                log.notes,
            ),
        )
        return cur.fetchone()["id"]


def get_log(log_id: int) -> Optional[MaintenanceLog]:
    with get_connection() as conn:
        row = conn.execute(
            """SELECT l.*, d.name as device_name
               FROM maintenance_log l JOIN devices d ON l.device_id = d.id
               WHERE l.id = %s""",
            (log_id,),
        ).fetchone()
    return MaintenanceLog.from_row(row) if row else None


def list_logs(device_id: Optional[int] = None, limit: int = 50) -> list[MaintenanceLog]:
    with get_connection() as conn:
        if device_id:
            rows = conn.execute(
                """SELECT l.*, d.name as device_name
                   FROM maintenance_log l JOIN devices d ON l.device_id = d.id
                   WHERE l.device_id = %s
                   ORDER BY l.completion_date DESC LIMIT %s""",
                (device_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT l.*, d.name as device_name
                   FROM maintenance_log l JOIN devices d ON l.device_id = d.id
                   ORDER BY l.completion_date DESC LIMIT %s""",
                (limit,),
            ).fetchall()
    return [MaintenanceLog.from_row(r) for r in rows]


def update_log(log: MaintenanceLog) -> None:
    with get_connection() as conn:
        conn.execute(
            """UPDATE maintenance_log SET
               task_performed=%s, completion_date=%s, cost_cad=%s, sourcing_info=%s, notes=%s
               WHERE id=%s""",
            (log.task_performed, log.completion_date, log.cost_cad,
             log.sourcing_info, log.notes, log.id),
        )


def delete_log(log_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM maintenance_log WHERE id = %s", (log_id,))


def total_cost(device_id: Optional[int] = None) -> float:
    with get_connection() as conn:
        if device_id:
            row = conn.execute(
                "SELECT COALESCE(SUM(cost_cad),0) as total FROM maintenance_log WHERE device_id=%s",
                (device_id,),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT COALESCE(SUM(cost_cad),0) as total FROM maintenance_log"
            ).fetchone()
    return float(row["total"])
