"""
Reference catalog of household devices and service types.
Authoritative seed source: scripts/seed_data.sql (run via Neon SQL editor).
This module provides Python-level constants for dev/testing use only.
"""
from .models import Device, ServiceType

# Each entry: Device kwargs (only fields that exist on the current Device model)
SEED_DEVICES: list[dict] = [
    # ── Kitchen Appliances ────────────────────────────────────────────────────
    {
        "name": "Main Fridge",
        "category": "Kitchen Appliances",
        "model": "KitchenAid KRFC300ESS",
        "purchase_date": "2021-03-28",
        "warranty_expiry": "2026-03-28",
        "notes": "Located in main kitchen island/wall unit. 1\" clearance on sides required. Sealed system warranty until 2026-03-28.",
    },
    {
        "name": "Dishwasher",
        "category": "Kitchen Appliances",
        "model": "KitchenAid KDTM404KPS",
        "purchase_date": "2021-03-28",
        "warranty_expiry": "2022-03-28",
        "notes": "Features FreeFlex third rack.",
    },
    {
        "name": "Wall Oven",
        "category": "Kitchen Appliances",
        "model": "KitchenAid KOSE500ESS",
        "purchase_date": "2021-03-28",
        "warranty_expiry": "2022-03-28",
        "notes": "Convection model. Check door seal for brittleness. Avoid Self-Clean mode to preserve control board.",
    },
    {
        "name": "Espresso Machine",
        "category": "Kitchen Appliances",
        "model": "Ascaso Steel Duo",
        "purchase_date": "2021-03-28",
        "warranty_expiry": "2023-03-28",
        "notes": "Solid brass group head. Use soft filtered water to reduce descaling frequency.",
    },
    # ── Laundry Systems ───────────────────────────────────────────────────────
    {
        "name": "Dryer",
        "category": "Laundry Systems",
        "model": "Whirlpool YWHD560CHW1",
        "purchase_date": "2021-03-28",
        "notes": "Heat pump dryer. Check indicator light for filter cleaning every 5-10 cycles.",
    },
    {
        "name": "Washer",
        "category": "Laundry Systems",
        "model": "Whirlpool (stacked)",
        "purchase_date": "2021-03-28",
        "notes": "Stacked unit. High humidity: check door gasket for mold monthly.",
    },
    # ── Plumbing & Water ──────────────────────────────────────────────────────
    {
        "name": "Water Heater",
        "category": "Plumbing & Water",
        "model": "Rheem (check unit label)",
        "notes": "Annual flushing critical — Squamish seasonal turbidity causes sediment buildup.",
    },
    {
        "name": "Faucets",
        "category": "Plumbing & Water",
        "model": "Kitchen + Bathrooms",
        "notes": "Squamish water is soft — aerator maintenance mainly for flow, not mineral buildup.",
    },
    {
        "name": "Toilets",
        "category": "Plumbing & Water",
        "notes": "All toilets. Check flappers and fill valves annually.",
    },
    # ── Safety & Electrical ───────────────────────────────────────────────────
    {
        "name": "vanEE Ventilation Control",
        "category": "Safety & Electrical",
        "notes": "Critical for moisture control in Squamish. Keep on Smart/High mode in winter to prevent mold.",
    },
    {
        "name": "Stelpro Thermostats",
        "category": "Safety & Electrical",
        "notes": "Electric baseboard thermostats. Turn off breaker before cleaning. No liquids on vents.",
    },
    {
        "name": "Electric Baseboards",
        "category": "Safety & Electrical",
        "notes": "Dust buildup reduces efficiency and causes burning smell at heating season start.",
    },
    {
        "name": "Bathroom Exhaust Fan",
        "category": "Safety & Electrical",
        "notes": "High humidity — mold in fan housing is a real risk. Annual deep clean critical.",
    },
    {
        "name": "Smoke & CO Detector",
        "category": "Safety & Electrical",
        "model": "BRK",
        "notes": "2026 BC Regs: CO alarm required on every storey and near sleeping areas. Replace smoke after 10yr, CO after 7yr.",
    },
    {
        "name": "Ceiling Fan",
        "category": "Safety & Electrical",
        "notes": "CW (low speed) in winter to push warm air down. CCW in summer for cooling breeze.",
    },
]
