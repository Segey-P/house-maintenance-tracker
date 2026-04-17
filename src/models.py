import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Device:
    name: str
    category: str
    id: Optional[int] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    part_numbers: list = field(default_factory=list)
    maintenance_frequency_days: Optional[int] = None
    resource_links: dict = field(default_factory=dict)
    purchase_date: Optional[str] = None
    warranty_expiry: Optional[str] = None
    notes: Optional[str] = None
    is_archived: bool = False
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Device":
        keys = row.keys()
        return cls(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            model=row["model"],
            serial_number=row["serial_number"],
            part_numbers=json.loads(row["part_numbers"] or "[]"),
            maintenance_frequency_days=row["maintenance_frequency_days"],
            resource_links=json.loads(row["resource_links"] or "{}"),
            purchase_date=row["purchase_date"],
            warranty_expiry=row["warranty_expiry"],
            notes=row["notes"],
            is_archived=bool(row["is_archived"]) if "is_archived" in keys else False,
            created_at=str(row["created_at"]) if row.get("created_at") else None,
        )


@dataclass
class MaintenanceLog:
    device_id: int
    task_performed: str
    completion_date: str
    id: Optional[int] = None
    cost_cad: float = 0.0
    sourcing_info: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    device_name: Optional[str] = None  # joined field

    @classmethod
    def from_row(cls, row) -> "MaintenanceLog":
        return cls(
            id=row["id"],
            device_id=row["device_id"],
            task_performed=row["task_performed"],
            completion_date=row["completion_date"],
            cost_cad=row["cost_cad"] or 0.0,
            sourcing_info=row["sourcing_info"],
            notes=row["notes"],
            created_at=str(row["created_at"]) if row.get("created_at") else None,
            device_name=row["device_name"] if "device_name" in row.keys() else None,
        )


@dataclass
class Schedule:
    device_id: int
    task_description: str
    next_due_date: str
    frequency_days: int
    id: Optional[int] = None
    calendar_event_id: Optional[str] = None
    is_active: bool = True
    created_at: Optional[str] = None
    device_name: Optional[str] = None  # joined field

    @classmethod
    def from_row(cls, row) -> "Schedule":
        return cls(
            id=row["id"],
            device_id=row["device_id"],
            task_description=row["task_description"],
            next_due_date=row["next_due_date"],
            frequency_days=row["frequency_days"],
            calendar_event_id=row["calendar_event_id"],
            is_active=bool(row["is_active"]),
            created_at=str(row["created_at"]) if row.get("created_at") else None,
            device_name=row["device_name"] if "device_name" in row.keys() else None,
        )
