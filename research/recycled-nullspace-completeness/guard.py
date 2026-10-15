"""Certify an integer candidate as a complete rational nullspace basis.

New work by ywz65 with substantial OpenAI Codex assistance, Apache-2.0.
This guard proves span completeness, not canonical row order/sign/scaling.
"""
from fractions import Fraction
from functools import lru_cache
from math import isqrt

PRIME = 2**31 - 1


def require(ok, message):
    if not ok:
        raise ValueError(message)


@lru_cache(None)
def checked_prime(p):
    require(type(p) is int and p >= 2, "rank modulus must be prime")
    require(p == 2 or (p % 2 and all(p % d for d in range(3, isqrt(p) + 1, 2))),
            "rank modulus must be prime")
    return p


def rank_mod(rows, width, p=PRIME):
    """Column-major elimination; the rank is a lower bound on rational rank."""
    p = checked_prime(p)
    matrix = [[x % p for x in row] for row in rows]
    pivot = 0
    for column in range(width):
        selected = next((i for i in range(pivot, len(matrix)) if matrix[i][column]), None)
        if selected is None:
            continue
        matrix[pivot], matrix[selected] = matrix[selected], matrix[pivot]
        row = matrix[pivot]
        reciprocal = pow(row[column], p - 2, p)
        row[column:] = [(x * reciprocal) % p for x in row[column:]]
        for i in range(pivot + 1, len(matrix)):
            factor = matrix[i][column]
            if factor:
                matrix[i][column:] = [(x - factor * y) % p
                                     for x, y in zip(matrix[i][column:], row[column:])]
        pivot += 1
        if pivot == len(matrix):
            break
    return pivot


def rank_exact(rows, width):
    """Independent rational echelon fallback, used only on inconclusive primes."""
    basis = {}
    for original in rows:
        row = [Fraction(x) for x in original]
        for column in sorted(basis):
            factor = row[column]
            if factor:
                row = [x - factor * y for x, y in zip(row, basis[column])]
        column = next((j for j in range(width) if row[j]), None)
        if column is not None:
            factor = row[column]
            basis[column] = [x / factor for x in row]
    return len(basis)


def certify(matrix, width, candidate, *, prime=PRIME):
    """Reject an incomplete/dependent/wrong kernel; never repair candidate rows.

    Inputs must be finite rectangular integer matrices. Empty matrix/candidate
    shapes use the explicit ambient width, including width zero. Returns only
    a small certificate; the caller retains the candidate unchanged.
    """
    require(type(width) is int and width >= 0, "invalid ambient width")
    a = [list(row) for row in matrix]
    n = [list(row) for row in candidate]
    require(all(len(row) == width and all(type(x) is int for x in row) for row in a),
            "input is not a rectangular integer matrix")
    require(all(len(row) == width and all(type(x) is int for x in row) for row in n),
            "candidate is not a rectangular integer matrix")
    require(len(n) <= width, "too many candidate basis rows")
    require(all(sum(x * y for x, y in zip(row, vector)) == 0 for row in a for vector in n),
            "candidate does not annihilate the exact input")
    ra, rn = rank_mod(a, width, prime), rank_mod(n, width, prime)
    mode = "modular-dimension-certificate"
    if rn != len(n) or ra + rn != width:
        ra, rn = rank_exact(a, width), rank_exact(n, width)
        mode = "exact-rank-fallback"
    require(rn == len(n), "candidate basis is dependent")
    require(ra + rn == width, "candidate basis is incomplete")
    return {"input_rank": ra, "nullity": rn, "ambient_width": width,
            "mode": mode, "prime": prime}


def wrap(integer_kernel, reference_kernel, *, observer=None, prime=PRIME):
    """Guard the integer fast path; retain the caller's noninteger fallback.

    A private copy goes to the optimized callback. Certification uses the
    original materialized values even if that callback mutates its argument.
    No global module patching or import-time installation occurs here.
    """
    def guarded(matrix, width):
        original = [list(row) for row in matrix]
        integral = type(width) is int and width >= 0 and all(
            len(row) == width and all(type(x) is int for x in row) for row in original)
        if not integral:
            return reference_kernel(original, width)
        output = [list(row) for row in integer_kernel([row[:] for row in original], width)]
        certificate = certify(original, width, output, prime=prime)
        if observer is not None:
            observer(certificate)
        return output
    return guarded
