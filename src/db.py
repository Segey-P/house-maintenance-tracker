import psycopg2
import psycopg2.extras
import streamlit as st


def _db_url() -> str:
    try:
        return st.secrets["database"]["url"]
    except Exception:
        raise RuntimeError(
            "Database not configured. "
            "Add [database]\nurl = '...' to .streamlit/secrets.toml"
        )


class _Conn:
    """Thin wrapper around psycopg2 that exposes a sqlite3-style execute() interface."""

    def __init__(self, pg):
        self._pg = pg

    def execute(self, sql: str, params=None):
        cur = self._pg.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql, params)
        return cur

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._pg.rollback()
        else:
            self._pg.commit()
        self._pg.close()
        return False


def get_connection() -> _Conn:
    return _Conn(psycopg2.connect(_db_url()))


def init_db() -> None:
    stmts = [
        """CREATE TABLE IF NOT EXISTS devices (
            id                          SERIAL PRIMARY KEY,
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
            is_archived                 SMALLINT DEFAULT 0,
            created_at                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS maintenance_log (
            id               SERIAL PRIMARY KEY,
            device_id        INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
            task_performed   TEXT NOT NULL,
            completion_date  TEXT NOT NULL,
            cost_cad         REAL DEFAULT 0.0,
            sourcing_info    TEXT,
            notes            TEXT,
            created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS schedules (
            id                 SERIAL PRIMARY KEY,
            device_id          INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
            task_description   TEXT NOT NULL,
            next_due_date      TEXT NOT NULL,
            frequency_days     INTEGER NOT NULL,
            calendar_event_id  TEXT,
            is_active          SMALLINT DEFAULT 1,
            created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        "ALTER TABLE devices ADD COLUMN IF NOT EXISTS is_archived SMALLINT DEFAULT 0",
    ]
    with get_connection() as conn:
        for stmt in stmts:
            conn.execute(stmt)
