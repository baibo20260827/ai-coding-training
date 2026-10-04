#!/usr/bin/env python3
"""Pre-planted teaching defects; the real application is never modified."""

from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from demo.app import BookingConflict, BookingStore, overlaps


def old_conflict(start, end, occupied_start, occupied_end):
    """故障 A：误用闭区间，相邻时段也判冲突。"""
    return start <= occupied_end and occupied_start <= end


def wrong_fix(start, end, occupied_start, occupied_end):
    """故障 B：仅拒绝完全相同的时段，部分重叠被放过。"""
    return start == occupied_start and end == occupied_end


# These acceptance expectations come from the teaching requirements baseline.
ACCEPTANCE = [
    ("相邻允许", (660, 720, 600, 660), False),
    ("部分重叠拒绝", (630, 690, 600, 660), True),
    ("完全相同拒绝", (600, 660, 600, 660), True),
    ("包含已有时段拒绝", (570, 690, 600, 660), True),
]


def run_examples(function, examples):
    failures = []
    for label, args, expected in examples:
        actual = function(*args)
        if actual != expected:
            failures.append(label)
    return failures


def main():
    print("虚构教学故障演练｜不会修改主应用、持久数据或测试预期")
    print("\n1. 期待：10:00–11:00 后，应允许 11:00–12:00。")
    old_failures = run_examples(old_conflict, ACCEPTANCE)
    assert old_failures == ["相邻允许"]
    print("   旧实现独立验收失败：" + "、".join(old_failures))
    print("\n2. 预设错误修复：只检查两段时间完全相同。")
    weak_tests = [ACCEPTANCE[0], ("被改错的部分重叠预期", (630, 690, 600, 660), False), ACCEPTANCE[2]]
    assert run_examples(wrong_fix, weak_tests) == []
    print("   弱测试 3/3 通过：其中一条把『重叠拒绝』改成『允许』。")
    detected = run_examples(wrong_fix, ACCEPTANCE)
    assert detected == ["部分重叠拒绝", "包含已有时段拒绝"]
    print("   需求独立验收发现：" + "、".join(detected))
    print("\n3. 正确规则：[开始, 结束)，相邻不重叠。")
    assert run_examples(overlaps, ACCEPTANCE) == []
    print("   正确区间判定：独立验收 4/4 通过。")
    with tempfile.TemporaryDirectory(prefix="harness-failure-") as directory:
        store = BookingStore(Path(directory) / "lab.sqlite3")
        base = {"date": "2026-10-08", "start": "10:00", "end": "11:00", "name": "演示同事 A", "purpose": "故障演练"}
        store.create_booking(base)
        store.create_booking(dict(base, start="11:00", end="12:00"))
        try:
            store.create_booking(dict(base, start="10:30", end="11:30"))
        except BookingConflict:
            pass
        else:
            raise AssertionError("主应用放过重叠预约")
        assert len(store.list_bookings(base["date"])) == 2
        print("   主应用 SQLite 行为：相邻成功，重叠被拒绝，数据库仅保留 2 条。")
        print("\n4. 新手情境：页面内存重建后，临时记录消失。")
        page_memory = [dict(base)]
        assert len(page_memory) == 1
        page_memory = []  # Explicit simulation of rebuilding page-only state.
        assert page_memory == []
        reopened = BookingStore(store.path)
        assert len(reopened.list_bookings(base["date"])) == 2
        print("   内存模型重建：0 条；重新连接主应用数据库：2 条。")
        print("   此步骤是内存模型模拟；真实浏览器刷新另按 README 操作验证。")
    print("\n演练 PASS：预设缺陷被稳定发现，正确实现通过。退出码 0 表示演练成功，不表示错误实现正确。")


if __name__ == "__main__":
    main()
