"""Authenticate original inputs and extract exactly credited PR2537 functions."""
import ast,hashlib,importlib.util,json,os,sys
from math import gcd
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def require(ok,message):
    if not ok: raise ValueError(message)

def load():
    for base,name in ((ROOT,'SOURCES.json'),(HERE,'PREDECESSORS.json')):
        for item in json.loads((HERE/name).read_text(encoding='utf-8'))['files']:
            if item.get('usage')=='provenance':continue
            raw=(base/item['path']).read_bytes()
            require(hashlib.sha256(raw).hexdigest()==item['sha256'],'source SHA256 '+item['path'])
            require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==item['git_blob'],'source blob '+item['path'])
    sys.path.insert(0,str(ROOT/'research/bit-reuse-147'))
    sys.path.insert(0,str(ROOT/'references/partial-gauge/pr97'))
    import frames147,linalg,check_lifted,word147
    path=HERE/'source/pr2537/integration_verify.py'
    parsed=ast.parse(path.read_bytes(),filename=str(path))
    names={'null_exact_ff','install_null_kernel'}
    nodes=[n for n in parsed.body if isinstance(n,ast.FunctionDef) and n.name in names]
    require({n.name for n in nodes}==names and len(nodes)==2,'exact credited function extraction')
    ns={'gcd':gcd,'sys':sys,'os':os,'frames147':frames147,'_ORIGINAL':{}}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)
    return ns,frames147,linalg,check_lifted,word147
