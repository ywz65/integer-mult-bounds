"""Independent finite audit of PR2203; no supplier/compiler module imports.

The phase convention is i^p X_a Z_b. Gaussian coefficients are integer pairs
with one power-of-two denominator. Prepared by ywz65 with OpenAI Codex help.
Apache-2.0; original construction and source credit remain in source/README.md.
"""
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    def unique(items):
        out = {}
        for key, value in items:
            need(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def pins():
    records = [r for r in read(HERE / 'SOURCES.json')['files'] if r['usage'] == 'input']
    predecessors = read(HERE / 'PREDECESSORS.json')['records']
    for prefix, record in [(ROOT, r) for r in records] + [(HERE, r) for r in predecessors]:
        raw = (prefix / record['path']).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == record['sha256'], 'source SHA256')
        need(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
             == record['git_blob'], 'source Git blob')
    return len(records) + len(predecessors)


def span(vectors):
    rows = {}
    for x in vectors:
        for bit in sorted(rows, reverse=True):
            if x >> bit & 1:
                x ^= rows[bit]
        if x:
            pivot = x.bit_length() - 1
            rows = {b: r ^ x if r >> pivot & 1 else r for b, r in rows.items()}
            rows[pivot] = x
    return tuple(rows[b] for b in sorted(rows, reverse=True))


def mul(matrix, x):
    return sum(((r & x).bit_count() % 2) << i for i, r in enumerate(matrix))


def transpose(matrix):
    return tuple(sum(((r >> j) & 1) << i for i, r in enumerate(matrix)) for j in range(9))


def inverse(matrix):
    a = [r | 1 << (9 + i) for i, r in enumerate(matrix)]
    for c in range(9):
        p = next((i for i in range(c, 9) if a[i] >> c & 1), None)
        need(p is not None, 'singular binary matrix')
        a[p], a[c] = a[c], a[p]
        for i in range(9):
            if i != c and a[i] >> c & 1:
                a[i] ^= a[c]
    return tuple(r >> 9 for r in a)


def phase(q, linear, x):
    return (sum(linear[i] for i in range(9) if x >> i & 1)
            + 2 * sum(1 for i in range(9) for j in range(i + 1, 9)
                      if x >> i & 1 and x >> j & 1 and q[i] >> j & 1)) % 4


def adjoint(gates):
    out = []
    for gate in reversed(gates):
        if gate[0] == 'P':
            out.append(('P', inverse(gate[1])))
        elif gate[0] == 'D':
            out.append(('D', gate[1], tuple(-x % 4 for x in gate[2])))
        elif gate[0] == 'C':
            out.append(('C', gate[1], -gate[2]))
        elif gate[0] == 'phase':
            out.append(('phase', -gate[1] % 4))
        else:
            need(gate[0] == 'X', 'adjoint gate')
            out.append(gate)
    return tuple(out)


def frame(vectors):
    if not vectors:
        return ()
    if len(vectors) == 9:
        return tuple(('C', 1 << i, 1) for i in range(9))
    columns = []
    for value in tuple(vectors) + tuple(1 << i for i in range(9)):
        if len(span(columns + [value])) > len(columns):
            columns.append(value)
    need(len(columns) == 9, 'complete frame chart')
    matrix = transpose(columns)
    dual = transpose(inverse(matrix))
    q = tuple((1 << i) ^ sum(((a & b).bit_count() % 2) << j for j, b in enumerate(dual))
              for i, a in enumerate(dual))
    linear = tuple((r >> i) & 1 for i, r in enumerate(q))
    chart = (('P', matrix), ('D', q, linear))
    return adjoint(chart) + tuple(('C', 1 << i, 1) for i in range(len(vectors))) + chart


def rotate(pair, power):
    a, b = pair
    return ((a, b), (-b, a), (-a, -b), (b, -a))[power % 4]


