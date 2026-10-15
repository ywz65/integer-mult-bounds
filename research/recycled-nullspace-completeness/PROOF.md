# Complete rational nullspaces without trusting the candidate generator

Let `A` be an integer matrix with `k` columns, and let the candidate `N`
have `d` integer rows and `k` columns. The required contract is that the rows
of `N` form a basis of `ker_Q(A)`. Canonical signs, scaling and order are not
part of this contract.

The guard first checks `A N^T = 0` over the integers. Thus the row space of
`N` is contained in the rational nullspace, and

`rank_Q(A) + rank_Q(N) <= k`.

For a proven prime `p`, elimination over `F_p` gives ranks `a` and `n`.
Each nonzero modular minor is a nonzero integer minor, so these are lower
bounds on the corresponding rational ranks. If `n = d` and `a + n = k`,
the lower-bound sum and the preceding upper-bound sum coincide. Hence
both ranks are exact, the `d` candidate rows are independent, and their
span has the full nullity. This is a deterministic certificate, not a
probabilistic assumption that a chosen prime is lucky.

If either dimension condition fails, the guard computes both ranks by
independent rational echelon reduction and applies the same independence
and dimension conditions. A bad prime can therefore cause more work but
cannot cause acceptance of an incomplete basis or rejection of a valid
basis. Exact annihilation is essential: for `A=[1,0]`, the false candidate
`[p,1]` has the right modular ranks and annihilates modulo `p`.

The empty matrix uses the explicit ambient width; an empty candidate is
valid exactly when `A` has full column rank. Width zero is allowed. Boolean
entries and noninteger candidates are rejected on this integer path.
The adapter preserves the predecessor's reference dispatch for noninteger
or ragged inputs, without extending this guard's claim to that fallback.

The optimized callback receives a private copy of `A`. Certification uses
the original materialized input, so mutation of the callback argument
cannot substitute a different problem. The candidate is never repaired;
valid row values are returned unchanged. The guard uses explicit
exceptions, so its conditions survive Python `-O`.

## Why the downstream containment check is insufficient

The retained PR147 caller's `Exact.inside(a,b)` tests every row of frame
`a` against the rows of `Exact.null(b)`, after trivial dimension branches.
If one annihilator row is missing, those tests describe a strictly larger
space. Let `n` be the omitted row of an independent annihilator basis and
`N'` the remaining rows. There exists a rational vector `v` annihilated by
`N'` but not by `n`; clearing denominators makes it integer. The caller
then accepts `span(v)` against the shortened basis while rejecting it
against the complete basis. Dimension-only short circuits do not prevent
this when the target has positive rank and the source has rank one.

`replay.py` constructs this control against a named actual target frame,
using the unchanged `Exact.inside` method. The source frame is deliberately
constructed, not an assertion that an actual valid ledger move was wrong.
The full receipt includes the vectors and target key. The guard rejects
the shortened basis with `candidate basis is incomplete` before it can
be consumed. This addresses the explicit missing-vector open question
reported by PR2537; that observation is credited to its author.

## Boundary of the proof

This certifies a rational nullspace basis of the supplied integer matrix.
It does not independently certify the frame construction, rank assertions
elsewhere in PR147, `prim`, nondegeneracy, scalar prices or the complete
supplier theorem. The opt-in replay checks containment for the original
ledger and authenticates every declared source before import; it does not
modify frozen source bytes, update an incumbent certificate, or install a
global change in the main verifier. The source is trusted Python code;
hashes and private input copies are not a hostile-code sandbox.
