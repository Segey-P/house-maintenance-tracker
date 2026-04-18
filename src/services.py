import json
from datetime import date, timedelta
from typing import Optional
from .db import get_connection
from .models import ServiceType


def add_service_type(st_obj: ServiceType, first_due_date: Optional[str] = None) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO service_types
               (device_id, name, frequency_days, part_numbers, tutorial_url, purchase_url, notes)
               VALUES (%s,%s,%s,%s,%s,%s,%s)
               RETURNING id""",
            (
                st_obj.device_id,
                st_obj.name,
                st_obj.frequency_days,
                json.dumps(st_obj.part_numbers),
                st_obj.tutorial_url,
                st_obj.purchase_url,
                st_obj.notes,
            ),
        )
        service_id = cur.fetchone()["id"]

    _auto_create_schedule(service_id, st_obj, first_due_date)
    return service_id


def _auto_create_schedule(service_type_id: int, st_obj: ServiceType, first_due_date: Optional[str] = None) -> None:
    if first_due_date:
        next_due = first_due_date
    else:
        next_due = (date.today() + timedelta(days=st_obj.frequency_days)).isoformat()
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO schedules
               (device_id, service_type_id, task_description, next_due_date, frequency_days)
               VALUES (%s,%s,%s,%s,%s)""",
            (st_obj.device_id, service_type_id, st_obj.name, next_due, st_obj.frequency_days),
        )


def get_service_type(service_type_id: int) -> Optional[ServiceType]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM service_types WHERE id = %s", (service_type_id,)
        ).fetchone()
    return ServiceType.from_row(row) if row else None


def list_service_types(device_id: int) -> list[ServiceType]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM service_types WHERE device_id = %s ORDER BY name",
            (device_id,),
        ).fetchall()
    return [ServiceType.from_row(r) for r in rows]


def update_service_type(st_obj: ServiceType) -> None:
    with get_connection() as conn:
        conn.execute(
            """UPDATE service_types SET
               name=%s, frequency_days=%s, part_numbers=%s,
               tutorial_url=%s, purchase_url=%s, notes=%s
               WHERE id=%s""",
            (
                st_obj.name,
                st_obj.frequency_days,
                json.dumps(st_obj.part_numbers),
                st_obj.tutorial_url,
                st_obj.purchase_url,
                st_obj.notes,
                st_obj.id,
            ),
        )
        conn.execute(
            "UPDATE schedules SET task_description=%s, frequency_days=%s WHERE service_type_id=%s",
            (st_obj.name, st_obj.frequency_days, st_obj.id),
        )


def delete_service_type(service_type_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM service_types WHERE id = %s", (service_type_id,))