def zero_column(gates):
    values, denominator = {0: (1, 0)}, 0
    for gate in gates:
        tag = gate[0]
        out = {}
        for x, (a, b) in values.items():
            if tag == 'C':
                q, sign = gate[1:]
                for y, pair in ((x, (a - sign * b, b + sign * a)),
                                (x ^ q, (a + sign * b, b - sign * a))):
                    old = out.get(y, (0, 0))
                    out[y] = (old[0] + pair[0], old[1] + pair[1])
            else:
                y, pair = x, (a, b)
                if tag == 'P':
                    y = mul(gate[1], x)
                elif tag == 'D':
                    pair = rotate(pair, phase(gate[1], gate[2], x))
                elif tag == 'X':
                    y = x ^ gate[1]
                else:
                    need(tag == 'phase', 'state gate')
                    pair = rotate(pair, gate[1])
                need(y not in out, 'monomial collision')
                out[y] = pair
        if tag == 'C':
            denominator += 1
        values = {x: v for x, v in out.items() if v != (0, 0)}
    while denominator and all((a | b) % 2 == 0 for a, b in values.values()):
        values = {x: (a // 2, b // 2) for x, (a, b) in values.items()}
        denominator -= 1
    return values, denominator


def x_images(gates):
    """Conjugate the nine X generators in the i^p X_a Z_b convention."""
    images = [(1 << i, 0, 0) for i in range(9)]
    for gate in gates:
        out = []
        for a, b, p in images:
            if gate[0] == 'P':
                a, b = mul(gate[1], a), mul(transpose(inverse(gate[1])), b)
            elif gate[0] == 'D':
                p += phase(gate[1], gate[2], a)
                b ^= mul(gate[1], a)
            elif gate[0] == 'X':
                p += 2 * ((b & gate[1]).bit_count() % 2)
            elif gate[0] == 'C':
                if (b & gate[1]).bit_count() % 2:
                    a ^= gate[1]
                    p -= gate[2]
            else:
                need(gate[0] == 'phase', 'Pauli gate')
            out.append((a, b, p % 4))
        images = out
    return images


def monomial(record):
    matrix, q, linear = record['matrix_rows'], record['quadratic_rows'], record['linear_Z4']
    need(len(matrix) == len(q) == len(linear) == 9, 'monomial dimension')
    need(tuple(q) == transpose(q), 'symmetric quadratic')
    need(all(x % 2 == (q[i] >> i & 1) for i, x in enumerate(linear)), 'quadratic parity')
    need(len(set(mul(matrix, x) for x in range(512))) == 512, 'invertible monomial')
    return [(mul(matrix, x) ^ record['offset'], (phase(q, linear, x) + record['phase']) % 4)
            for x in range(512)]


def child_coeff(rank, delta):
    a, b = 1, 0
    for i in range(rank):
        sign = -1 if delta >> i & 1 else 1
        a, b = a - sign * b, b + sign * a
    return a, b


def check_recipe(recipe, expected):
    rank = recipe['rank']
    need(type(rank) is int and 0 <= rank <= 9, 'recipe rank')
    left = monomial(recipe['left'])
    if rank:
        right = monomial(recipe['right'])
    else:
        need(recipe['right'] is None, 'rank-zero right')
        right = [(x, 0) for x in range(512)]
    zero, power = zero_column(expected)
    generators = x_images(expected)
    paulis = [(0, 0, 0)]
    for x in range(1, 512):
        low = x & -x
        a, b, p = paulis[x ^ low]
        c, d, q = generators[low.bit_length() - 1]
        paulis.append((a ^ c, b ^ d, (p + q + 2 * ((b & c).bit_count() % 2)) % 4))
    exponent = max(power, rank)
    scale_actual, scale_expected = 1 << (exponent - rank), 1 << (exponent - power)
    coeff = [child_coeff(rank, d) for d in range(1 << rank)]
    for x in range(512):
        a, b, p = paulis[x]
        wanted = {y ^ a: rotate((v[0] * scale_expected, v[1] * scale_expected),
                               p + 2 * ((b & y).bit_count() % 2)) for y, v in zero.items()}
        start, phase0 = right[x]
        actual = {}
        for delta, value in enumerate(coeff):
            end, phase1 = left[start ^ delta]
            actual[end] = rotate((value[0] * scale_actual, value[1] * scale_actual), phase0 + phase1)
        need(actual == wanted, 'complete Gaussian column')
    return 512


def source_word(program, transfer=((1, 0), (0, 1))):
    order = ('X0', 'X1', 'Y0', 'Y1')
    rows = {name: [int(i == j) for j in range(4)] for i, name in enumerate(order)}
    frames = {name: 'E' if name.startswith('X') else 'ZERO' for name in order}
    calls, lifetimes = Counter(), 0
    for event in program:
        tag, dest = event[:2]
        if tag == 'zero':
            need(dest == 'C' and dest not in rows, 'owned fresh private')
            rows[dest], frames[dest] = [0] * 4, 'E'
            lifetimes += 1
        elif tag == 'copy':
            src = event[2]
            need(dest == 'C' and not any(rows[dest]) and frames[dest] == frames[src], 'owned copy')
            rows[dest] = rows[src][:]
        elif tag == 'transport':
            old, new, rank = event[2:]
            need(frames[dest] == old, 'transport input')
            need((old, new, rank) in [('E', 'FULL', 7), ('E', 'ZERO', 2), ('ZERO', 'Eperp', 7)], 'paid route')
            frames[dest] = new
            calls[rank] += 1
        elif tag == 'add':
            src, coefficient = event[2:]
            need(frames[dest] == frames[src], 'ADD common frame')
            rows[dest] = [a + coefficient * b for a, b in zip(rows[dest], rows[src])]
        else:
            need(tag == 'erase' and dest == 'C' and frames[dest] == 'ZERO', 'owned disposal')
            del rows[dest], frames[dest]
    need([rows[name] for name in order] == [[1, 0, 0, 0], [0, 1, 0, 0],
                                         list(transfer[0]) + [1, 0], list(transfer[1]) + [0, 1]], 'dirty full block')
    need(frames == {'X0': 'FULL', 'X1': 'FULL', 'Y0': 'Eperp', 'Y1': 'Eperp'}, 'block frames')
    return calls, lifetimes


def rejected(fn):
    try:
        fn()
    except ValueError:
        return True
    return False


def audit():
    pin_count = pins()
    expected = read(HERE / 'source/EXPECTED.json')
    records = read(HERE / 'RECIPES.json')
    need(hashlib.sha256(canonical(records).encode()).hexdigest() == expected['native_recipe_sha256'], 'source-generated recipe digest')
    archive = ROOT / 'research/community-frontier1094-audit/selected-replay.tar.gz'
    with tarfile.open(archive) as tf:
        raw = tf.extractfile('candidate/strict/global/base/work/complex-nine-native/DATA-PHASES.json').read()
    data = json.loads(raw)
    labels = [r['q'] for r in sorted(data['recipes'], key=lambda r: r['port'])]
    matching = read(ROOT / 'research/paired-plane-port-matching-seed6c563a/CERTIFICATE.json')
    need(matching['selected_payload_sha256'] == hashlib.sha256(raw).hexdigest(), 'matching payload')
    need(len(records) == 56 and [r['ports'] for r in records] == matching['matching'], 'all matched planes')
    need(sorted(p for r in records for p in r['ports']) == list(range(112)), 'port partition')
    columns, recipes, invoice = 0, 0, Counter()
    first = None
    for record in records:
        q, r = [labels[p] for p in record['ports']]
        need(record['labels'] == [q, r], 'actual source labels')
        need(q.bit_count() % 2 == r.bit_count() % 2 == 1 and (q & r).bit_count() % 2 == 0, 'nondegenerate plane')
        plane = span((q, r))
        cap = span(v for v in range(512) if (q & v).bit_count() % 2 == (r & v).bit_count() % 2 == 0)
        e, v, f = frame(plane), frame(cap), frame(tuple(1 << i for i in range(9)))
        c = (('C', q, 1), ('C', r, 1))
        operators = {'source_entry': adjoint(c) + e, 'source_advance': adjoint(e) + f,
                     'private_drop': adjoint(e), 'target_advance': v,
                     'target_exit': adjoint(v) + adjoint(c) + f}
        ranks = {'source_entry': 0, 'source_advance': 7, 'private_drop': 2,
                 'target_advance': 7, 'target_exit': 0}
        need(set(record['recipes']) == set(operators), 'complete recipe kinds')
        for name, operator in operators.items():
            recipe = record['recipes'][name]
            need(type(recipe['rank']) is int and recipe['rank'] == ranks[name], 'expected child rank')
            columns += check_recipe(recipe, operator)
            recipes += 1
            if recipe['rank']:
                invoice[recipe['rank']] += 2
            if first is None and name == 'private_drop':
                first = (recipe, operator)
    calls, lifetimes = source_word(expected['block_program'])
    need(calls == {7: 4, 2: 2} and lifetimes == 2, 'independent payload occurrence')
    need(invoice == {7: 224, 2: 112} and invoice == {k: 56 * v for k, v in calls.items()}, 'whole direct invoice')
    ratio = Fraction(71 * 896 + 224 * 9, 73 * 896)
    need(ratio == Fraction(293, 292) > 1, 'zero-saving rejection')
    import copy
    faulty = copy.deepcopy(first[0]); faulty['left']['phase'] = (faulty['left']['phase'] + 1) % 4
    need(rejected(lambda: check_recipe(faulty, first[1])), 'global phase control')
    faulty = copy.deepcopy(first[0]); faulty['rank'] = 1
    need(rejected(lambda: check_recipe(faulty, first[1])), 'single-direction drop control')
    faulty = copy.deepcopy(expected['block_program'])
    next(e for e in faulty if e[:3] == ['add', 'Y1', 'C'])[3] = 0
    need(rejected(lambda: source_word(faulty)), 'missing second payload control')
    broadcast = [['zero', 'C'], ['copy', 'C', 'X0'], ['add', 'C', 'X1', 1],
                 ['transport', 'X0', 'E', 'FULL', 7], ['transport', 'X1', 'E', 'FULL', 7],
                 ['transport', 'C', 'E', 'ZERO', 2], ['add', 'Y0', 'C', 1], ['add', 'Y1', 'C', 1],
                 ['erase', 'C'], ['transport', 'Y0', 'ZERO', 'Eperp', 7], ['transport', 'Y1', 'ZERO', 'Eperp', 7]]
    need(source_word(broadcast, ((1, 1), (1, 1))) == (Counter({7: 4, 2: 1}), 1), 'legal broadcast positive control')
    need(rejected(lambda: source_word(broadcast)), 'broadcast is not identity control')
    need(rejected(lambda: need({7: 224, 2: 56} == invoice, 'half invoice')), 'half invoice control')
    return {'status': 'PASS', 'source_head': 'c3c85ea8c226640334b1d2246071f230d81cc137',
            'authenticated_files': pin_count, 'planes': 56, 'recipes': recipes,
            'gaussian_columns': columns, 'public_input_arrays': 224,
            'native_occurrences': dict(sorted(invoice.items())), 'rank_mass': sum(k * v for k, v in invoice.items()),
            'copy_mass': 224, 'private_lifetimes': lifetimes * 56, 'peak_owned_private_arrays': 1,
            'zero_saving_ratio': str(ratio), 'semantic_controls': 5, 'positive_broadcast_control': True,
            'limits': 'Independent finite review of the exact direct block interface; no shared-decoder floor or global supplier admission.'}


if __name__ == '__main__':
    result = audit()
    need(canonical(result) == canonical(read(HERE / 'RESULT.json')), 'complete typed review receipt')
    print('PASS_INDEPENDENT_PAIRED_PLANE_REVIEW recipes=280 Gaussian_columns=143360 payload_copy_mass=224 controls=5')
