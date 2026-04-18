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
            purchase_date=row["purchase_date"],
            warranty_expiry=row["warranty_expiry"],
            notes=row["notes"],
            is_archived=bool(row["is_archived"]) if "is_archived" in keys else False,
            created_at=str(row["created_at"]) if row.get("created_at") else None,
        )


@dataclass
class ServiceType:
    device_id: int
    name: str
    frequency_days: int
    id: Optional[int] = None
    part_numbers: list = field(default_factory=list)
    tutorial_url: Optional[str] = None
    purchase_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "ServiceType":
        return cls(
            id=row["id"],
            device_id=row["device_id"],
            name=row["name"],
            frequency_days=row["frequency_days"],
            part_numbers=json.loads(row["part_numbers"] or "[]"),
            tutorial_url=row["tutorial_url"],
            purchase_url=row["purchase_url"],
            notes=row["notes"],
            created_at=str(row["created_at"]) if row.get("created_at") else None,
        )


@dataclass
class MaintenanceLog:
    device_id: int
    task_performed: str
    completion_date: str
    id: Optional[int] = None
    service_type_id: Optional[int] = None
    cost_cad: float = 0.0
    sourcing_info: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    device_name: Optional[str] = None
    service_type_name: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "MaintenanceLog":
        keys = row.keys()
        return cls(
            id=row["id"],
            device_id=row["device_id"],
            service_type_id=row.get("service_type_id"),
            task_performed=row["task_performed"],
            completion_date=row["completion_date"],
            cost_cad=row["cost_cad"] or 0.0,
            sourcing_info=row["sourcing_info"],
            notes=row["notes"],
            created_at=str(row["created_at"]) if row.get("created_at") else None,
            device_name=row["device_name"] if "device_name" in keys else None,
            service_type_name=row["service_type_name"] if "service_type_name" in keys else None,
        )


@dataclass
class Schedule:
    device_id: int
    task_description: str
    next_due_date: str
    frequency_days: int
    id: Optional[int] = None
    service_type_id: Optional[int] = None
    calendar_event_id: Optional[str] = None
    is_active: bool = True
    created_at: Optional[str] = None
    device_name: Optional[str] = None
    service_type_name: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "Schedule":
        keys = row.keys()
        return cls(
            id=row["id"],
            device_id=row["device_id"],
            service_type_id=row.get("service_type_id"),
            task_description=row["task_description"],
            next_due_date=row["next_due_date"],
            frequency_days=row["frequency_days"],
            calendar_event_id=row["calendar_event_id"],
            is_active=bool(row["is_active"]),
            created_at=str(row["created_at"]) if row.get("created_at") else None,
            device_name=row["device_name"] if "device_name" in keys else None,
            service_type_name=row["service_type_name"] if "service_type_name" in keys else None,
        )
