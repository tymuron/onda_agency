"""Cookieless, privacy-friendly web analytics for the Onda site.

- Production: Postgres (Neon) via asyncpg, selected when DATABASE_URL is a
  postgres URL.
- Local/dev: SQLite via aiosqlite (default backend/analytics.db) so the whole
  funnel can be verified without any cloud credentials.

Portability is kept trivial by storing `ts` and `day` as ISO/`YYYY-MM-DD`
strings computed in Python, so every aggregate query is plain ANSI SQL that
runs identically on both backends.

No cookies, no persistent client identifier, no PII stored. Unique visitors are
counted via a daily-rotating salted hash of IP+UA (the AEPD/CNIL pattern for
consent-exempt audience measurement). Sessions use an ephemeral
sessionStorage id generated client-side.
"""
from __future__ import annotations

import asyncio
import datetime as _dt
import hashlib
import json
import logging
import os
import re
import secrets
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger("onda.analytics")

EVENT_TYPES = {
    "pageview",
    "scroll",
    "cta_click",
    "nav_click",
    "form_view",
    "form_submit",
}

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_SQLITE = os.path.join(_BASE_DIR, "backend", "analytics.db")

_SCHEMA_SQLITE = """
CREATE TABLE IF NOT EXISTS events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    ts           TEXT NOT NULL,
    day          TEXT NOT NULL,
    event_type   TEXT NOT NULL,
    session_id   TEXT,
    visitor_hash TEXT,
    page         TEXT,
    lang         TEXT,
    referrer_host TEXT,
    utm_source   TEXT,
    device       TEXT,
    country      TEXT,
    scroll_depth INTEGER,
    meta         TEXT
);
"""
_SCHEMA_PG = _SCHEMA_SQLITE.replace(
    "INTEGER PRIMARY KEY AUTOINCREMENT", "BIGSERIAL PRIMARY KEY"
)
_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_events_day ON events(day)",
    "CREATE INDEX IF NOT EXISTS idx_events_type_day ON events(event_type, day)",
    "CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id)",
    "CREATE INDEX IF NOT EXISTS idx_events_visitor ON events(visitor_hash, day)",
]

