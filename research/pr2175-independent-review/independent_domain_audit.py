"""Independent bounded review; imports no producer executable."""
import argparse,hashlib,itertools,json,sys
from pathlib import Path
D=Path(__file__).resolve().parent;S=D/'source'
def need(x,label):
    if not x:raise ValueError(label)
def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col))%2 for col in zip(*b)] for row in a]
def rank(matrix):
    rows=[sum(v<<i for i,v in enumerate(row)) for row in matrix];pivots={}
    for x in rows:
        while x:
            bit=x.bit_length()-1
            if bit in pivots:x^=pivots[bit]
            else:pivots[bit]=x;break
    return len(pivots)
X=[[1,1,1,0,1],[0,0,0,1,1]];Y=[[1,0],[1,0],[0,1],[0,1],[0,1]]
U=[[0,0,1,1,0],[0,0,0,0,1]];V=[[1,0],[0,0],[1,1],[0,1],[0,1]]
products={'XY':mm(X,Y),'UY':mm(U,Y),'XV':mm(X,V),'UV':mm(U,V)}
need(products=={'XY':[[0,0],[0,0]],'UY':[[0,0],[0,1]],'XV':[[0,0],[0,0]],'UV':[[1,0],[0,1]]},'four-matrix fixture')
need(rank(X)==rank(Y)==2,'both middle ranks')
need(all(any(c) for c in zip(*X)) and all(any(r) for r in Y),'all nonzero factorizations')
bad=[r[:] for r in V];bad[0][0]^=1;need(mm(X,bad)!=products['XV'],'V mutation')
# Independent outer-domain construction: choose A positions among the nine
# events, then read the cumulative matrix at each B, instead of assigning gaps.
matrices=[n for n in range(1,16) if rank([[(n>>(2*i+j))&1 for j in range(2)] for i in range(2)])==1]
need(len(matrices)==9,'complete nonzero binary rank-one alphabet')
def xor(items):
    s=0
    for x in items:s^=x
    return s
zero4=[word for word in itertools.product(matrices,repeat=4) if xor(word)==0]
zero5=sum(xor(word)==0 for word in itertools.product(matrices,repeat=5))
positions=list(itertools.combinations(range(9),4));profiles=set();realizations=0
for word in zero4:
    for places in positions:
        assigned=dict(zip(places,word));current=0;profile=[]
        for slot in range(9):
            if slot in assigned:current^=assigned[slot]
            else:profile.append(current)
        need(current==0 and len(profile)==5,'zero outer profile')
        profiles.add(tuple(profile));realizations+=1
expected=json.loads((S/'research/ut4-mixed-central-middle/EXPECTED.json').read_text())
need(len(zero4)==expected['census']['outer_zero_sequences'],'outer domain')
need(zero5==expected['census']['middles']==3600,'middle domain')
need(len(positions)==126 and len(profiles)==expected['census']['profiles']==9721,'profiles')
# Literal 4x4 matrices, independent of the producer six-bit group law.
identity=[[int(i==j) for j in range(4)] for i in range(4)]
letters={}
for k,letter in enumerate('abc'):
    a=[r[:] for r in identity];a[k][k+1]=1;letters[letter]=a
attaining={}
for word,coordinates in [('abcbabcb',[(0,3)]),('acbabc',[(0,2),(0,3)])]:
    a=[r[:] for r in identity]
    for g in word:a=mm(a,letters[g])
    target=[r[:] for r in identity]
    for i,j in coordinates:target[i][j]=1
    need(a==target,'literal upper word '+word);attaining[word]=a
pins=json.loads((D/'SOURCE-INVENTORY.json').read_text());hashes={}
for path,record in pins['files'].items():
    raw=(S/path).read_bytes();h=hashlib.sha256(raw).hexdigest()
    need(h==record['sha256'],'source SHA '+path)
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==record['git_blob'],'source blob '+path)
    hashes[path]=h
result={'status':'PASS_BOUNDED_INDEPENDENT_REVIEW','source_head':pins['head'],'python':sys.version,'four_matrix_products':products,'middle_ranks':[rank(X),rank(Y)],'quotient_dimension':5-rank(X)-rank(Y),
        'domains':{'rank_one_matrices':len(matrices),'outer_zero_sequences':len(zero4),'middle_zero_sequences':zero5,'outer_placements':len(positions),'outer_realizations':realizations,'distinct_profiles':len(profiles)},
        'literal_upper_words':attaining,'source_sha256':hashes,'findings':[],
        'limits':'No producer executable imported. This bounded corroboration does not repeat the 5536-word census; root owns its complete rerun and formal follow-up. Arbitrary-workspace exclusion comes from the separately read quotient/rank/compression proof.'}
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
if args.output:
    with args.output.open('x',encoding='utf-8') as f:f.write(json.dumps(result,indent=2)+'\n')
else:
    saved=json.loads((D/'REVIEW-independent-C.json').read_text())
    need({k:v for k,v in result.items() if k!='python'}=={k:v for k,v in saved.items() if k!='python'},'retained independent review (only Python version excluded)')
print(json.dumps({'status':result['status'],'domains':result['domains'],'source_files':len(hashes)}))
