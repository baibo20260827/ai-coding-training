import concurrent.futures
import http.client
import json
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest

from demo.app import BookingConflict, BookingStore, ValidationError, make_server
from demo.backup import copy_snapshot

DAY = "2026-10-08"


def booking(**changes):
    values = {"date": DAY, "start": "10:00", "end": "11:00", "name": "演示同事 A", "purpose": "验收练习"}
    values.update(changes)
    return values


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="harness-test-")
        self.path = Path(self.directory.name) / "bookings.sqlite3"
        self.store = BookingStore(self.path)

    def tearDown(self):
        self.directory.cleanup()

    def test_R01_empty_and_date_filtered_order(self):
        self.assertEqual(self.store.list_bookings(DAY), [])
        self.store.create_booking(booking(start="13:00", end="14:00"))
        self.store.create_booking(booking())
        self.store.create_booking(booking(date="2026-10-09"))
        self.assertEqual([b["start"] for b in self.store.list_bookings(DAY)], ["10:00", "13:00"])

    def test_R02_create_returns_saved_fields(self):
        result = self.store.create_booking(booking(name="  演示同事 B  "))
        self.assertEqual(result["name"], "演示同事 B")
        self.assertRegex(result["id"], r"^[0-9a-f]{32}$")
        self.assertEqual(self.store.list_bookings(DAY), [result])

    def test_R03_adjacent_on_both_sides_allowed(self):
        self.store.create_booking(booking())
        self.store.create_booking(booking(start="09:00", end="10:00"))
        self.store.create_booking(booking(start="11:00", end="12:00"))
        self.assertEqual(len(self.store.list_bookings(DAY)), 3)

    def test_R03_overlap_variations_rejected_and_no_partial_rows(self):
        self.store.create_booking(booking())
        for start, end in [("10:00", "11:00"), ("09:30", "10:30"), ("10:30", "11:30"), ("09:00", "12:00"), ("10:00", "10:30")]:
            with self.subTest(start=start, end=end), self.assertRaises(BookingConflict):
                self.store.create_booking(booking(start=start, end=end))
        self.assertEqual(len(self.store.list_bookings(DAY)), 1)
        with sqlite3.connect(str(self.path)) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM slots").fetchone()[0], 2)
        # A failed multi-slot insert must not keep its initially free slot.
        self.store.create_booking(booking(start="09:00", end="10:00"))

    def test_R03_same_time_different_date_allowed(self):
        self.store.create_booking(booking())
        self.store.create_booking(booking(date="2026-10-09"))
        self.assertEqual(len(self.store.list_bookings("2026-10-09")), 1)

    def test_R04_cancel_releases_slots_and_missing_is_false(self):
        result = self.store.create_booking(booking())
        self.assertTrue(self.store.cancel_booking(result["id"]))
        self.assertFalse(self.store.cancel_booking(result["id"]))
        self.assertEqual(self.store.list_bookings(DAY), [])
        self.store.create_booking(booking())

    def test_R05_reopen_preserves_booking_and_cancel(self):
        result = self.store.create_booking(booking())
        reopened = BookingStore(self.path)
        self.assertEqual(reopened.list_bookings(DAY), [result])
        reopened.cancel_booking(result["id"])
        self.assertEqual(BookingStore(self.path).list_bookings(DAY), [])

    def test_R06_invalid_inputs_rejected_without_writes(self):
        invalid = [booking(date="2026-02-30"), booking(date="2026-1-01"), booking(date=None),
                   booking(start="10:15"), booking(start="24:00"), booking(start="09:60"), booking(start=10),
                   booking(start="08:30"), booking(end="18:30"), booking(start="11:00", end="10:00"),
                   booking(end="10:00"), booking(name=" "), booking(name="a" * 31), booking(purpose="a" * 81),
                   booking(name=5), booking(purpose="a\nb"), [], {}, dict(booking(), extra="x")]
        for value in invalid:
            with self.subTest(payload=value), self.assertRaises(ValidationError):
                self.store.create_booking(value)
        self.assertEqual(self.store.list_bookings(DAY), [])

    def test_R06_opening_and_closing_boundaries_allowed(self):
        self.store.create_booking(booking(start="09:00", end="09:30"))
        self.store.create_booking(booking(start="17:30", end="18:00"))

    def test_R06_invalid_cancel_id_rejected(self):
        with self.assertRaises(ValidationError):
            self.store.cancel_booking("not-an-id")

    def test_R06_text_is_stored_as_data(self):
        result = self.store.create_booking(booking(name="<script>alert(1)</script>", purpose="'; DROP TABLE bookings;--"))
        self.assertEqual(self.store.list_bookings(DAY), [result])

    def test_R08_simultaneous_identical_requests_exactly_one_success(self):
        barrier = threading.Barrier(8)
        def attempt(index):
            barrier.wait(timeout=5)
            try:
                self.store.create_booking(booking(name="演示同事 {}".format(index)))
                return "created"
            except BookingConflict:
                return "conflict"
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(attempt, range(8)))
        self.assertEqual(results.count("created"), 1)
        self.assertEqual(results.count("conflict"), 7)
        self.assertEqual(len(self.store.list_bookings(DAY)), 1)

    def test_R08_simultaneous_adjacent_requests_all_succeed(self):
        barrier = threading.Barrier(3)
        def attempt(index):
            barrier.wait(timeout=5)
            return self.store.create_booking(booking(start="{}:00".format(10 + index), end="{}:00".format(11 + index)))
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            self.assertEqual(len(list(pool.map(attempt, range(3)))), 3)
        self.assertEqual(len(self.store.list_bookings(DAY)), 3)

    def test_unrelated_database_is_not_adopted(self):
        unrelated = Path(self.directory.name) / "other.sqlite3"
        with sqlite3.connect(str(unrelated)) as conn:
            conn.execute("CREATE TABLE customer_data (value TEXT)")
            conn.execute("INSERT INTO customer_data VALUES ('preserve')")
        with self.assertRaises(ValueError):
            BookingStore(unrelated)
        with sqlite3.connect(str(unrelated)) as conn:
            self.assertEqual(conn.execute("SELECT value FROM customer_data").fetchone()[0], "preserve")

    def test_backup_restore_new_path_and_refuse_overwrite(self):
        result = self.store.create_booking(booking())
        snapshot = Path(self.directory.name) / "snapshot.sqlite3"
        restored = Path(self.directory.name) / "restored.sqlite3"
        self.assertEqual(copy_snapshot(self.path, snapshot), 1)
        self.store.cancel_booking(result["id"])
        self.assertEqual(copy_snapshot(snapshot, restored), 1)
        self.assertEqual(BookingStore(restored).list_bookings(DAY), [result])
        with self.assertRaises(FileExistsError):
            copy_snapshot(snapshot, self.path)
        self.assertEqual(self.store.list_bookings(DAY), [])


