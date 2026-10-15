"""Third arithmetic implementation: directed 256-bit integer intervals only.

Audits PR1392's complete transport receipts without importing its code.
Prepared by ywz65 with substantial OpenAI Codex assistance. Apache-2.0.
"""
import argparse,hashlib,json,math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
D=Path(__file__).resolve().parent; S=D/'source'; SCALE=1<<256
LOW=Fraction(1733427039589844234749,10**24); HIGH=LOW+Fraction(1,10**24)
LAMBDA=Fraction(32*64**2,10**16)
def need(v,m):
 if not v:raise ValueError(m)
def ceildiv(n,d):return -(-n//d)
def interval(q):return q.numerator*SCALE//q.denominator,ceildiv(q.numerator*SCALE,q.denominator)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):
 need(a[0]>=0 and b[0]>=0,'nonnegative interval multiplication')
 return a[0]*b[0]//SCALE,ceildiv(a[1]*b[1],SCALE)
def times(a,n):return (a[0]*n,a[1]*n) if n>=0 else (a[1]*n,a[0]*n)
def divint(a,n):return a[0]//n,ceildiv(a[1],n)
def log_reduced(n,d):
 # n/d in [1,2], t=(n-d)/(n+d) in [0,1/3].
 need(d<=n<=2*d,'log range'); t=interval(Fraction(n-d,n+d)); square=mul(t,t); term=t; total=(0,0)
 for k in range(110):
  total=add(total,divint(term,2*k+1));term=mul(term,square)
 # Tail <=2*(1/3)^221 / (221*(1-1/9)); lower partial sum.
 tail=ceildiv(18*SCALE,8*221*3**221)
 return 2*total[0],2*total[1]+tail
@lru_cache(None)
def log_integer(n):
 need(type(n) is int and n>=1,'positive integer log');k=n.bit_length()-1
 return add(times(log_reduced(2,1),k),log_reduced(n,1<<k))
def exp_positive(x):
 need(0<=x[0]<=x[1]<=SCALE,'exp range');term=(SCALE,SCALE);total=term
 for k in range(1,81):
  term=divint(mul(term,x),k);total=add(total,term)
 # For x<=1, tail after degree80 is <=2/81!.
 return total[0],total[1]+ceildiv(2*SCALE,math.factorial(81))
def positive_power(n,a,b=None):
 if b is None:b=a
 return exp_positive(mul(log_integer(n),(interval(a)[0],interval(b)[1])))
@lru_cache(None)
def weight(r):
 e=positive_power(r,LOW,HIGH)
 return r*SCALE*SCALE//e[1],ceildiv(r*SCALE*SCALE,e[0])
def jprice(delta):
 v=interval(LAMBDA*sum(delta.values()))
 for r,c in delta.items():v=add(v,times(weight(r),c))
 return v
def residual(profile,a,surcharge=True):
 v=(0,0)
 for r,c in profile.items():
  # exp(a*(log64-logr)), bounds subtraction and positive coefficients.
  n,d=log_integer(64),log_integer(r);logratio=(n[0]-d[1],n[1]-d[0])
  if r==64:logratio=(0,0)
  v=add(v,times(exp_positive(mul(logratio,interval(a))),r*c))
 if surcharge:v=add(v,mul(interval(LAMBDA*sum(profile.values())),positive_power(64,a)))
 return v[0]-64*28416*SCALE,v[1]-64*28416*SCALE
def sign(a):return 'POSITIVE' if a[0]>0 else 'NEGATIVE' if a[1]<0 else 'ZERO' if a==(0,0) else 'UNRESOLVED'
def serial(a):return [str(Fraction(x,SCALE)) for x in a]
def main(output=None):
 expected=json.loads((S/'research/bit-profile-pair-audit/EXPECTED.json').read_text());local={int(r):c for r,c in expected['tuned_word']['profile'].items()}
 globalp={int(r):c for r,c in expected['pipeline']['idle_remainder'].items()}
 for r,c in local.items():globalp[r]=globalp.get(r,0)+288*c
 need(sum(r*c for r,c in globalp.items())==1808352,'global mass')
 endpoints=[residual(globalp,a) for a in (LOW,HIGH)]
 need(sign(endpoints[0])=='NEGATIVE' and sign(endpoints[1])=='POSITIVE','strict surcharged reference bracket')
 # Retain the material surcharge control: the unsurcharged endpoint must differ.
 no_surcharge=residual(globalp,HIGH,False);need(sign(no_surcharge)=='NEGATIVE','dropping surcharge must invalidate bracket')
 files=[S/'research/pr1048-complete-feasibility/primary-singles.json',S/'research/pr1048-complete-feasibility/complete-pairs.json']
 records=[]
 for path in files:
  data=json.loads(path.read_text());rows=data.get('profile_deltas',data.get('delta_classes'));total=0;ties=0;worse=0
  for row in rows:
   delta={int(r):c for r,c in row['delta'].items()};need(sum(r*c for r,c in delta.items())==0,'mass-preserving delta')
   need(all(local.get(r,0)+c>=0 for r,c in delta.items()),'nonnegative candidate')
   price=jprice(delta);category=sign(price);need(category==('POSITIVE' if delta else 'ZERO'),'strict delta sign')
   quoted=tuple(map(Fraction,row.get('interval',row.get('price',{}).get('interval'))))
   need(quoted[0]<=Fraction(price[0],SCALE)<=Fraction(price[1],SCALE)<=quoted[1],'third interval enclosed by producer')
   count=row.get('occurrences',row.get('priced_classes'));total+=count
   if delta:worse+=count
   else:ties+=count
  records.append({'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'classes':len(rows),'total':total,'ties':ties,'strictly_worse':worse})
 need([(r['classes'],r['total'],r['ties'],r['strictly_worse']) for r in records]==[(22,1452893,1227676,225217),(93,1379084,1282055,97029)],'complete retained census counts')
 controls={'strict_improvement':sign(jprice({1:-3,3:1})),'strict_worsening':sign(jprice({1:3,3:-1})),'exact_tie':sign(jprice({})),'omitted_surcharge_upper_endpoint':sign(no_surcharge)}
 need(controls=={'strict_improvement':'NEGATIVE','strict_worsening':'POSITIVE','exact_tie':'ZERO','omitted_surcharge_upper_endpoint':'NEGATIVE'},'arithmetic controls')
 result={'status':'PASS_THIRD_INTEGER_PRICE_AUDIT','scale_bits':256,'ln_terms':110,'exp_degree':80,'source_head':'bedd71af790bb151590be45599cb5bafe89d9723','reference_bracket':[str(LOW),str(HIGH)],'global_profile':globalp,'endpoint_intervals':list(map(serial,endpoints)),'records':records,'controls':controls,'limitations':'Checks arithmetic of complete retained receipts; full enumeration is separately rerun by the exact primary and independent programs. No new transport exclusion theorem or supplier admission.'}
 if output:
  with Path(output).open('x',encoding='utf-8') as file:file.write(json.dumps(result,indent=2)+'\n')
 else:
  need(json.loads((D/'INTEGER-PRICE-AUDIT.json').read_text())==json.loads(json.dumps(result)),'retained independent arithmetic receipt')
 print(result['status'])
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output');main(parser.parse_args().output)
