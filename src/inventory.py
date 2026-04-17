import json
from typing import Optional
from .db import get_connection
from .models import Device


def add_device(device: Device) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO devices
               (name, category, model, serial_number, part_numbers,
                maintenance_frequency_days, resource_links,
                purchase_date, warranty_expiry, notes)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                device.name,
                device.category,
                device.model,
                device.serial_number,
                json.dumps(device.part_numbers),
                device.maintenance_frequency_days,
                json.dumps(device.resource_links),
                device.purchase_date,
                device.warranty_expiry,
                device.notes,
            ),
        )
        return cur.lastrowid


def get_device(device_id: int) -> Optional[Device]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM devices WHERE id = ?", (device_id,)).fetchone()
    return Device.from_row(row) if row else None


def list_devices(category: Optional[str] = None, include_archived: bool = False) -> list[Device]:
    with get_connection() as conn:
        query = "SELECT * FROM devices WHERE 1=1"
        params: list = []
        if not include_archived:
            query += " AND is_archived = 0"
        if category:
            query += " AND category = ?"
            params.append(category)
        query += " ORDER BY category, name"
        rows = conn.execute(query, params).fetchall()
    return [Device.from_row(r) for r in rows]


def update_device(device: Device) -> None:
    with get_connection() as conn:
        conn.execute(
            """UPDATE devices SET
               name=?, category=?, model=?, serial_number=?, part_numbers=?,
               maintenance_frequency_days=?, resource_links=?,
               purchase_date=?, warranty_expiry=?, notes=?, is_archived=?
               WHERE id=?""",
            (
                device.name,
                device.category,
                device.model,
                device.serial_number,
                json.dumps(device.part_numbers),
                device.maintenance_frequency_days,
                json.dumps(device.resource_links),
                device.purchase_date,
                device.warranty_expiry,
                device.notes,
                int(device.is_archived),
                device.id,
            ),
        )


def delete_device(device_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM devices WHERE id = ?", (device_id,))


def archive_device(device_id: int) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE devices SET is_archived = 1 WHERE id = ?", (device_id,))


def unarchive_device(device_id: int) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE devices SET is_archived = 0 WHERE id = ?", (device_id,))