class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="harness-http-")
        self.store = BookingStore(Path(self.directory.name) / "http.sqlite3")
        self.server = make_server(self.store, port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": .02}, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.directory.cleanup()

    def request(self, method, path, payload=None, headers=None, raw=None):
        supplied = {"Content-Type": "application/json"}
        supplied.update(headers or {})
        body = json.dumps(payload).encode() if payload is not None else raw
        conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        conn.request(method, path, body=body, headers=supplied)
        response = conn.getresponse()
        content = response.read()
        status, response_headers = response.status, dict(response.getheaders())
        conn.close()
        if "application/json" in response_headers.get("Content-Type", ""):
            content = json.loads(content)
        return status, content, response_headers

    def test_R01_static_assets_and_health(self):
        for path, content_type in [("/", "text/html"), ("/assets/app.js", "text/javascript"), ("/assets/style.css", "text/css")]:
            status, content, headers = self.request("GET", path)
            self.assertEqual(status, 200)
            self.assertIn(content_type, headers["Content-Type"])
            self.assertTrue(content)
        self.assertEqual(self.request("GET", "/api/health")[1]["mode"], "local-teaching")

    def test_R01_R02_R04_R05_http_create_read_cancel(self):
        self.assertEqual(self.request("GET", "/api/bookings?date=" + DAY)[1], {"bookings": []})
        status, body, _ = self.request("POST", "/api/bookings", booking())
        self.assertEqual(status, 201)
        record = body["booking"]
        self.assertEqual(self.request("GET", "/api/bookings?date=" + DAY)[1]["bookings"], [record])
        self.assertEqual(BookingStore(self.store.path).list_bookings(DAY), [record])
        self.assertEqual(self.request("DELETE", "/api/bookings/" + record["id"])[0], 200)
        self.assertEqual(self.request("DELETE", "/api/bookings/" + record["id"])[0], 404)
        self.assertEqual(self.request("GET", "/api/bookings?date=" + DAY)[1]["bookings"], [])

    def test_R03_http_conflict_is_409_adjacent_is_201(self):
        self.request("POST", "/api/bookings", booking())
        status, body, _ = self.request("POST", "/api/bookings", booking(start="10:30", end="11:30"))
        self.assertEqual(status, 409)
        self.assertEqual(body["error"]["code"], "booking_conflict")
        self.assertEqual(self.request("POST", "/api/bookings", booking(start="11:00", end="12:00"))[0], 201)

    def test_R06_http_malformed_body_and_input(self):
        for raw in (b"{", b"\xff"):
            self.assertEqual(self.request("POST", "/api/bookings", raw=raw)[0], 400)
        self.assertEqual(self.request("POST", "/api/bookings", booking(start="08:00"))[0], 400)
        self.assertEqual(self.request("POST", "/api/bookings", booking(), headers={"Content-Type": "text/plain"})[0], 415)
        self.assertEqual(self.request("POST", "/api/bookings", raw=b"x" * 8193)[0], 413)
        self.assertEqual(self.request("GET", "/api/bookings")[0], 400)
        self.assertEqual(self.request("GET", "/api/bookings?date=" + DAY + "&date=" + DAY)[0], 400)

    def test_R07_bind_loopback_origin_and_host_guards(self):
        self.assertEqual(self.server.server_address[0], "127.0.0.1")
        self.assertEqual(self.request("GET", "/", headers={"Host": "evil.example"})[0], 403)
        self.assertEqual(self.request("POST", "/api/bookings", booking(), headers={"Origin": "https://evil.example"})[0], 403)
        self.assertEqual(self.request("OPTIONS", "/api/bookings")[0], 403)
        origin = "http://127.0.0.1:{}".format(self.server.server_port)
        self.assertEqual(self.request("POST", "/api/bookings", booking(), headers={"Origin": origin})[0], 201)
        self.assertEqual(self.request("GET", "/../../app.py")[0], 404)

    def test_R08_http_concurrent_requests_one_201_others_409(self):
        barrier = threading.Barrier(4)
        def attempt(_):
            barrier.wait(timeout=5)
            return self.request("POST", "/api/bookings", booking())[0]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            statuses = list(pool.map(attempt, range(4)))
        self.assertEqual(sorted(statuses), [201, 409, 409, 409])
        self.assertEqual(len(self.store.list_bookings(DAY)), 1)


if __name__ == "__main__":
    unittest.main()
