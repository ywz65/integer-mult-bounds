"""Independent small-matrix controls; imports the reviewed guard only."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations, permutations, product
from math import lcm
import hashlib
import importlib.util
import json
import random
import sys

SOURCE = Path(__file__).resolve().parent / 'source/pr2560/guard.py'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != 'a3b8d2fabd57555e7de32f54d3d4389285bfaf788befad09c6e9efe401e8c39d':
    raise ValueError('reviewed PR2560 guard hash changed')
spec = importlib.util.spec_from_file_location('guard_under_review', SOURCE)
G = importlib.util.module_from_spec(spec)
exec(compile(SOURCE.read_bytes(), str(SOURCE), 'exec'), G.__dict__)


def determinant(matrix):
    total = 0
    for order in permutations(range(len(matrix))):
        sign = (-1) ** sum(order[i] > order[j] for i in range(len(order)) for j in range(i + 1, len(order)))
        term = sign
        for i, j in enumerate(order):
            term *= matrix[i][j]
        total += term
    return total


def minors_rank(a, n):
    for size in range(min(len(a), n), 0, -1):
        for rows in combinations(range(len(a)), size):
            for cols in combinations(range(n), size):
                if determinant([[a[i][j] for j in cols] for i in rows]):
                    return size
    return 0


def reference_kernel(a, n):
    a = [[Fraction(x) for x in row] for row in a]
    pivots = []
    row = 0
    for col in range(n):
        selected = next((i for i in range(row, len(a)) if a[i][col]), None)
        if selected is None:
            continue
        a[row], a[selected] = a[selected], a[row]
        div = a[row][col]
        a[row] = [x / div for x in a[row]]
        for i in range(len(a)):
            if i != row:
                div = a[i][col]
                a[i] = [x - div * y for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
    out = []
    for free in set(range(n)) - set(pivots):
        vector = [Fraction(0)] * n
        vector[free] = 1
        for i, pivot in enumerate(pivots):
            vector[pivot] = -a[i][free]
        scale = lcm(*(x.denominator for x in vector))
        out.append([int(x * scale) for x in vector])
    return out


def rejects(callback):
    try:
        callback()
    except ValueError:
        return
    raise RuntimeError('invalid candidate accepted')


def main():
    rng = random.Random(81007)
    cases = [([], n) for n in range(5)]
    cases += [([[], []], 0)]
    cases += [([list(v[:3]), list(v[3:])], 3) for v in product((-1, 0, 1), repeat=6)]
    cases += [([[rng.randrange(-5, 6) for _ in range(n)] for _ in range(m)], n)
              for n in range(1, 5) for m in range(5) for _ in range(8)]
    accepted = omitted = duplicated = 0
    for a, n in cases:
        rank = minors_rank(a, n)
        basis = reference_kernel(a, n)
        if len(basis) != n - rank:
            raise RuntimeError('independent oracle dimension mismatch')
        for _ in (0,):
            certificate = G.certify(a, n, basis)
            accepted += 1
            G.certify(a, n, [[-2 * x for x in row] for row in reversed(basis)])
            if basis:
                rejects(lambda: G.certify(a, n, basis[:-1]))
                omitted += 1
                rejects(lambda: G.certify(a, n, [*basis, basis[0]]))
                duplicated += 1
    original = [[1, 0]]
    def mutator(a, n):
        a[0][0] = 0
        return [[1, 0], [0, 1]]
    rejects(lambda: G.guarded_kernel(mutator)(original, 2))
    if original != [[1, 0]]:
        raise RuntimeError('callback changed original input')
    for a, n, basis in [([[True]], 1, []), ([[1.0]], 1, []), ([[1]], True, []), ([[1, 2]], 1, [])]:
        rejects(lambda: G.certify(a, n, basis))
    rejects(lambda: G.guarded_kernel(reference_kernel)([[Fraction(1, 2)]], 1))
    q = G.PRIMES[0] * G.PRIMES[1]
    fallback = G.certify([[q, 0]], 2, [[0, 1]])
    if fallback['input'] != 'exact':
        raise RuntimeError('input bad-prime fallback not exercised')
    basis_fallback = G.certify([], 2, [[q, q], [q, -q]])
    if basis_fallback['basis'] != 'exact':
        raise RuntimeError('basis bad-prime fallback not exercised')
    print(json.dumps(dict(status='PASS',runtime=sys.version,source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                         matrices=len(cases),valid_certificates=accepted,omitted_rejected=omitted,
                         duplicate_rejected=duplicated,bad_prime_fallback=fallback,
                         argument_mutation_rejected=True,nonintegral_input_rejected=True,basis_fallback=basis_fallback,source_head="6f981dfc414eda4bd17584a0f6d4f1fb3c5d6f04"),indent=2))


if __name__ == '__main__':
    main()
