"""Meaningful exported input drift and inherited assertion-mode controls."""
import json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

class SourceControls(unittest.TestCase):
    def test_exported_source_drift_rejects_before_import(self):
        # Export only the declared inputs and loader. A valid import is not
        # available here, so the named hash rejection must precede that path.
        for relative,predecessor in [('research/bit-reuse-147/frames147.py',False),
                                     ('source/pr2537/integration_verify.py',True)]:
            with self.subTest(relative=relative),tempfile.TemporaryDirectory(prefix='null-source-control-') as td:
                root=Path(td);package=root/'research/recycled-nullspace-completeness'
                package.mkdir(parents=True)
                for name in ['source.py','SOURCES.json','PREDECESSORS.json']:
                    shutil.copyfile(HERE/name,package/name)
                for source,manifest,dest in [(ROOT,'SOURCES.json',root),(HERE,'PREDECESSORS.json',package)]:
                    for item in json.loads((HERE/manifest).read_text())['files']:
                        if item.get('usage')=='provenance':continue
                        target=dest/item['path'];target.parent.mkdir(parents=True,exist_ok=True)
                        shutil.copyfile(source/item['path'],target)
                changed=(package if predecessor else root)/relative
                changed.write_bytes(changed.read_bytes()+b'\n# deliberate source drift\n')
                result=subprocess.run([sys.executable,'-I','-O','-B','-c',
                    'import runpy,sys; runpy.run_path(sys.argv[1])["load"]()',str(package/'source.py')],capture_output=True,text=True)
                self.assertNotEqual(result.returncode,0)
                self.assertIn('source SHA256 '+relative,result.stderr)

    def test_inherited_replay_refuses_optimization(self):
        result=subprocess.run([sys.executable,'-I','-O','-B',str(HERE/'replay.py')],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Inherited caller assertions must remain enabled',result.stderr)

if __name__=='__main__':unittest.main()
