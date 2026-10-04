#!/usr/bin/env python3
"""Build and verify the portable training package using the standard library."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'harness-ai-coding-training-v1.1'
DIRECTORIES = ('demo', 'docs', 'evidence', 'faq', 'scripts', 'templates', 'training')
ROOT_FILES = ('.gitignore', 'AGENTS.md', 'README.md', 'START_HERE.html', 'STATUS.md',
              '学习手册.html', '参考解析.html', '讲师手册.html')
OMIT = {'.git', '.DS_Store', '__pycache__', 'node_modules', '.venv', 'dist'}
EXTENSIONS = {'.md', '.html', '.py', '.js', '.mjs', '.css', '.json', '.svg', '.png', '.pptx', '.txt'}


def selected_files():
    files = [ROOT / name for name in ROOT_FILES]
    for folder in DIRECTORIES:
        for path in (ROOT / folder).rglob('*'):
            relative = path.relative_to(ROOT)
            if (path.is_file() and not path.is_symlink()
                    and not any(part in OMIT for part in relative.parts)
                    and relative.parts[:3] != ('evidence', 'slides', 'build')
                    and path.suffix.lower() in EXTENSIONS):
                files.append(path)
    return sorted(set(files))


def main():
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_delivery.py')], check=True, cwd=ROOT)
    files = selected_files()
    manifest = {
        'version': '1.1',
        'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'description': 'Self-study material with practice, reference answers and a verified local example; real learning outcomes pending.',
        'files': [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                   'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
    }
    output_dir = ROOT / 'dist'
    output_dir.mkdir(exist_ok=True)
    output = output_dir / (NAME + '.zip')
    with ZipFile(output, 'w', ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, NAME + '/' + path.relative_to(ROOT).as_posix())
        archive.writestr(NAME + '/MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    with tempfile.TemporaryDirectory(prefix='harness-package-check-') as scratch:
        with ZipFile(output) as archive:
            if archive.testzip() is not None:
                raise RuntimeError('ZIP CRC verification failed')
            archive.extractall(scratch)
        extracted = Path(scratch) / NAME
        for item in manifest['files']:
            path = extracted / item['path']
            if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                raise RuntimeError('SHA-256 mismatch: ' + item['path'])
        check = subprocess.run([sys.executable, str(extracted / 'scripts/check_delivery.py')],
                               check=True, cwd=extracted, text=True, capture_output=True)
        report = {'status': 'pass', 'archive': output.relative_to(ROOT).as_posix(),
                  'archive_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
                  'bytes': output.stat().st_size, 'files_with_manifest': len(files) + 1,
                  'checks': ['ZIP CRC', 'all manifest SHA-256 values', 'fresh-directory delivery check'],
                  'extracted_check': check.stdout.strip(),
                  'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
    (output_dir / 'package-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
