import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "house_maintenance.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS devices (
                id                          INTEGER PRIMARY KEY AUTOINCREMENT,
                name                        TEXT NOT NULL,
                category                    TEXT NOT NULL,
                model                       TEXT,
                serial_number               TEXT,
                part_numbers                TEXT DEFAULT '[]',
                maintenance_frequency_days  INTEGER,
                resource_links              TEXT DEFAULT '{}',
                purchase_date               TEXT,
                warranty_expiry             TEXT,
                notes                       TEXT,
                is_archived                 INTEGER DEFAULT 0,
                created_at                  TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS maintenance_log (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id        INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
                task_performed   TEXT NOT NULL,
                completion_date  TEXT NOT NULL,
                cost_cad         REAL DEFAULT 0.0,
                sourcing_info    TEXT,
                notes            TEXT,
                created_at       TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS schedules (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id          INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
                task_description   TEXT NOT NULL,
                next_due_date      TEXT NOT NULL,
                frequency_days     INTEGER NOT NULL,
                calendar_event_id  TEXT,
                is_active          INTEGER DEFAULT 1,
                created_at         TEXT DEFAULT (datetime('now'))
            );
        """)
        # Migration: add is_archived if upgrading from older schema
        try:
            conn.execute("ALTER TABLE devices ADD COLUMN is_archived INTEGER DEFAULT 0")
        except Exception:
            pass
