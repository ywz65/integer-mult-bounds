"""Opt-in guarded replay of the exact source's frame builder and nesting caller.

Runs the unchanged PR147 caller with the authenticated PR2537 fast functions.
No original module bytes or certificate pins are edited. This is not the full
supplier main(): scalar/price replay is outside this targeted kernel audit.
"""
import argparse
from collections import Counter
import hashlib,importlib.util,json,random,sys,tempfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def require(ok,message):
    if not ok:raise ValueError(message)

def load_local(name):
    p=HERE/(name+'.py');s=importlib.util.spec_from_file_location('guard_'+name,p)
    m=importlib.util.module_from_spec(s);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m

def digest_map(rows):
    stream=hashlib.sha256()
    for key,value in sorted(rows.items(),key=lambda x:str(x[0])):
        stream.update(json.dumps([key,value],separators=(',',':')).encode()+b'\n')
    return stream.hexdigest()

def run(mode,scope,implementation):
    require(not sys.flags.optimize,'Inherited caller assertions must remain enabled; guard tests separately support -O')
    guard=load_local('guard');source=load_local('source')
    ns,frames,la,cl,word147=source.load()
    _,W,_,schedule,record,folder=word147.load_schedule()
    plan=json.loads((ROOT/'research/recycled-bit-integration/plan.json').read_text())
    word=word147.Word(schedule,plan['elim'],plan['retained'],plan['pairs'])
    ledger=word.ledger();all_moves=ledger['moves']
    moves=all_moves if scope=='full' else random.Random(1).sample(sorted(all_moves,key=str),400)
    keys=sorted({a for _,a,b in moves}|{b for _,a,b in moves},key=str)
    targets=sorted({b for _,a,b in moves},key=str)
    ns['install_null_kernel'](folder,'fast')
    reference=ns['_ORIGINAL']['null_exact']
    counters=Counter();timing=Counter()
    def optimized(a,k):
        t=time.perf_counter();out=ns['null_exact_ff'](a,k)
        timing['optimized_kernel_seconds']+=time.perf_counter()-t
        return out
    def observe(certificate):counters[certificate['mode']]+=1
    if mode=='guarded' and implementation=='pr2560':
        # Execute the authenticated, unchanged published guard, including its
        # original guarded_kernel adapter. Only observe certificate routes.
        path=HERE/'source/pr2560/guard.py'
        spec=importlib.util.spec_from_file_location('reviewed_guard2560',path)
        reviewed=importlib.util.module_from_spec(spec)
        exec(compile(path.read_bytes(),str(path),'exec'),reviewed.__dict__)
        original_certify=reviewed.certify
        def watched_certify(a,k,n):
            cert=original_certify(a,k,n)
            counters['pr2560-input-'+cert['input']+'-basis-'+cert['basis']]+=1
            return cert
        reviewed.certify=watched_certify
        core=reviewed.guarded_kernel(optimized)
    else:
        core=guard.wrap(optimized,reference,observer=observe) if mode=='guarded' else optimized
    def measured(a,k):
        t=time.perf_counter();out=core(a,k);timing['null_callback_seconds']+=time.perf_counter()-t
        counters['kernel_calls']+=1;counters['returned_vectors']+=len(out)
        return out
    la.null_exact=cl.null_exact=measured
    t=time.perf_counter();exact=frames.Exact(schedule,W,folder)
    timing['initialization_seconds']=time.perf_counter()-t
    counters['initialization_calls']=counters['kernel_calls']
    print('INITIALIZED',mode,scope,json.dumps(dict(counters)),flush=True)
    t=time.perf_counter()
    for i,key in enumerate(keys,1):
        exact.basis(key)
        if i%20000==0:print('BASIS',i,'of',len(keys),flush=True)
    for i,key in enumerate(targets,1):
        b=exact.basis(key)
        if b and len(b)<exact.h:exact.null(key)
        if i%20000==0:print('NULLS',i,'of',len(targets),flush=True)
    timing['basis_and_target_seconds']=time.perf_counter()-t
    t=time.perf_counter()
    require(all(exact.inside(a,b) for _,a,b in moves),'an actual ledger nesting check failed')
    timing['inside_seconds']=time.perf_counter()-t
    mathematical={'mode':mode,'scope':scope,'source_pr':2537,
       'source_head':'222063b96ec1a109a8c9f40e5d615498a737c6dd',
       'ambient_width':exact.h,'moves':len(moves),'all_ledger_moves':len(all_moves),
       'distinct_keys':len(keys),'distinct_targets':len(targets),'counters':dict(counters),
       'basis_sha256':digest_map(exact._basis),'annihilator_sha256':digest_map(exact._null)}
    if implementation=='pr2560':
        mathematical['reviewed_guard']={'pr':2560,'head':'6f981dfc414eda4bd17584a0f6d4f1fb3c5d6f04'}
    if mode=='guarded':
        certified=(sum(v for k,v in counters.items() if k.startswith('pr2560-')) if implementation=='pr2560'
                   else counters['modular-dimension-certificate']+counters['exact-rank-fallback'])
        require(counters['kernel_calls']==certified,
                'an integer source callback was not certified')

    # Named actual caller, actual target frame, constructed adversarial source.
    key=next(k for k in targets if 0<len(exact.basis(k))<exact.h and exact.null(k))
    b=exact.basis(key);complete=exact.null(key);short=complete[:-1]
    witness=next(v for v in ns['null_exact_ff'](short,exact.h)
                 if sum(x*y for x,y in zip(v,complete[-1])))
    probe=('guard_witness',)
    exact._basis[probe]=[witness]
    require(not exact.inside(probe,key),'complete actual-caller kernel failed to separate witness')
    saved=exact._null[key];exact._null[key]=short
    try:require(exact.inside(probe,key),'dropped-vector caller control did not demonstrate gap')
    finally:exact._null[key]=saved;del exact._basis[probe]
    actual_certify=original_certify if mode=='guarded' and implementation=='pr2560' else guard.certify
    try:actual_certify(b,exact.h,short)
    except ValueError as error:
        require('incomplete' in str(error),'wrong omission rejection reason')
        mathematical['caller_control']={'target_key':key,'target_rank':len(b),'dropped_nullity':len(short),
            'source_vector':witness,'omitted_vector':complete[-1],
            'full_basis_inside':False,'dropped_basis_inside':True,'guard_rejection':str(error)}
    else:raise ValueError('guard accepted dropped actual null vector')
    return {'status':'PASS_RECYCLED_NULLSPACE_COMPLETENESS','mathematical':mathematical,
            'environment':{'python':sys.version,'platform':sys.platform},'timing':dict(timing)}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode',choices=('guarded','unguarded'),default='guarded')
    ap.add_argument('--scope',choices=('sample','full'),default='sample')
    ap.add_argument('--guard-implementation',choices=('independent','pr2560'),default='independent')
    ap.add_argument('--out',type=Path);ap.add_argument('--expect',type=Path)
    args=ap.parse_args()
    old_prefix,old_write=sys.pycache_prefix,sys.dont_write_bytecode
    with tempfile.TemporaryDirectory(prefix='null-replay-cache-') as cache:
        sys.pycache_prefix,sys.dont_write_bytecode=cache,True
        try:result=run(args.mode,args.scope,args.guard_implementation)
        finally:sys.pycache_prefix,sys.dont_write_bytecode=old_prefix,old_write
    if args.expect:
        expected=json.loads(args.expect.read_text(encoding='utf-8'))
        require(expected['status']==result['status'] and
                json.dumps(expected['mathematical'],sort_keys=True)==json.dumps(result['mathematical'],sort_keys=True),
                'complete mathematical replay receipt changed')
    if args.out:
        with args.out.open('x',encoding='utf-8',newline='\n') as out:
            json.dump(result,out,indent=2,sort_keys=True);out.write('\n')
    print(result['status'],json.dumps(result,sort_keys=True),flush=True)

if __name__=='__main__':main()
