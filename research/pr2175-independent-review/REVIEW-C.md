# Independent bounded review of PR2175

Reviewed exact source `1d943bc9e0718c8a2f15e1d0a22b73ad528ef0ca`, including
`ut4-mixed-central-middle/PROOF.md`, `verify.py` and the retained mixed-root
proof. No material proof or census-domain defect found.

The four identities `XY=0, UY=S, XV=T, UV=H` preserve chronological matrix
order. The `BAC/BCA` and `ACB/CAB` representatives give the required entire
active-plane column and row spans. Deleting S-supported output coordinates
and restricting input to ker T leaves exactly the pure-central rank k.
The induced map factors through `ker X / im Y`, since XY=0, XV=T and UY=S.
Thus its dimension is at least k and gives the additional middle-call bound.

At thirteen calls the outer counts must be 4 and the middle count 5. The
two-dimensional active plane lies in each same-letter column and row span;
the zero first coefficient bounds the outer rank sums by 4. The mixed-middle
bound gives the same rank-sum ceiling for b. Consequently all six spans equal
that plane, so every coupling already has zero dirty-complement rows and
columns. This justifies restriction to two roles for arbitrary finite dirty
workspace; no clean-role or fixed-workspace assumption is hidden in the census.

The code enumerates all nine nonzero binary rank-one couplings, every
zero-total middle sequence, and every ordered outer sequence/gap placement.
The side formulas retain scalar order; the two terms in BAB equal the ordered
sum over middle pairs. Profile keys preserve all column/row data needed by
ABC and CBA. The parity-key search enumerates every five-bit row satisfying
ABC=I, then checks CBA=I. Grouping retains every profile and every concrete
realization. All A/C interleavings inside each gap are restored before the
complete quotient comparison. These filters are necessary equations, and a
full quotient rejection is used only as an exclusion, never as formal equality.

`review086_C.py` imports no candidate code. It independently checks the four
matrix fixture and ranks, a changed-V rejection, the complete outer/middle
zero-sum domains, all 126 outer placements via event-position selection,
the 9,721 distinct profiles, literal 4-by-4 products of both attaining words,
and every retained source SHA-256/Git blob. The receipt records its results.
This does not duplicate the full census, which root reruns separately.

The theorem is an exact unit-price minimum for the stated formal UT4 alphabet
and full restored boundary, supported by the finite quotient/census premises.
It does not establish a weighted tariff, physical/native letters, address-size
faithfulness, arbitrary changed alphabets, a supplier or a new exponent.
Written/code review and exact bounded checks are not human or formal-kernel
verification.
