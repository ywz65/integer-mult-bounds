# Independent full-ledger audit of PR2560's nullspace guard

This is a review artifact for PR2560 at
`6f981dfc414eda4bd17584a0f6d4f1fb3c5d6f04`. The final overlap check found
that its guard had been published during this investigation. A second guard
PR was abandoned. This artifact instead exercises that exact published
`guarded_kernel` across the full inherited key/containment workload, measures
its validation cost and demonstrates the actual caller's omission failure.

PR2560's own evidence covers all 4,473 initializer calls. The new target is
those calls plus all 145,513 post-initialization calls for 86,789 keys and
85,017 targets, followed by all 202,190 ledger containment moves. Its guard,
the faster PR2537 candidate and the actual PR147 frame caller remain byte
unchanged. No production certificate is amended.

## Reproduce and inspect

From the repository root, using standard-library Python 3.12:

```sh
python3 -I -B research/recycled-nullspace-completeness/replay.py --scope full --guard-implementation pr2560 --expect research/recycled-nullspace-completeness/PR2560-FULL-REPLAY.json
python3 -I -O -B research/recycled-nullspace-completeness/test_guard.py
python3 -I -O -B research/recycled-nullspace-completeness/test_sources.py
```

The full replay deliberately rejects `-O`: the unchanged inherited caller
uses assertions. The guard's standalone controls do support `-O`. Sources
are authenticated before import; fresh bytecode-cache namespaces avoid
stale default-path caches. Source files are trusted Python, not sandboxed
hostile code. No dependency installation or network access is required.

`PR2560-FULL-REPLAY.json` is the exact published-guard run. `FULL-REPLAY.json`
is a prior independent-comparator run, using `guard.py`; that implementation
is retained only as an independently developed comparison, not proposed as
another contribution. Both receipts include every mathematical counter,
basis/annihilator map digests and the named caller witness. `--expect`
compares the entire mathematical receipt, excluding environment and timing.
Sorted map entries stabilize iteration order; `-I` ignores inherited
`PYTHONHASHSEED` settings. Outputs named with `--out` must be new files.

The earlier paired 400-move runs, `SAMPLE-UNGUARDED.json` and
`SAMPLE-REPLAY.json`, compare the original fast kernel with the independent
comparator. They have identical basis and annihilator maps, 5,319 calls,
88,992 returned vectors and the same omission witness. They are not
measurements of PR2560. Their callback times are 2.49s unguarded and 7.62s
with the comparator; whole initialization plus basis/containment stages are
140.87s and 163.28s on a shared Windows CPython 3.12.7 host. Workload noise
precludes identifying their wall-time difference solely with guard cost.

## Measured full result

All **149,986 calls** passed the published guard, each through its modular
input-rank witness and diagonal basis minor. All **202,190 containment moves**
passed. The run returned **1,584,540 vectors**. Both complete map digests and
all proof-relevant common fields agree with the independent comparator;
`COMPARISON.json` documents the excluded implementation-route labels.

Published-guard initialization took **134.95s**, basis/target work **155.63s**,
and containment **13.79s**, a **304.37s** stage total. Within those stages,
the fast candidate took **35.61s** and the complete callback **85.39s**;
the additional callback work was **49.78s**, including copying, exact
annihilation, rank/minor checks and observation. Nested times must not be
added to the stage total. These are measurements of one loaded host.

The exact published guard also passed the separate determinant/RREF review:
895 matrices, 814 omitted-basis and 814 duplicate-basis rejections, both
unlucky-prime fallback routes, and mutation/input-domain controls under
native Python3.12.7 with `-I -O -B`. `review_pr2560.py` is a portable copy of
that independent review, with an explicit fixed source hash gate.

## What is independently checked

The rank-nullity argument is standard and credited to the published guard.
[PROOF.md](PROOF.md) records the independent review: exact annihilation and
complementary rational-rank lower bounds force independence and completeness.
A successful modular dimension witness is deterministic; inconclusive primes
use exact fallback. Equivalent signs, scaling and order remain valid.

The concrete containment control chooses an actual target frame and removes
one annihilator row. It constructs a source vector annihilated by the retained
rows but not by the omitted one, then calls unchanged `Exact.inside` with
both caches. The complete basis rejects the false containment, the truncated
basis accepts it, and the published guard rejects the truncated basis. This
is a constructed adversarial source against a genuine target, not a claim
that a valid ledger move was wrong.

The independent comparator's tests cover 185 reference matrices plus
omission, dependence, modular aliasing, exact fallback, malformed inputs,
callback mutation and noninteger dispatch. Separate review uses an independent
RREF basis and determinant-minor ranks; its receipt states the exact candidate
and code hashes. These tests support an implementation; they do not formalize
the inherited verifier or multiplication theorem.

## Provenance, credit and limits

Base: canonical main `0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2`, priority 4.
`SOURCES.json` binds the source's paired-cube input, PR97 manifest and all
manifest files, PR147 frame/word callers, loader and recycled plan.
`PREDECESSORS.json` authenticates retained PR2537 and PR2560 files before
extraction/execution. Only exact `null_exact_ff` and `install_null_kernel`
AST nodes are extracted from PR2537; its main is not executed.

PR2537 by thakrarsagar, with disclosed Claude assistance, supplies the faster
kernel and the explicit missing-vector warning. PR2560 supplies the reviewed
guard, diagonal/minor optimization and initializer admission proof. Douglas
Colkitt's recycled-bit integration and its predecessor lineage remain credited.
PR97 physical-ledger work is by Zhihao Chen and frame/lifted sources by Swapnil
Jain; original notices and `word147.py`'s finer credits remain unchanged.
New independent replay, caller control and review: ywz65 with substantial
OpenAI Codex assistance, Apache-2.0. Separate AI review is not human or
maintainer acceptance.

The full new run covers all ledger containment moves, not fresh-pair
nondegeneracy, scalar identity, pricing, a production installer/certificate
update, all-size transfer or the complete supplier theorem. It changes no
selected exponent and claims no speedup. Source-authenticated reuse of the
predecessor is distinct from independent validation of that predecessor.

## Open next questions

Adopting the guard in the production installer still needs its full `--all`
replay, including nondegeneracy and pricing, with a reviewed certificate-pin
update. Start from the exact guard and candidate pins here. Independently
certified existing ranks might reduce validation cost; first establish their
provenance without trusting the candidate row count. See TASK.json.
