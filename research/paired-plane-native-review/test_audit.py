"""Bounded Git-free integrity controls for the independent review artifact."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


class ExportControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix='paired-plane-review-controls-')
        cls.work = Path(cls.tmp.name)
        cls.export = cls.work / 'export'
        cls.package = cls.export / 'research/paired-plane-native-review'
        shutil.copytree(HERE, cls.package, ignore=shutil.ignore_patterns('__pycache__'))
        for item in json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))['files']:
            if item['usage'] != 'input':
                continue
            target = cls.export / item['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / item['path'], target)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_audit(self):
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith('GIT_')}
        return subprocess.run([sys.executable, '-I', '-O', '-B', str(self.package / 'audit.py')],
                              cwd=self.work, env=env, capture_output=True, text=True, timeout=60)

    def snapshot(self):
        return {p.relative_to(self.export).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.export.rglob('*') if p.is_file()}

    def reject_changed(self, path, raw, diagnostic):
        original = path.read_bytes()
        try:
            path.write_bytes(raw)
            before = self.snapshot()
            result = self.run_audit()
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn(diagnostic, result.stderr)
            self.assertEqual(self.snapshot(), before)
        finally:
            path.write_bytes(original)

    def test_git_free_read_only_positive(self):
        self.assertFalse((self.export / '.git').exists())
        before = self.snapshot()
        result = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PASS_INDEPENDENT_PAIRED_PLANE_REVIEW', result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_both_source_namespaces_reject(self):
        paths = [self.package / 'source/verify.py',
                 self.export / 'research/p104-native-channel/vendor/clifford_exact.py']
        for path in paths:
            with self.subTest(source=path.name):
                self.reject_changed(path, path.read_bytes() + b'\n# source drift\n', 'source SHA256')

    def test_recipe_drift_rejects(self):
        path = self.package / 'RECIPES.json'
        value = json.loads(path.read_text(encoding='utf-8'))
        value[0]['recipes']['private_drop']['left']['phase'] ^= 1
        self.reject_changed(path, json.dumps(value).encode(), 'source-generated recipe digest')

    def test_complete_typed_receipt_rejects(self):
        path = self.package / 'RESULT.json'
        value = json.loads(path.read_text(encoding='utf-8'))
        # Python True == 1 is insufficient for a scientific receipt comparison.
        value['peak_owned_private_arrays'] = True
        self.reject_changed(path, json.dumps(value).encode(), 'complete typed review receipt')

    def test_executed_export_is_authenticated(self):
        old_package = self.export / 'research/paired-plane-native-payload'
        shutil.copytree(self.package / 'source', old_package)
        authenticate = runpy.run_path(str(self.package / 'replay_source.py'))['authenticate_export']
        self.assertEqual(authenticate(self.export), 11)
        path = old_package / 'verify.py'
        original = path.read_bytes()
        try:
            path.write_bytes(original + b'\n# copied source drift\n')
            with self.assertRaisesRegex(ValueError, 'export source SHA256'):
                authenticate(self.export)
        finally:
            path.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
