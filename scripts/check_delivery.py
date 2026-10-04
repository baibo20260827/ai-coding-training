#!/usr/bin/env python3
"""Portable, offline delivery checks using only the Python standard library.

Run from any directory: python3 /path/to/project/scripts/check_delivery.py
An extracted package can also be checked with --root /path/to/package.
Exit 0 means the requested structural checks passed, not training acceptance.
"""

import argparse
import datetime as dt
from html import unescape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import posixpath
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile


PRESENTATIONS = {"manager": 14, "engineer": 18, "beginner": 18}
VIEWS = ("ba", "aa", "da", "ta")
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def excluded(relative):
    return (any(part in {".git", "dist", "__pycache__"} for part in relative.parts)
            or relative.parts[:3] == ("evidence", "slides", "build"))


def documents(root):
    for directory, dirs, files in os.walk(root, followlinks=False):
        folder = Path(directory)
        dirs[:] = [name for name in dirs if not excluded((folder / name).relative_to(root))]
        for name in sorted(files):
            path = folder / name
            if path.suffix.lower() in {".md", ".html", ".htm"} and not excluded(path.relative_to(root)):
                yield path


def without_code(text):
    """Remove fenced and inline code examples, preserving line numbers."""
    lines, fence = [], None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is None and match:
            fence = match.group(1)
            lines.append("\n" if line.endswith("\n") else "")
        elif fence is not None:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
            lines.append("\n" if line.endswith("\n") else "")
        else:
            lines.append(re.sub(r"(`+)(.*?)\1", lambda m: " " * len(m.group(0)), line))
    return "".join(lines)


def markdown_targets(text):
    """Read inline destinations and reference definitions, including <paths>.

    Balanced parentheses and backslash escapes in destinations are supported;
    labels and optional link titles are irrelevant to file-existence checks.
    """
    for match in re.finditer(r"\]\(\s*", text):
        start = index = match.end()
        if index >= len(text):
            continue
        if text[index] == "<":
            end = text.find(">", index + 1)
            if end < 0:
                continue
            target = text[index + 1:end]
        else:
            depth = 0
            while index < len(text):
                character = text[index]
                if character == "\\" and index + 1 < len(text):
                    index += 2
                    continue
                if character == "(":
                    depth += 1
                elif character == ")":
                    if depth == 0:
                        break
                    depth -= 1
                elif character.isspace() and depth == 0:
                    break
                index += 1
            target = text[start:index]
        yield text.count("\n", 0, match.start()) + 1, re.sub(r"\\(.)", r"\1", target)
    for match in re.finditer(r"^\s{0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|(\S+))", text, re.MULTILINE):
        yield text.count("\n", 0, match.start()) + 1, re.sub(r"\\(.)", r"\1", match.group(1) or match.group(2))


