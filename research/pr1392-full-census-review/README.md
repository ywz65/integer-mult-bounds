# Independent complete replay of PR1392

This review supplies the full execution evidence explicitly requested for
[PR1392](https://github.com/CrocSwap/integer-mult-bounds/pull/1392) by the
retained `community-efficient500-review.md`, and still identified as open in
[PR2645](https://github.com/CrocSwap/integer-mult-bounds/pull/2645).
Reviewed head: `bedd71af790bb151590be45599cb5bafe89d9723`.
Review branch starts from canonical main `1884c509efc004524786e9b7cfcc4aca572316d5`.
The clean branch was fast-forwarded to `b5ea56e0a5ac4552166253b1fa4be0753bb38c30`
before packaging; priority5, selected record and the retained PR1392 review
request were unchanged. Historical scientific source pins remain unchanged.
No material discrepancy was found within the declared frozen transport domain.
This is independently executed AI-assisted review, not maintainer integration,
human peer review, a new exclusion theorem or a selected frontier change.

## Complete result

Both exact published implementations were run in full with assertions disabled.
All 3,064 single-operation domain records agree, covering 1,452,893 literal
single transports: 1,227,676 exact ties and 225,217 strictly worse outcomes.
All 59,998 overlapping ordered pairs agree, with 327,963 projected first states
and 1,379,084 final representatives: 1,282,055 ties and 97,029 strictly worse.
There are no improving or unresolved cases. The canonical transcript is
`b39d6d23210ab7eee24c04e165b078e39ea00053e4be4b523f7c793e24b79679`.

Fresh receipts match their corresponding published receipts in every field
except runtime metadata (`elapsed` for singles, `timing` for pairs). The
cross-implementation comparison checks every domain digest, frequency, status,
aggregate and transcript; the independent price intervals are enclosed by the
primary intervals. COMPARISON.json lists the exact exclusions and source pins.
Four disposable receipt corruptions (incomplete status, transcript, count and
classification) are rejected.
Fresh-receipt SHA-256 values normalize CRLF to LF before hashing; all JSON
fields, including timing, remain included. The default check also requires
the retained COMPARISON.json to equal the newly computed comparison record.
This avoids platform line-ending changes invalidating the receipt binding.

The complete repaired-invoice driver also passed: baseline root signs,
surcharge-inclusive signed comparisons, bounded post-first-move reconstruction,
and its separate semantic/source corruption controls. All 61 files in the four
changed packages and all 36 mandatory dependencies are authenticated before and
after the replay. `source/` retains exact Git bytes, including original licenses,
notices, historical claims and receipts; their authorship is unchanged.

## Third arithmetic check

`integer_price_audit.py` imports no predecessor executable. It uses directed
integer intervals at scale 2^256, 110 positive atanh terms after range reduction,
and an exponential Taylor polynomial of degree 80. These are standard bounding
methods, not a novel arithmetic algorithm. Its interval for every one of the
22 single and 93 pair delta classes lies inside the producer interval.

It independently reconstructs the full replicated profile including rank-42
idle calls and the count surcharge, and certifies both strict reference-root
endpoint signs. Omitting the surcharge makes the stated upper endpoint fail;
this is a material control. Improvement, worsening and exact-tie controls pass.
The arithmetic check alone does not establish enumeration completeness.

A separate OpenAI Codex reviewer inspected the exact reduction proof and both
enumerators, reconstructed the full source profile and occurrence partition
without importing candidate code, and checked the new interval/comparison
scripts. Its Decimal point checks are corroboration only. The exact bindings
and limitations are retained in REVIEW-round085-independent-C.json and the
accompanying review note.

For n/d in [1,2], t=(n-d)/(n+d) is at most 1/3. After 110 atanh terms the log
tail is at most 18/(8*221*3^221). After degree 80 at 0<=x<=1, the exp tail is
at most 2/81!. Every intervening multiplication and division rounds outwards.
Reciprocal endpoints and negative coefficients reverse their bounds.

## Proof review and limits

The original proof is credited to Brian Ross. Repeated movers reduce to singles
because deleting that occurrence leaves the same background and fixed catalogue.
Disjoint movers preserve each other's frame/COPY/commuting constraints, and their
signed reference-root prices add. For overlapping movers, retaining every gate
touching either support in both sections preserves the relevant itineraries and
all blockers. Projected slots lift through erased commuting gates. Only the final
step merges identical frame/touch contexts; first states remain literal, so
equal first profiles do not discard different continuation neighborhoods.

This reasoning depends on the fixed 636-frame catalogue plus each slot's own
rational lower closure, legal intermediate words, fixed COPY frames, and at most
two within-section commuting transports. It does not cover growing catalogues,
arbitrary subspaces, longer paths, other scalar identities or arbitrary new words.
Native lowering, hosting, precision, all-size transfer and multiplication-theorem
obligations remain inherited. No PR933 domain correspondence is established.

## Reproduce

The retained review checks are read-only and need the Python standard library:

```sh
python3 -I -O -B research/pr1392-full-census-review/compare.py
python3 -I -O -B research/pr1392-full-census-review/integer_price_audit.py
```

For fresh census execution, choose a new writable output directory `$OUT` and
set `$P` to `research/pr1392-full-census-review`. Run the unchanged programs:

```sh
python3 -I -O -B $P/source/research/pr1048-complete-feasibility/singles.py --engine primary --out $OUT/primary-singles.json
python3 -I -O -B $P/source/research/pr1048-complete-feasibility/singles.py --engine independent --out $OUT/independent-singles.json
python3 -I -O -B $P/source/research/pr1048-complete-feasibility/pairs.py --full --time-budget 1800 --output $OUT/primary-pairs.json
python3 -I -O -B $P/source/research/pr1048-complete-feasibility/independent_pairs.py --full --time-budget 1800 --output $OUT/independent-pairs.json
python3 -I -O -B $P/compare.py --fresh $OUT
```

Require COMPLETE, all counts and the transcript; a time-capped INCOMPLETE run
does not pass. The repaired bounded driver additionally needs NumPy:

```sh
python3 -I -O -B $P/source/research/pr1048-certified-repair/run.py --out $OUT/bounded
```

The full censuses ran under native Windows CPython 3.12.7; the bounded driver
ran under CPython 3.14.5 with NumPy 2.3.5. An initial 3.12 bounded attempt stopped
because NumPy was unavailable. EXECUTION.json records successful runs separately.
Wall times are local replay observations, not algorithmic speedup claims.

## Scope decision and open next questions

Priority revision 5, task scalar-to-moment, fixed picker nonce
`e9a4da2b52625af3fb4dd65b290ecdb9`: narrow to the retained review's explicit
acceptance gap. Original inputs, scalar output, frames, COPY state and restoration
contract are unchanged. Complete census and arithmetic evidence are supplied;
physical implementation costs remain unknown, not zero. No family optimization
is justified by reproducing this negative domain. Stop after this review.

The next useful step is maintainer assessment of the original head together
with these reproducible receipts. PR933 correspondence remains a separate
question requiring an explicit mapping of move domains. This review does not
authorize a larger search or replace the retained review disposition.

Credit Brian Ross for PR1392 and its two existing engines and proof; flemhhh for
PR1048, woklerx for PR1182, Ian Libanio for PR933, Douglas Colkitt for the retained
counterexample, and DreamingOfClouds/eumemic and the supplier lineage. New replay,
comparison and third arithmetic check prepared by ywz65 with substantial OpenAI
Codex assistance. Apache-2.0. No human or proof-assistant review is claimed.
