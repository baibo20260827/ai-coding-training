#!/usr/bin/env python3
"""SQLite backup/restore to a NEW path only; never overwrite existing files."""

import argparse
from pathlib import Path
import sqlite3
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from demo.app import APPLICATION_ID, SCHEMA_VERSION, BookingStore


def validate_snapshot(conn):
    if conn.execute("PRAGMA application_id").fetchone()[0] != APPLICATION_ID:
        raise ValueError("源文件不是本教学应用的数据库。")
    if conn.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
        raise ValueError("源数据库版本与当前应用不兼容。")
    if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise ValueError("数据库完整性检查失败。")
    if conn.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("数据库外键检查失败。")
    return conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]


def copy_snapshot(source, output):
    source, output = Path(source).expanduser().resolve(), Path(output).expanduser().resolve()
    if not source.is_file():
        raise ValueError("源文件不存在，请检查路径。")
    if output.exists():
        raise FileExistsError("目标已存在，拒绝覆盖。请提供一个全新的文件名。")
    output.parent.mkdir(parents=True, exist_ok=True)
    created = False
    src = dst = None
    try:
        src = sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)
        validate_snapshot(src)
        # Exclusive creation also prevents a competing process's existing file
        # from being replaced between the exists() check and open().
        with output.open("xb"):
            created = True
        dst = sqlite3.connect(str(output))
        src.backup(dst)
        count = validate_snapshot(dst)
        dst.close()
        dst = None
        return count
    except Exception:
        if dst is not None:
            dst.close()
        if created:
            output.unlink(missing_ok=True)
        raise
    finally:
        if src is not None:
            src.close()


def exercise():
    with tempfile.TemporaryDirectory(prefix="harness-recovery-") as directory:
        folder = Path(directory)
        original = folder / "original.sqlite3"
        snapshot = folder / "snapshot.sqlite3"
        restored = folder / "restored.sqlite3"
        store = BookingStore(original)
        record = store.create_booking({"date": "2026-10-08", "start": "10:00", "end": "11:00", "name": "演示同事 A", "purpose": "恢复演练"})
        assert copy_snapshot(original, snapshot) == 1
        assert store.cancel_booking(record["id"])
        assert store.list_bookings("2026-10-08") == []
        assert copy_snapshot(snapshot, restored) == 1
        assert len(BookingStore(restored).list_bookings("2026-10-08")) == 1
        assert store.list_bookings("2026-10-08") == []
        try:
            copy_snapshot(snapshot, original)
        except FileExistsError:
            pass
        else:
            raise AssertionError("Expected existing destination to be protected")
        print("PASS：备份含 1 条预约；取消后原库 0 条；恢复到新库 1 条。")
        print("PASS：原库保持 0 条，覆盖已有目标被拒绝。")
        print("演练完成：仅使用自动清理的临时目录，未触碰 demo/data 或用户文件。")


def main():
    parser = argparse.ArgumentParser(description="教学数据库备份/恢复：目标必须是新文件。")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("backup", "restore"):
        command = commands.add_parser(name)
        command.add_argument("--source", type=Path, required=True)
        command.add_argument("--output", type=Path, required=True)
    commands.add_parser("exercise", help="在临时目录自动演练备份、恢复和拒绝覆盖")
    args = parser.parse_args()
    try:
        if args.command == "exercise":
            exercise()
        else:
            count = copy_snapshot(args.source, args.output)
            print("完成：{}，包含 {} 条预约。原文件保持不变。".format(args.output.resolve(), count))
    except (OSError, sqlite3.Error, ValueError) as exc:
        parser.exit(1, "未执行完成：{}\n".format(exc))


if __name__ == "__main__":
    main()
