"""Independent full UT4 endpoint check of every retained census candidate.

Candidate enumeration is the authenticated PR2175 implementation. The dense
group law and full group-ring endpoint calculation here share no producer
arithmetic. This is not a second independent enumeration or a native supplier.
"""
import argparse,hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent
P=D/'source/research/ut4-mixed-central-middle'
POSITIONS=((0,1),(1,2),(2,3),(0,2),(1,3),(0,3))
def need(v,m):
 if not v:raise ValueError(m)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def matrix(g):
 a=[[int(i==j) for j in range(4)] for i in range(4)]
 for k,(i,j) in enumerate(POSITIONS):a[i][j]=(g>>k)&1
 return a
MATRICES=[matrix(g) for g in range(64)]
def multiply(g,h):
 a,b=MATRICES[g],MATRICES[h]
 c=[[sum(a[i][k]*b[k][j] for k in range(4))%2 for j in range(4)] for i in range(4)]
 return sum(c[i][j]<<k for k,(i,j) in enumerate(POSITIONS))
TABLE=[[multiply(g,h) for h in range(64)] for g in range(64)]
GENERATORS={'a':1,'b':2,'c':4}
def right(bits,g):
 out=0
 while bits:
  low=bits&-bits;bits^=low;out^=1<<TABLE[low.bit_length()-1][g]
 return out
def endpoint(word):
 state=[[1,0],[0,1]]
 for letter,n in word:
  need(letter in GENERATORS and 0<n<16,'alphabet')
  need(((n&1)*((n>>3)&1))^(((n>>1)&1)*((n>>2)&1))==0,'rank one')
  previous=state;state=[row[:] for row in previous];g=GENERATORS[letter]
  for i in range(2):
   for k in range(2):
    delta=previous[i][k]^right(previous[i][k],g)
    for j in range(2):
     if (n>>(2*k+j))&1:state[i][j]^=delta
 return state
TARGET=[[1<<32,0],[0,1<<40]]
def run():
 inventory=json.loads((D/'SOURCE-INVENTORY.json').read_text())
 buffers={}
 for name,row in inventory['files'].items():
  raw=(D/'source'/name).read_bytes()
  need(hashlib.sha256(raw).hexdigest()==row['sha256'],'source '+name)
  buffers[name]=raw
 source=P/'verify.py';namespace={'__name__':'audited_producer','__file__':str(source)}
 exec(compile(buffers['research/ut4-mixed-central-middle/verify.py'],str(source),'exec',optimize=0),namespace)
 original=namespace['quotient'];transcript=hashlib.sha256();words=set();failures={}
 def audit(word):
  key=canonical(word);need(key not in words,'duplicate literal candidate');words.add(key)
  image=endpoint(word);need(image!=TARGET,'unexpected full formal solution')
  bad=next((f'{i},{j}' for i in range(2) for j in range(2) if image[i][j]!=TARGET[i][j]),None)
  failures[bad]=failures.get(bad,0)+1
  transcript.update(canonical([word,image])+b'\n')
  return original(word)
 namespace['quotient']=audit
 census=namespace['census']()
 need(census==json.loads((D/'FRESH.json').read_text())['census'],'complete census receipt')
 need(len(words)==5536,'all literal candidates')
 upper=[(c,1) for c in 'abcbabcb']+[(c,8) for c in 'acbabc']
 need(endpoint(upper)==TARGET,'full upper word')
 for i in range(14):need(endpoint(upper[:i]+upper[i+1:])!=TARGET,'omitted upper call')
 changed=upper[:];changed[0]=('c',1);need(endpoint(changed)!=TARGET,'wrong upper label')
 need(endpoint([('a',1),('b',1)])!=endpoint([('b',1),('a',1)]),'noncommuting order')
 return {'status':'PASS_FULL_FORMAL_CANDIDATE_AUDIT','source_head':inventory['head'],
  'group_products':4096,'group_table_sha256':hashlib.sha256(canonical(TABLE)).hexdigest(),
  'candidate_words':len(words),'formal_survivors':0,'first_different_block':failures,
  'full_formal_transcript_sha256':transcript.hexdigest(),
  'producer_quotient_transcript_sha256':census['expanded_transcript_sha256'],
  'full_upper_columns':128,'omitted_upper_controls':14,'wrong_label_controls':1,'noncommuting_order_control':True,
  'scope':'Same authenticated candidate enumerator; separate dense group law and full group-ring endpoint arithmetic. No independent completeness or native claim.'}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args();result=run()
 if args.output:
  with args.output.open('x',encoding='utf-8') as f:f.write(json.dumps(result,indent=2)+'\n')
 else:need(result==json.loads((D/'FORMAL-AUDIT.json').read_text()),'retained formal audit')
 print(json.dumps(result))
