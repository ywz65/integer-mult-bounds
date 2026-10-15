"""Compare complete fresh PR1392 receipts, excluding only runtime metadata."""
import argparse,copy,hashlib,json
from fractions import Fraction
from pathlib import Path
D=Path(__file__).resolve().parent; S=D/'source/research/pr1048-complete-feasibility'; F=D/'fresh'
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def single_math(x):
 return {k:v for k,v in x.items() if k not in ('elapsed','engine','endpoint_residuals','profile_deltas')}
def classes(rows,single=False):
 return [(r['delta'],r['occurrences'],r['status']) if single else (r['delta'],r['priced_classes'],r['price']['status']) for r in rows]
def inside(outer,inner):
 a,b=map(Fraction,outer);c,d=map(Fraction,inner);return a<=c<=d<=b
def compare_pair(p,i):
 need(p['status']==i['status']=='COMPLETE' and p['complete_domain'] is True and i['complete_domain'] is True,'complete pairs')
 need(p['requested_pairs']==i['requested_pairs']==59998,'pair domain')
 need(p['candidate_digest']==i['candidate_digest']=='b39d6d23210ab7eee24c04e165b078e39ea00053e4be4b523f7c793e24b79679','full candidate transcript')
 need(p['totals']==i['totals'],'all pair totals')
 need(p['totals']['ordered_pairs']==59998 and p['totals']['first_states']==327963 and p['totals']['priced_second_classes']==1379084,'complete pair counts')
 need(not p['witnesses_requiring_full_lift_and_independent_check'] and not i['witnesses_requiring_full_lift_and_independent_check'],'no unresolved witness')
 need(classes(p['delta_classes'])==classes(i['delta_classes']),'all pair classifications/frequencies')
 for a,b in zip(p['delta_classes'],i['delta_classes']):need(inside(a['price']['interval'],b['price']['interval']),'independent pair interval enclosure')
def run(fresh=None,output=None):
 global F
 using_retained = fresh is None
 if fresh is not None:F=Path(fresh)
 names=['primary-singles','independent-singles','primary-pairs','independent-pairs'];fresh={n:load(F/(n+'.json')) for n in names}
 saved={n:load(S/(('complete-pairs' if n=='primary-pairs' else 'independent-complete-pairs' if n=='independent-pairs' else n)+'.json')) for n in names}
 p,i=fresh['primary-singles'],fresh['independent-singles'];need(single_math(p)==single_math(i),'complete single domains')
 need(classes(p['profile_deltas'],True)==classes(i['profile_deltas'],True),'all single classifications/frequencies')
 for a,b in zip(p['profile_deltas'],i['profile_deltas']):need(inside(a['interval'],b['interval']),'independent single interval enclosure')
 for n in names[:2]:
  a,b=dict(fresh[n]),dict(saved[n]);a.pop('elapsed');b.pop('elapsed');need(a==b,'saved single exact math '+n)
 for n in names[2:]:
  a,b=dict(fresh[n]),dict(saved[n]);a.pop('timing');b.pop('timing');need(a==b,'saved pair exact math '+n)
 compare_pair(fresh['primary-pairs'],fresh['independent-pairs'])
 # Sensitivity to false completeness, transcript truncation, lost cases and
 # a misclassified negative-price class. Disposable data only, no source edit.
 rejected=[]
 for name,mutate in [('incomplete',lambda x:x.update(complete_domain=False)),('transcript',lambda x:x.update(candidate_digest='0'*64)),('count',lambda x:x['totals'].update(priced_second_classes=1379083)),('classification',lambda x:x['delta_classes'][1]['price'].update(status='BETTER'))]:
  x=copy.deepcopy(fresh['independent-pairs']);mutate(x)
  try:compare_pair(fresh['primary-pairs'],x)
  except ValueError:rejected.append(name)
  else:raise ValueError('tampered receipt accepted '+name)
 inventory=load(D/'SOURCE-INVENTORY.json');pins=load(D/'source/research/pr1048-certified-repair/SOURCE-PINS.json')['inputs']
 for name,record in {**inventory['files'],**pins}.items():need(hashlib.sha256((D/'source'/name).read_bytes()).hexdigest()==record['sha256'],'post-run source integrity '+name)
 result={'status':'PASS_FULL_PR1392_REPLAY_COMPARISON','four_package_files':len(inventory['files']),'mandatory_inputs':len(pins),'single_domains':3064,'single_moves':1452893,'single_ties':1227676,'single_strict_worse':225217,'single_delta_classes':22,'pair_totals':fresh['primary-pairs']['totals'],'pair_delta_classes':93,'candidate_digest':fresh['primary-pairs']['candidate_digest'],'fresh_receipts':{n:hashlib.sha256((F/(n+'.json')).read_bytes()).hexdigest() for n in names},'comparison_exclusions':{'same_engine_singles':['elapsed'],'same_engine_pairs':['timing'],'between_single_engines':['elapsed','engine','endpoint_residuals','profile_deltas intervals (separately checked by enclosure)'],'between_pair_engines':'Different engine metadata; all totals, transcript, classifications and frequencies exact; intervals by enclosure.'},'receipt_controls':rejected,'source_word_sha256':fresh['primary-pairs']['source_word_sha256']}
 result['fresh_receipts']={n:hashlib.sha256((F/(n+'.json')).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for n in names}
 result['fresh_receipt_hash_encoding']='UTF-8 bytes with CRLF normalized to LF; every JSON field, including runtime metadata, retained'
 if using_retained and output is None:
  need(result==load(D/'COMPARISON.json'),'retained comparison receipt')
 if output:
  with Path(output).open('x',encoding='utf-8') as file:file.write(json.dumps(result,indent=2)+'\n')
 print(result['status'])
 return result
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fresh');parser.add_argument('--output');args=parser.parse_args();run(args.fresh,args.output)