_INSERT = """
INSERT INTO events
 (ts, day, event_type, session_id, visitor_hash, page, lang,
  referrer_host, utm_source, device, country, scroll_depth, meta)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

# ---------------------------------------------------------------------------
# Cookieless identity helpers
# ---------------------------------------------------------------------------
_salts: Dict[str, str] = {}


def _daily_salt() -> str:
    today = _dt.datetime.utcnow().strftime("%Y-%m-%d")
    salt = _salts.get(today)
    if salt is None:
        salt = secrets.token_hex(16)
        _salts.clear()
        _salts[today] = salt
    return salt


def visitor_hash(ip: str, ua: str) -> str:
    return hashlib.sha256(f"{_daily_salt()}|{ip}|{ua}".encode()).hexdigest()[:32]


_MOBILE_RE = re.compile(r"Mobi|Android|iPhone|iPod", re.I)
_TABLET_RE = re.compile(r"iPad|Tablet", re.I)


def device_from_ua(ua: str) -> str:
    if _TABLET_RE.search(ua or ""):
        return "tablet"
    if _MOBILE_RE.search(ua or ""):
        return "mobile"
    return "desktop"


def referrer_host(referrer: str, site_host: str) -> Optional[str]:
    if not referrer:
        return None
    try:
        host = urlparse(referrer).hostname or None
    except Exception:
        return None
    if host and site_host and host.endswith(site_host):
        return None  # internal navigation = not a source
    return host


def utm_source_from(page: str, referrer: str) -> Optional[str]:
    for u in (page, referrer):
        if not u:
            continue
        try:
            qs = parse_qs(urlparse(u).query)
        except Exception:
            continue
        if qs.get("utm_source"):
            return qs["utm_source"][0][:64]
    return None


# ---------------------------------------------------------------------------
# DB abstraction
# ---------------------------------------------------------------------------
class AnalyticsDB:
    def __init__(self, database_url: Optional[str]):
        url = (database_url or "").strip()
        self.is_pg = url.startswith("postgres://") or url.startswith("postgresql://")
        self.url = url
        self._pool = None          # asyncpg pool
        self._sqlite = None        # aiosqlite connection
        self._lock = asyncio.Lock()
        self.ready = False

    async def connect(self) -> None:
        try:
            if self.is_pg:
                import asyncpg

                dsn = self.url.replace("postgres://", "postgresql://", 1)
                self._pool = await asyncpg.create_pool(
                    dsn, min_size=1, max_size=5, command_timeout=10
                )
                async with self._pool.acquire() as con:
                    await con.execute(_SCHEMA_PG)
                    for ix in _INDEXES:
                        await con.execute(ix)
            else:
                import aiosqlite

                path = self.url[len("sqlite://"):] if self.url.startswith("sqlite://") else _DEFAULT_SQLITE
                self._sqlite = await aiosqlite.connect(path or _DEFAULT_SQLITE)
                self._sqlite.row_factory = aiosqlite.Row
                await self._sqlite.executescript(_SCHEMA_SQLITE)
                for ix in _INDEXES:
                    await self._sqlite.execute(ix)
                await self._sqlite.commit()
            self.ready = True
            logger.info(
                "Analytics DB ready (%s)", "postgres" if self.is_pg else "sqlite"
            )
        except Exception as e:  # never let analytics break the app
            self.ready = False
            logger.error("Analytics DB connect failed: %s", e)

    async def close(self) -> None:
        try:
            if self._pool:
                await self._pool.close()
            if self._sqlite:
                await self._sqlite.close()
        except Exception:
            pass

    @staticmethod
    def _to_pg(sql: str) -> str:
        idx = 0

        def repl(_m):
            nonlocal idx
            idx += 1
            return f"${idx}"

        return re.sub(r"\?", repl, sql)

    async def _exec(self, sql: str, params: Tuple) -> None:
        if not self.ready:
            return
        try:
            if self.is_pg:
                async with self._pool.acquire() as con:
                    await con.execute(self._to_pg(sql), *params)
            else:
                async with self._lock:
                    await self._sqlite.execute(sql, params)
                    await self._sqlite.commit()
        except Exception as e:
            logger.error("Analytics insert failed: %s", e)

    async def _query(self, sql: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        if not self.ready:
            return []
        try:
            if self.is_pg:
                async with self._pool.acquire() as con:
                    rows = await con.fetch(self._to_pg(sql), *params)
                    return [dict(r) for r in rows]
            else:
                async with self._lock:
                    cur = await self._sqlite.execute(sql, params)
                    rows = await cur.fetchall()
                    return [dict(r) for r in rows]
        except Exception as e:
            logger.error("Analytics query failed: %s", e)
            return []

    # -- writes -----------------------------------------------------------
    async def insert_event(self, ev: Dict[str, Any]) -> None:
        now = _dt.datetime.utcnow()
        await self._exec(
            _INSERT,
            (
                now.isoformat(timespec="seconds") + "Z",
                now.strftime("%Y-%m-%d"),
                ev["event_type"],
                ev.get("session_id"),
                ev.get("visitor_hash"),
                ev.get("page"),
                ev.get("lang"),
                ev.get("referrer_host"),
                ev.get("utm_source"),
                ev.get("device"),
                ev.get("country"),
                ev.get("scroll_depth"),
                json.dumps(ev.get("meta")) if ev.get("meta") else None,
            ),
        )

    # -- reads (dashboard) ------------------------------------------------
    async def funnel(self, d0: str, d1: str) -> Dict[str, int]:
        sql = """
        SELECT
          COUNT(DISTINCT session_id) AS landing,
          COUNT(DISTINCT CASE WHEN event_type='scroll' AND scroll_depth>=50
                THEN session_id END) AS scrolled,
          COUNT(DISTINCT CASE WHEN event_type='nav_click'
                 OR (event_type='pageview' AND (page LIKE '%portfolio%'
                     OR page LIKE '%process%' OR page LIKE '%/examples/%'))
                THEN session_id END) AS explored,
          COUNT(DISTINCT CASE WHEN event_type='form_view'
                THEN session_id END) AS form_view,
          COUNT(DISTINCT CASE WHEN event_type='form_submit'
                THEN session_id END) AS form_submit
        FROM events WHERE day BETWEEN ? AND ?
        """
        rows = await self._query(sql, (d0, d1))
        if not rows:
            return {k: 0 for k in
                    ("landing", "scrolled", "explored", "form_view", "form_submit")}
        return {k: int(v or 0) for k, v in rows[0].items()}

    async def timeseries(self, d0: str, d1: str) -> List[Dict[str, Any]]:
        sql = """
        SELECT day,
          COUNT(DISTINCT visitor_hash) AS visitors,
          SUM(CASE WHEN event_type='pageview' THEN 1 ELSE 0 END) AS pageviews
        FROM events WHERE day BETWEEN ? AND ?
        GROUP BY day ORDER BY day
        """
        return await self._query(sql, (d0, d1))

    async def breakdown(self, field: str, d0: str, d1: str,
                        limit: int = 12) -> List[Dict[str, Any]]:
        allowed = {
            "page": "page", "referrer_host": "referrer_host",
            "device": "device", "country": "country", "lang": "lang",
            "utm_source": "utm_source",
        }
        col = allowed[field]
        sql = f"""
        SELECT COALESCE({col}, 'direct' ) AS label, COUNT(*) AS hits
        FROM events
        WHERE event_type='pageview' AND day BETWEEN ? AND ?
        GROUP BY COALESCE({col}, 'direct')
        ORDER BY hits DESC LIMIT {int(limit)}
        """
        return await self._query(sql, (d0, d1))

    async def totals(self, d0: str, d1: str) -> Dict[str, int]:
        sql = """
        SELECT
          COUNT(DISTINCT visitor_hash) AS visitors,
          COUNT(DISTINCT session_id) AS sessions,
          SUM(CASE WHEN event_type='pageview' THEN 1 ELSE 0 END) AS pageviews,
          SUM(CASE WHEN event_type='form_submit' THEN 1 ELSE 0 END) AS leads
        FROM events WHERE day BETWEEN ? AND ?
        """
        rows = await self._query(sql, (d0, d1))
        if not rows:
            return {"visitors": 0, "sessions": 0, "pageviews": 0, "leads": 0}
        return {k: int(v or 0) for k, v in rows[0].items()}