class LocalHTMLTargets(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.targets = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.targets.append((self.getpos()[0], value))

    handle_startendtag = handle_starttag


def local_target(root, source, target):
    target = unescape(target.strip().strip("<>"))
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[A-Za-z]:[\\/]", target):
        raise ValueError("absolute_machine_path")
    parsed = urlsplit(target)
    if parsed.scheme == "file":
        raise ValueError("absolute_machine_path")
    if parsed.scheme or parsed.netloc:
        return None  # No external requests: includes HTTP, mailto, data, etc.
    decoded = unquote(parsed.path)
    if not decoded:
        return None
    # The demo's HTTP route /assets/* is explicitly backed by demo/static/*.
    # These are application URLs, not paths at the computer's filesystem root.
    if source.relative_to(root).as_posix() == "demo/static/index.html" and decoded.startswith("/assets/"):
        resolved = source.parent / decoded.removeprefix("/assets/")
    elif decoded.startswith("/"):
        resolved = root / decoded.lstrip("/")
    else:
        resolved = source.parent / decoded
    resolved = resolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError("target_outside_package") from None
    return resolved


def package_part(source_part, target):
    return (posixpath.normpath(target.lstrip("/")) if target.startswith("/")
            else posixpath.normpath(posixpath.join(posixpath.dirname(source_part), target)))


def relationships(archive, part):
    folder, filename = posixpath.split(part)
    relpart = posixpath.join(folder, "_rels", filename + ".rels")
    return {element.attrib["Id"]: element.attrib for element in ET.fromstring(archive.read(relpart))}


def check_presentation(path, expected):
    result = {"path": path.as_posix(), "expected_slides": expected, "slides": 0,
              "slides_with_notes": 0, "missing_notes_pages": [], "status": "fail"}
    with ZipFile(path) as archive:
        bad_part = archive.testzip()
        if bad_part:
            raise ValueError("ZIP CRC failure: " + bad_part)
        presentation_part = "ppt/presentation.xml"
        presentation = ET.fromstring(archive.read(presentation_part))
        rels = relationships(archive, presentation_part)
        slide_ids = presentation.findall("p:sldIdLst/p:sldId", NS)
        result["slides"] = len(slide_ids)
        for number, slide_id in enumerate(slide_ids, 1):
            relation = rels[slide_id.attrib["{" + NS["r"] + "}id"]]
            slide_part = package_part(presentation_part, relation["Target"])
            ET.fromstring(archive.read(slide_part))
            slide_rels = relationships(archive, slide_part)
            note_relations = [rel for rel in slide_rels.values() if rel["Type"].endswith("/notesSlide")]
            notes_text = []
            for note in note_relations:
                note_xml = ET.fromstring(archive.read(package_part(slide_part, note["Target"])))
                for shape in note_xml.findall(".//p:sp", NS):
                    placeholder = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
                    if placeholder is not None and placeholder.get("type") == "body":
                        notes_text.extend(node.text or "" for node in shape.findall(".//a:t", NS))
            if "".join(notes_text).strip():
                result["slides_with_notes"] += 1
            else:
                result["missing_notes_pages"].append(number)
        if result["slides"] == expected and not result["missing_notes_pages"]:
            result["status"] = "pass"
    return result


def run(root):
    root = Path(root).expanduser().resolve()
    result = {"schema_version": 1,
              "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
              "status": "pass", "scope": "offline structural delivery checks; no visual or learning-effect assessment",
              "excluded": ["evidence/slides/build", "dist", ".git", "__pycache__"],
              "documents": {"markdown": 0, "html": 0, "local_links_checked": 0, "external_or_anchor_links_ignored": 0},
              "svg": [], "presentations": [], "errors": []}
    for source in sorted(documents(root)):
        relative = source.relative_to(root).as_posix()
        try:
            text = source.read_text(encoding="utf-8")
            is_markdown = source.suffix.lower() == ".md"
            result["documents"]["markdown" if is_markdown else "html"] += 1
            if is_markdown:
                text = without_code(text)
            targets = list(markdown_targets(text)) if is_markdown else []
            parser = LocalHTMLTargets()
            parser.feed(text)
            targets.extend(parser.targets)
            for line, target in targets:
                try:
                    resolved = local_target(root, source, target)
                    if resolved is None:
                        result["documents"]["external_or_anchor_links_ignored"] += 1
                        continue
                    result["documents"]["local_links_checked"] += 1
                    if not resolved.exists():
                        result["errors"].append({"kind": "broken_link", "source": relative, "line": line,
                                                 "target": target, "resolved": resolved.relative_to(root).as_posix()})
                except (ValueError, OSError) as exc:
                    result["errors"].append({"kind": "invalid_local_link", "source": relative,
                                             "line": line, "target": target, "reason": str(exc)})
        except (OSError, UnicodeError) as exc:
            result["errors"].append({"kind": "document_unreadable", "source": relative, "reason": str(exc)})
    for view in VIEWS:
        relative = "docs/architecture-views/{}.svg".format(view)
        entry = {"path": relative, "status": "pass"}
        try:
            ET.parse(root / relative)
        except (OSError, ET.ParseError) as exc:
            entry["status"] = "fail"
            result["errors"].append({"kind": "svg_unreadable", "source": relative, "reason": str(exc)})
        result["svg"].append(entry)
    for name, count in PRESENTATIONS.items():
        relative = "training/slides/{}.pptx".format(name)
        try:
            entry = check_presentation(root / relative, count)
            entry["path"] = relative
            if entry["status"] != "pass":
                result["errors"].append({"kind": "presentation_structure", "source": relative,
                                         "slides": entry["slides"], "expected_slides": count,
                                         "missing_notes_pages": entry["missing_notes_pages"]})
        except (OSError, BadZipFile, ET.ParseError, KeyError, ValueError) as exc:
            entry = {"path": relative, "expected_slides": count, "status": "fail"}
            result["errors"].append({"kind": "presentation_unreadable", "source": relative, "reason": str(exc)})
        result["presentations"].append(entry)
    if result["errors"]:
        result["status"] = "fail"
    return result


def main():
    parser = argparse.ArgumentParser(description="离线检查交付链接、4A SVG、3 套 PPTX 页数及每页备注。")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="项目或解压后的培训包目录；默认由脚本位置定位")
    parser.add_argument("--output", type=Path, help="JSON 结果；默认写入项目 evidence/delivery-check.json")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        parser.error("--root 必须是现有项目目录。")
    output = args.output.expanduser().resolve() if args.output else root / "evidence" / "delivery-check.json"
    result = run(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = result["documents"]
    print("{}: {} Markdown, {} HTML, {} local links; {} SVG, {} PPTX; {} errors".format(
        result["status"].upper(), summary["markdown"], summary["html"], summary["local_links_checked"],
        len(result["svg"]), len(result["presentations"]), len(result["errors"])))
    for error in result["errors"]:
        print("- {}:{} {} {}".format(error["source"], error.get("line", ""), error["kind"], error.get("target", error.get("reason", ""))))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
