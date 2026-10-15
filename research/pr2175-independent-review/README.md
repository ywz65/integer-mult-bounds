# Independent execution and proof review of PR2175

The retained community-efficient1200 review at canonical main
`6bd33bc0b87a01e9c9d8b1c01576f3ddbcaee850` leaves PR2175's scoped execution
pending. This artifact supplies a complete clean replay and a separate review
of its proof and census code. Reviewed source:
`1d943bc9e0718c8a2f15e1d0a22b73ad528ef0ca`, Nick Petalas.
No material discrepancy was found in the declared formal model. This does not
change the maintainer disposition or establish a physical supplier.

## Replayed evidence

All nine changed package files and six source/provenance dependencies are
retained as exact Git bytes under `source/`; SOURCE-INVENTORY.json binds SHA-256
and Git blobs. Their line endings are preserved by the local .gitattributes.
No predecessor file is edited or imported from a mutable remote branch.

The source's complete census passed on native Windows CPython 3.12.7 with
`-I -O -B -W error` in 24.486 seconds. Its separately implemented semantic
test suite passed in 3.760 seconds. FRESH.json equals every field of the
original EXPECTED.json, including the complete expansion transcript:

`118ea0c1edc09d94b02e90dce7a6bf6168f917b5d10f78a9d59ef77dd04703a8`.

The census retains 3,600 zero-sum middle sequences, 441 zero-sum outer
sequences, 9,721 profiles, 89,052 A-side and 1,201,320 C-side passes,
68 cross-compatible keys, 152 profile pairs and all 5,536 concrete words.
None passes the complete necessary quotient. All 4,096 group products,
4,913 quotient associativity triples, the full fourteen-call witness,
fourteen omission controls and the wrong-label control pass. The test suite
also covers a separate dense relation oracle, planted reconstruction,
profile joins, arbitrary dirty inputs and source/receipt failure controls.
These are credited checks executed afresh, not new algorithms.

## Separate full group-algebra check

`formal_audit.py` implements the group law using literal dense 4-by-4 binary
matrix multiplication and evaluates full 2-by-2 matrices over F2[UT4(F2)]
with 64-bit coefficient sets. It does not use the producer's group-product,
quotient or formal-endpoint arithmetic. All 5,536 candidate words fail the
full endpoint; every one already differs at block (0,0). The full formal
transcript is
`a2daef16e2489228bf381bbb8096d2ac972769a2a69ba428ec0571f88ca21f1b`.

The original authenticated census supplies the candidate enumeration through
a read-only callback. This is a separate endpoint evaluator, **not an
independent enumeration**. It checks the complete original census record
and rejects duplicate literal candidates. Exact operator equality for the
original fourteen-call upper word covers all 128 active regular-representation
columns; all fourteen
omissions, a wrong label and a noncommuting-order control are discriminating.
The original replay additionally retains its separate dirty identity role.

## Proof review

The mixed-middle factorization XY=0, UY=S, XV=T, UV=H yields the pure-central
rank through ker(X)/im(Y). With each same-label row and column span containing
the active target plane, this proves n_b >= 2d+k. At thirteen calls the
outer counts and middle quotient force all six scalar spans to equal the
two active roles. Thus arbitrary restored dirty workspace cannot rescue the
(4,5,4) split; this implication is written mathematics, not extrapolation
from a small dirty fixture.

A separate OpenAI Codex agent reviewed that argument, the necessary side
and cross screens, all gap/interleaving coverage, and the final quotient
exclusion. Its no-import sanity script independently rebuilt the nine
rank-one couplings, all zero-sum sequences and all 55,566 concrete outer
placements, the four-matrix relaxation and the literal upper words. Exact
evidence and limits are in REVIEW-C.md and REVIEW-independent-C.json.
No human or proof-kernel review is claimed.

## Reproduce

Set P to this artifact directory and use Python 3.12 with a writable temporary
directory. These commands are read-only:

```sh
python3.12 -I -O -B -W error $P/source/research/ut4-mixed-central-middle/verify.py
python3.12 -I -O -B -W error $P/source/research/ut4-mixed-central-middle/test_package.py
python3.12 -I -O -B $P/formal_audit.py
python3.12 -I -O -B $P/independent_domain_audit.py
```

The formal audit authenticates all fifteen original files before compiling
the captured producer source bytes. Its default compares every retained
FORMAL-AUDIT field; `--output NEW_PATH` exclusively creates a fresh report.
Fresh full census generation can use the original `--emit NEW_PATH`; compare
decoded JSON to EXPECTED.json so platform line endings are immaterial.
Raw hashes remain mandatory for the unchanged source inputs.
Timings are local observations, not a performance improvement claim.

## Scope, provenance and stopping decision

The theorem reviewed is unit-price minimum fourteen for diag([z],[uz],I)
over every finite number of dirty roles, in the specified full formal
rank-one a,b,c alphabet. Both nilpotent and idempotent couplings are allowed;
free scalar GL mixing is normalized by augmentation. Free address maps,
clean storage, COPY/ERASE and higher-rank calls are excluded.
Weighted extensions in PR2314/2323 are separate claims. Native letters,
physical movement/hosting, rational frames, precision, all-size compilation,
supplier admission and selected-frontier improvements remain unproved here.

Root round086 drew bit-new-register-model, nonce
`2e7f3c924dfb40eb7ba6574480deb346`, priority5. The baseline bindings passed.
The refined task closes an explicit existing execution/proof-review gap,
rather than proposing another register search. The boundary and formal call
bill are reviewed; the physical costs are unknown, not zero. Decision: finish
this bounded review and stop. No family expansion follows.

Open next step: maintainer assessment of this exact head and these receipts.
The existing weighted and physical handoffs require their own source-bound
reviews; they are not answered by this unit-price audit.

Credit Nick Petalas/PR2175, Gareth Davidson/PR2027, ToikY/PR1662 and PR1680,
Aaron Wang/PR1690, steph4n-gh/PR1573, Arham Tahir/PR1589 and Hanson Sun/PR1607.
Their original proofs, code, notices and claims are retained unchanged.
New independent execution, endpoint evaluator and review by ywz65 with
substantial OpenAI Codex assistance. Apache-2.0.
