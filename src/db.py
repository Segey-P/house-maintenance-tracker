import psycopg2
import psycopg2.extras
import streamlit as st


def _db_params() -> dict:
    try:
        db = st.secrets["database"]
        return dict(
            host=db["host"],
            port=int(db.get("port", 5432)),
            dbname=db.get("dbname", "postgres"),
            user=db["user"],
            password=db["password"],
            sslmode="require",
        )
    except Exception:
        raise RuntimeError(
            "Database not configured. Add [database] section to .streamlit/secrets.toml"
        )


class _Conn:
    """Wraps a psycopg2 connection to expose a sqlite3-style execute() interface."""

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
    return _Conn(psycopg2.connect(**_db_params()))


def init_db() -> None:
    with get_connection() as conn:
        # One-time migration: if service_types table doesn't exist, drop old schema and rebuild
        result = conn.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'service_types')"
        ).fetchone()
        if not result["exists"]:
            conn.execute("DROP TABLE IF EXISTS schedules CASCADE")
            conn.execute("DROP TABLE IF EXISTS maintenance_log CASCADE")
            conn.execute("DROP TABLE IF EXISTS devices CASCADE")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id               SERIAL PRIMARY KEY,
                name             TEXT NOT NULL,
                category         TEXT NOT NULL,
                model            TEXT,
                serial_number    TEXT,
                purchase_date    TEXT,
                warranty_expiry  TEXT,
                notes            TEXT,
                is_archived      SMALLINT DEFAULT 0,
                created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS service_types (
                id              SERIAL PRIMARY KEY,
                device_id       INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
                name            TEXT NOT NULL,
                frequency_days  INTEGER NOT NULL DEFAULT 180,
                part_numbers    TEXT DEFAULT '[]',
                tutorial_url    TEXT,
                purchase_url    TEXT,
                notes           TEXT,
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schedules (
                id                SERIAL PRIMARY KEY,
                device_id         INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
                service_type_id   INTEGER REFERENCES service_types(id) ON DELETE CASCADE,
                task_description  TEXT NOT NULL,
                next_due_date     TEXT NOT NULL,
                frequency_days    INTEGER NOT NULL,
                calendar_event_id TEXT,
                is_active         SMALLINT DEFAULT 1,
                created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS maintenance_log (
                id               SERIAL PRIMARY KEY,
                device_id        INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
                service_type_id  INTEGER REFERENCES service_types(id) ON DELETE SET NULL,
                task_performed   TEXT NOT NULL,
                completion_date  TEXT NOT NULL,
                cost_cad         REAL DEFAULT 0.0,
                sourcing_info    TEXT,
                notes            TEXT,
                created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
