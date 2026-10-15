# Independent bounded review of the complete PR1392 audit

Status: PASS within the stated scope. No material proof/code issue found.

Reviewed the exact pair-reduction proof, primary and independent pair drivers,
single driver, their retained legal-move/profile implementations, the retained
pricing proof, and root's current `integer_price_audit.py` and `compare.py`.
Exact SHA256 bindings are in `REVIEW-round085-independent-C.json`. This review
does not substitute for the separately running complete census.

The repeated-occurrence reduction is valid because deleting the repeated mover
restores the unchanged background. The final slot's original catalogue plus
lower-span closure is therefore a legal baseline single option. The fixed
catalogue condition matters: a new frame introduced at the first step is not
automatically added to all later domains. For disjoint movers, neither changes
the other's register frames or COPY snapshot; their crossings commute and the
profile deltas, including the call-count surcharge, add.

For overlapping movers, retaining every operation that touches their support
union preserves each relevant blocker, frame neighbor, A/B boundary and COPY
snapshot. Erased operations commute with both movers. Projected moves lift into
full gaps without changing any register outside the support union. Both
implementations retain all first states, including identity; neither applies
the unsafe first-step touch/profile quotient. Their second-step caching is
valid because only the final profile remains. Cross-section moves preserve the
section of each occurrence and still retain both section boundaries.

The third pricing engine uses standard positive log and exponential series,
not a novel arithmetic algorithm. Its range reduction, directed integer
multiplication/division, negative coefficient endpoint reversal, reciprocal
weight bounds, and exact surcharge are consistent. After 110 log terms the
tail starts at degree 221 and is bounded by
`2/(221*3^221*(1-1/9))`; after exponential degree 80, `2/81!` bounds the tail
on `[0,1]`. Strict endpoint signs establish the reference root bracket, and
the complete bracket is used for signed prices. The omitted-surcharge control
correctly invalidates the upper endpoint. The full-receipt comparator checks
completeness, transcript, domains, classifications, frequencies, counts and
source integrity. Its same-engine comparisons omit only elapsed/timing data.

An independent script importing no candidate executable reconstructed the
literal frozen-word profile and all ordered occurrence categories: 3,064
repeated, 9,325,034 disjoint, and 59,998 overlapping pairs, of which 13,054
cross sections. It authenticated 73 distinct source/input files. Separately,
90-digit Decimal evaluations at the bracket's two ends and midpoint agree
with all 22 single and 93 pair delta classifications and their rational
enclosures. These Decimal checks are numerical corroboration only; the
directed interval certification rests on the reviewed integer algorithm.

The bounded script and root's read-only third arithmetic replay passed under
native CPython 3.12.7 with `-I -O -B`. I did not rerun either expensive pair
census or the full selected supplier. No unrestricted retiming, growing
catalogue, three-move, native/compiler, supplier or new-kappa conclusion follows.
Acceptance of the complete exclusion still requires the complete fresh primary
and independent census outputs and their exact comparison.

Prepared by worker C for ywz65 with substantial OpenAI Codex assistance.
