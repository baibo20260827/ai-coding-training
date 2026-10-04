#!/usr/bin/env python3
"""Meeting-room training demo: Python standard library, local HTTP, SQLite."""

import argparse
from contextlib import contextmanager
import datetime as dt
import json
from pathlib import Path
import re
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
import uuid

ROOT = Path(__file__).resolve().parent
APPLICATION_ID = 0x4841524E  # HARN: refuse to adopt an unrelated database.
SCHEMA_VERSION = 1
OPEN_MINUTE, CLOSE_MINUTE, SLOT_MINUTES = 9 * 60, 18 * 60, 30
MAX_BODY_BYTES = 8192


class ValidationError(ValueError):
    pass


class BookingConflict(ValueError):
    pass


def validate_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValidationError("日期请使用 YYYY-MM-DD，例如 2026-10-08。")
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        raise ValidationError("日期不存在，请检查年月日。") from None
    return value


def parse_time(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{2}:\d{2}", value):
        raise ValidationError("时间请使用 HH:MM，例如 10:30。")
    hour, minute = map(int, value.split(":"))
    if hour > 23 or minute > 59:
        raise ValidationError("时间不存在，请检查小时和分钟。")
    result = hour * 60 + minute
    if result % SLOT_MINUTES:
        raise ValidationError("请按半小时选择时间，例如 10:00 或 10:30。")
    return result


def format_time(value):
    return "{:02d}:{:02d}".format(*divmod(value, 60))


def overlaps(start, end, other_start, other_end):
    """Half-open intervals: [start, end). Adjacent intervals do not overlap."""
    return start < other_end and other_start < end


def validate_booking(payload):
    if not isinstance(payload, dict):
        raise ValidationError("预约内容必须是 JSON 对象。")
    required = {"date", "start", "end", "name", "purpose"}
    if set(payload) != required:
        raise ValidationError("预约需要且仅包含 date、start、end、name、purpose 五个字段。")
    day = validate_date(payload["date"])
    start, end = parse_time(payload["start"]), parse_time(payload["end"])
    if not OPEN_MINUTE <= start < end <= CLOSE_MINUTE:
        raise ValidationError("预约须在 09:00–18:00 内，结束时间必须晚于开始时间。")
    values = {}
    for key, label, maximum in (("name", "演示姓名", 30), ("purpose", "预约主题", 80)):
        value = payload[key]
        if not isinstance(value, str):
            raise ValidationError(label + "必须是文字。")
        value = value.strip()
        if not 1 <= len(value) <= maximum or any(ord(c) < 32 or ord(c) == 127 for c in value):
            raise ValidationError("{}请填写 1–{} 个字符，不能包含控制字符。".format(label, maximum))
        values[key] = value
    return day, start, end, values["name"], values["purpose"]


class BookingStore:
    def __init__(self, path):
        self.path = Path(path).expanduser().resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            application_id = conn.execute("PRAGMA application_id").fetchone()[0]
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            if application_id not in (0, APPLICATION_ID) or (application_id == 0 and tables):
                raise ValueError("该数据库不是本教学应用创建的文件，请使用一个新的 --db 路径。")
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if application_id == APPLICATION_ID and version != SCHEMA_VERSION:
                raise ValueError("数据库版本不兼容；请保留原文件并使用匹配的应用版本。")
            if application_id == 0:
                conn.executescript("""
                    CREATE TABLE bookings (
                        id TEXT PRIMARY KEY,
                        day TEXT NOT NULL,
                        start_minute INTEGER NOT NULL,
                        end_minute INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        purpose TEXT NOT NULL,
                        CHECK(start_minute >= 540 AND end_minute <= 1080),
                        CHECK(start_minute < end_minute),
                        CHECK(start_minute % 30 = 0 AND end_minute % 30 = 0),
                        CHECK(length(name) BETWEEN 1 AND 30),
                        CHECK(length(purpose) BETWEEN 1 AND 80)
                    );
                    CREATE TABLE slots (
                        day TEXT NOT NULL,
                        start_minute INTEGER NOT NULL,
                        booking_id TEXT NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
                        PRIMARY KEY(day, start_minute)
                    );
                    CREATE INDEX bookings_day ON bookings(day, start_minute);
                """)
                conn.execute("PRAGMA application_id = {}".format(APPLICATION_ID))
                conn.execute("PRAGMA user_version = {}".format(SCHEMA_VERSION))

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(str(self.path), timeout=5.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    @staticmethod
    def _public(row):
        return {"id": row["id"], "date": row["day"],
                "start": format_time(row["start_minute"]), "end": format_time(row["end_minute"]),
                "name": row["name"], "purpose": row["purpose"]}

    def list_bookings(self, day):
        validate_date(day)
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM bookings WHERE day = ? ORDER BY start_minute", (day,)).fetchall()
            return [self._public(row) for row in rows]

    def create_booking(self, payload):
        day, start, end, name, purpose = validate_booking(payload)
        booking_id = uuid.uuid4().hex
        with self._connect() as conn:
            # R03/R08: the transaction and unique occupied slots are the actual guard.
            # A Python 'check then insert' without a transaction would race.
            conn.execute("BEGIN IMMEDIATE")
            try:
                conn.execute("INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?)",
                             (booking_id, day, start, end, name, purpose))
                conn.executemany("INSERT INTO slots VALUES (?, ?, ?)",
                                 [(day, minute, booking_id) for minute in range(start, end, SLOT_MINUTES)])
            except sqlite3.IntegrityError:
                raise BookingConflict("该时段已被预约，请刷新列表并选择其他时段。") from None
            row = conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
            return self._public(row)

    def cancel_booking(self, booking_id):
        if not isinstance(booking_id, str) or not re.fullmatch(r"[0-9a-f]{32}", booking_id):
            raise ValidationError("预约编号无效，请刷新列表后重试。")
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
            return cursor.rowcount == 1


def make_server(store, port=8765):
    """R07: loopback only; port=0 is used by tests for an isolated free port."""
    class Handler(BaseHTTPRequestHandler):
        server_version = "HarnessTeaching/1.0"

        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def _send(self, status, data, content_type="application/json; charset=utf-8"):
            body = json.dumps(data, ensure_ascii=False).encode("utf-8") if isinstance(data, (dict, list)) else data
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(body)

        def _error(self, status, code, message):
            self._send(status, {"error": {"code": code, "message": message}})

        def _allowed(self, mutation=False):
            port = self.server.server_port
            hosts = {"127.0.0.1:{}".format(port), "localhost:{}".format(port)}
            if self.headers.get("Host") not in hosts:
                self._error(403, "local_only", "教学应用仅接受本机 localhost 或 127.0.0.1 访问。")
                return False
            origin = self.headers.get("Origin")
            if mutation and origin is not None and origin not in {"http://" + h for h in hosts}:
                self._error(403, "origin_rejected", "请从本机教学页面提交操作。")
                return False
            return True

        def _run(self, action, mutation=False):
            if not self._allowed(mutation):
                return
            try:
                action()
            except ValidationError as exc:
                self._error(400, "invalid_input", str(exc))
            except BookingConflict as exc:
                self._error(409, "booking_conflict", str(exc))
            except sqlite3.OperationalError:
                self._error(503, "database_unavailable", "数据库暂时不可用，请稍后刷新检查结果；如仍失败，请记录错误并查阅运行说明。")

        def do_GET(self):
            self._run(self._get)

        def _get(self):
            parsed = urlsplit(self.path)
            if parsed.path == "/api/health":
                self._send(200, {"status": "ok", "mode": "local-teaching", "schema_version": SCHEMA_VERSION})
            elif parsed.path == "/api/bookings":
                query = parse_qs(parsed.query, keep_blank_values=True)
                if set(query) != {"date"} or len(query["date"]) != 1:
                    raise ValidationError("查询需要一个 date 参数，例如 ?date=2026-10-08。")
                self._send(200, {"bookings": store.list_bookings(query["date"][0])})
            else:
                assets = {"/": ("index.html", "text/html; charset=utf-8"),
                          "/assets/style.css": ("style.css", "text/css; charset=utf-8"),
                          "/assets/app.js": ("app.js", "text/javascript; charset=utf-8")}
                if parsed.path not in assets:
                    self._error(404, "not_found", "未找到该页面或接口。")
                    return
                name, content_type = assets[parsed.path]
                self._send(200, (ROOT / "static" / name).read_bytes(), content_type)

        def do_POST(self):
            self._run(self._post, mutation=True)

        def _post(self):
            if self.path != "/api/bookings":
                self._error(404, "not_found", "未找到该接口。")
                return
            if self.headers.get_content_type() != "application/json":
                self._error(415, "json_required", "请使用 application/json 提交预约。")
                return
            if self.headers.get("Transfer-Encoding"):
                raise ValidationError("不支持分块请求，请提供 Content-Length。")
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                raise ValidationError("Content-Length 无效。") from None
            if not 0 < length <= MAX_BODY_BYTES:
                self._error(413, "body_size", "请求为空或过大，最多允许 8192 字节。")
                return
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                raise ValidationError("JSON 内容无法读取，请检查格式。") from None
            self._send(201, {"booking": store.create_booking(payload)})

        def do_DELETE(self):
            self._run(self._delete, mutation=True)

        def _delete(self):
            match = re.fullmatch(r"/api/bookings/([0-9a-f]{32})", self.path)
            if not match:
                self._error(404, "not_found", "未找到该预约接口。")
            elif not store.cancel_booking(match.group(1)):
                self._error(404, "booking_missing", "该预约已不存在，请刷新列表。")
            else:
                self._send(200, {"cancelled": True})

        def do_OPTIONS(self):
            self._error(403, "local_only", "本教学应用不提供跨站访问。")

        def log_message(self, fmt, *args):
            # Default logs contain paths/status, never booking names or request bodies.
            super().log_message(fmt, *args)

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    return server


def main():
    parser = argparse.ArgumentParser(description="会议室预约教学应用：仅本机、虚构数据、无登录。")
    parser.add_argument("--port", type=int, default=8765, help="本机端口，默认 8765")
    parser.add_argument("--db", type=Path, default=ROOT / "data" / "bookings.sqlite3", help="教学数据库文件路径")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("端口必须在 1–65535 之间。")
    try:
        store = BookingStore(args.db)
        server = make_server(store, args.port)
    except (OSError, sqlite3.Error, ValueError) as exc:
        parser.exit(1, "启动失败：{}\n请检查端口、文件权限及数据库路径，保留已有文件。\n".format(exc))
    print("教学应用：http://127.0.0.1:{}\n数据库：{}\n仅使用虚构数据；无身份认证，任意本机操作者可取消预约。\n按 Ctrl+C 停止。".format(args.port, store.path), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。数据库文件保留。", flush=True)
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
