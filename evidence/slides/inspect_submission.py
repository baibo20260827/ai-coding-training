"""Validate the authored PPTX package and speaker notes using the standard library."""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main", "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
source = json.loads((ROOT / "training/slides/source/content.json").read_text())
report = {"checked_at": "2026-10-03", "scope": "PPTX structure, notes, editable objects, typography and render presence; no PowerPoint application execution", "decks": []}
for deck in source["decks"]:
    file = ROOT / f'training/slides/{deck["id"]}.pptx'
    items = [deck["cover"], *source["opening"], *deck["slides"]]
    summary = {"id": deck["id"], "file": str(file.relative_to(ROOT)), "sha256": hashlib.sha256(file.read_bytes()).hexdigest(), "slides": []}
    with ZipFile(file) as archive:
        parts = sorted((n for n in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)), key=lambda n: int(re.search(r"slide(\d+)", n)[1]))
        assert len(parts) == deck["expectedCount"]
        for i, part in enumerate(parts, 1):
            xml = ET.fromstring(archive.read(part))
            texts = [t.text or "" for t in xml.findall(".//a:t", NS)]
            note = ET.fromstring(archive.read(f"ppt/notesSlides/notesSlide{i}.xml"))
            note_text = "".join(t.text or "" for t in note.findall(".//a:t", NS))
            assert len(note_text) > 120, (deck["id"], i, "missing notes")
            tables = len(xml.findall(".//a:tbl", NS))
            pictures = len(xml.findall(".//p:pic", NS))
            assert pictures == 0, (deck["id"], i, "unexpected flattened image")
            assert (tables == 1) == (items[i - 1]["kind"] == "table")
            if items[i - 1]["kind"] == "architecture":
                for label in ["BA", "AA", "DA", "TA", "预约记录", "1 对多占用格", "同日每格唯一"]:
                    assert label in texts, (deck["id"], i, label)
                assert len(xml.findall(".//p:cxnSp", NS)) == 8
            sizes = []
            for shape in xml.findall(".//p:sp", NS):
                nv = shape.find("p:nvSpPr/p:cNvPr", NS)
                name = nv.get("name", "") if nv is not None else ""
                if name.startswith("footer-"):
                    continue
                shape_sizes = [int(r.get("sz")) / 100 for r in shape.findall(".//a:rPr", NS) if r.get("sz")]
                if name == "slide-title":
                    assert min(shape_sizes) >= 32
                if shape_sizes:
                    assert min(shape_sizes) >= 17, (deck["id"], i, name, min(shape_sizes))
                    sizes.extend(shape_sizes)
            rendered = ROOT / f'evidence/slides/renders/{deck["id"]}/slide-{i:02d}.png'
            assert rendered.exists() and rendered.stat().st_size > 1000
            summary["slides"].append({"slide": i, "title": items[i-1]["title"], "notes_characters": len(note_text), "native_tables": tables, "native_shapes": len(xml.findall(".//p:sp", NS)), "native_connectors": len(xml.findall(".//p:cxnSp", NS)), "minimum_content_font_pt": min(sizes), "render": str(rendered.relative_to(ROOT))})
    summary["status"] = "pass"
    report["decks"].append(summary)
(ROOT / "evidence/slides/submission-check.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": "pass", "decks": len(report["decks"]), "slides": sum(len(d["slides"]) for d in report["decks"])}, ensure_ascii=False))
