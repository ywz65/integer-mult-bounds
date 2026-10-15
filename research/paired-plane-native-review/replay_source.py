"""Replay retained PR2203 commands in a fresh, source-authenticated export.

Only standard-library modules are used. Original source files are never edited.
The profile callback observes generated records; it changes no source callable.
"""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ORIGINAL = 'research/paired-plane-native-payload'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def capture(root, output):
    source = root / ORIGINAL / 'verify.py'
    observed = {}

    def profile(frame, event, arg):
        if event == 'return' and frame.f_code.co_name == 'main' and Path(frame.f_code.co_filename) == source:
            observed['records'] = frame.f_locals['records']
            observed['receipt'] = frame.f_locals['receipt']

    sys.argv = [str(source)]
    sys.setprofile(profile)
    try:
        runpy.run_path(str(source), run_name='__main__')
    finally:
        sys.setprofile(None)
    need(hashlib.sha256(canon(observed['records']).encode()).hexdigest()
         == observed['receipt']['native_recipe_sha256'], 'observed native recipe digest')
    with output.open('x', encoding='utf-8') as stream:
        stream.write(canon(observed))


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def authenticate_export(export):
    records = [(r['path'], r) for r in read(HERE / 'SOURCES.json')['files']
               if r['usage'] == 'input']
    records += [(r['upstream_path'], r) for r in read(HERE / 'PREDECESSORS.json')['records']]
    for path, record in records:
        raw = (export / path).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == record['sha256'], 'export source SHA256')
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        need(blob == record['git_blob'], 'export source Git blob')
    return len(records)


def replay():
    # run_path compiles the current audit source directly; no .pyc selection.
    runpy.run_path(str(HERE / 'audit.py'))['pins']()
    with tempfile.TemporaryDirectory(prefix='paired-plane-source-review-') as directory:
        work = Path(directory)
        export = work / 'export'
        package = export / ORIGINAL
        shutil.copytree(HERE / 'source', package)
        for record in read(HERE / 'SOURCES.json')['files']:
            if record['usage'] != 'input':
                continue
            target = export / record['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / record['path'], target)
        # Authenticate the copied bytes themselves, not just their source paths.
        need(authenticate_export(export) == 11, 'complete executed source inventory')
        before = snapshot(export)
        cache1, cache2 = work / 'cache-primary', work / 'cache-controls'
        cache1.mkdir(); cache2.mkdir()
        captured = work / 'observed.json'
        first = [sys.executable, '-I', '-O', '-B', '-X', 'pycache_prefix=' + str(cache1),
                 str(Path(__file__).resolve()), '--capture-root', str(export), '--capture-output', str(captured)]
        second = [sys.executable, '-I', '-O', '-B', '-X', 'pycache_prefix=' + str(cache2),
                  str(package / 'test_export.py')]
        for command in (first, second):
            subprocess.run(command, cwd=work, check=True, timeout=120)
        need(snapshot(export) == before, 'original source export changed')
        observed = read(captured)
        need(canon(observed['records']) == canon(read(HERE / 'RECIPES.json')), 'complete generated recipes')
        need(canon(observed['receipt']) == canon(read(HERE / 'source/EXPECTED.json')), 'complete source receipt')
    print('PASS_EXACT_SOURCE_REPLAY original_primary original_exports recipes_complete sources_read_only')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--capture-root', type=Path)
    parser.add_argument('--capture-output', type=Path)
    args = parser.parse_args()
    if args.capture_root is not None:
        need(args.capture_output is not None, 'capture output required')
        capture(args.capture_root, args.capture_output)
    else:
        need(args.capture_output is None, 'capture root required')
        replay()
