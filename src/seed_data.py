"""Pre-populated device catalog for a 1-bedroom BC residence."""
from datetime import date, timedelta
from .models import Device, Schedule

SEED_DEVICES: list[dict] = [
    {
        "name": "Furnace / HVAC Filter",
        "category": "Safety & Electrical",
        "model": "16x25x1 MERV-8 (verify your size)",
        "part_numbers": ["16x25x1 MERV-8"],
        "maintenance_frequency_days": 90,
        "resource_links": {
            "purchase": "https://www.amazon.ca/s?k=16x25x1+MERV-8+furnace+filter",
            "tutorial": "https://www.youtube.com/results?search_query=how+to+replace+furnace+filter",
        },
        "notes": "Check monthly during heating season (Oct–Mar). Replace every 90 days minimum.",
    },
    {
        "name": "Refrigerator Water Filter",
        "category": "Major Appliances",
        "model": "Check inside fridge — model label near filter housing",
        "part_numbers": [],
        "maintenance_frequency_days": 180,
        "resource_links": {
            "purchase": "https://www.amazon.ca/s?k=refrigerator+water+filter",
            "tutorial": "https://www.youtube.com/results?search_query=how+to+replace+refrigerator+water+filter",
        },
        "notes": "Part number varies by brand. Check door label or existing filter cartridge.",
    },
    {
        "name": "Refrigerator Coils",
        "category": "Major Appliances",
        "model": None,
        "part_numbers": [],
        "maintenance_frequency_days": 180,
        "resource_links": {
            "tutorial": "https://www.youtube.com/results?search_query=clean+refrigerator+condenser+coils",
        },
        "notes": "Vacuum coils at back or underneath. Improves efficiency and lifespan.",
    },
    {
        "name": "Smoke Detectors",
        "category": "Safety & Electrical",
        "model": "Check unit label for model",
        "part_numbers": ["9V battery (test monthly)", "Full unit replacement at 10 years"],
        "maintenance_frequency_days": 30,
        "resource_links": {
            "purchase": "https://www.amazon.ca/s?k=smoke+detector+9v",
            "tutorial": "https://www.youtube.com/results?search_query=test+smoke+detector",
        },
        "notes": "BC Fire Code: test monthly, replace batteries annually, replace unit every 10 years.",
    },
    {
        "name": "CO Detector",
        "category": "Safety & Electrical",
        "model": "Check unit label for model",
        "part_numbers": ["Battery per unit spec", "Full unit replacement at 7 years"],
        "maintenance_frequency_days": 30,
        "resource_links": {
            "tutorial": "https://www.youtube.com/results?search_query=test+carbon+monoxide+detector",
        },
        "notes": "BC Building Code: test monthly, replace unit every 7 years.",
    },
    {
        "name": "Water Heater",
        "category": "Plumbing & Water",
        "model": "Check unit label",
        "part_numbers": ["Anode rod — match thread size (typically 1-1/16\")"],
        "maintenance_frequency_days": 365,
        "resource_links": {
            "tutorial": "https://www.youtube.com/results?search_query=flush+water+heater+BC",
        },
        "notes": "Flush sediment annually. Inspect anode rod every 3 years; replace if less than 1/2 inch thick.",
    },
    {
        "name": "Washing Machine Drum & Hoses",
        "category": "Laundry Systems",
        "model": "Check unit label",
        "part_numbers": ["Washer drum cleaner tab (e.g., Affresh)"],
        "maintenance_frequency_days": 30,
        "resource_links": {
            "purchase": "https://www.amazon.ca/s?k=affresh+washer+cleaner",
            "tutorial": "https://www.youtube.com/results?search_query=clean+washing+machine+drum",
        },
        "notes": "Run drum clean cycle monthly. Inspect rubber hoses annually — replace every 5 years or if cracked.",
    },
    {
        "name": "Dryer Vent Duct",
        "category": "Laundry Systems",
        "model": None,
        "part_numbers": ["Dryer vent cleaning brush kit"],
        "maintenance_frequency_days": 365,
        "resource_links": {
            "purchase": "https://www.amazon.ca/s?k=dryer+vent+cleaning+brush+kit",
            "tutorial": "https://www.youtube.com/results?search_query=clean+dryer+vent+duct",
        },
        "notes": "Clean lint trap after every load. Full vent duct cleaning annually — fire hazard if blocked.",
    },
    {
        "name": "Range Hood Filter",
        "category": "Major Appliances",
        "model": "Check hood underside for filter dimensions",
        "part_numbers": ["Grease filter — measure your size"],
        "maintenance_frequency_days": 30,
        "resource_links": {
            "tutorial": "https://www.youtube.com/results?search_query=clean+range+hood+grease+filter",
        },
        "notes": "Metal mesh filters: soak in hot soapy water monthly. Replace disposable carbon filters every 3–4 months.",
    },
    {
        "name": "Bathroom Exhaust Fan",
        "category": "Safety & Electrical",
        "model": None,
        "part_numbers": [],
        "maintenance_frequency_days": 180,
        "resource_links": {
            "tutorial": "https://www.youtube.com/results?search_query=clean+bathroom+exhaust+fan",
        },
        "notes": "Vacuum grille and fan blades every 6 months to prevent motor strain and mold buildup.",
    },
]


def _next_due(offset_days: int) -> str:
    return (date.today() + timedelta(days=offset_days)).isoformat()


def get_seed_schedules(device_map: dict[str, int]) -> list[dict]:
    """Return initial schedules keyed by device name -> device_id."""
    schedules = []
    for device_name, offset, task in [
        ("Furnace / HVAC Filter", 45, "Replace furnace filter"),
        ("Refrigerator Water Filter", 90, "Replace water filter cartridge"),
        ("Refrigerator Coils", 60, "Vacuum condenser coils"),
        ("Smoke Detectors", 7, "Test smoke detectors"),
        ("CO Detector", 7, "Test CO detector"),
        ("Water Heater", 180, "Flush sediment from water heater"),
        ("Washing Machine Drum & Hoses", 14, "Run drum clean cycle"),
        ("Dryer Vent Duct", 270, "Clean dryer vent duct"),
        ("Range Hood Filter", 20, "Clean range hood grease filter"),
        ("Bathroom Exhaust Fan", 120, "Clean exhaust fan grille and blades"),
    ]:
        if device_name in device_map:
            dev = next(d for d in SEED_DEVICES if d["name"] == device_name)
            schedules.append(
                {
                    "device_id": device_map[device_name],
                    "task_description": task,
                    "next_due_date": _next_due(offset),
                    "frequency_days": dev["maintenance_frequency_days"],
                }
            )
    return schedules
