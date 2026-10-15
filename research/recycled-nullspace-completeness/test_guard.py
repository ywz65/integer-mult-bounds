"""Actual omission/dependence and modular alias controls; stdlib only."""
import importlib.util,json,random,sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
def module(name):
    p=HERE/(name+'.py');s=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(s);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
g=module('guard');src=module('source')

class GuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cache=tempfile.TemporaryDirectory(prefix='null-guard-cache-')
        cls.prefix=sys.pycache_prefix;sys.pycache_prefix=cls.cache.name
        ns,frames,la,cl,w=src.load()
        cls.fast=staticmethod(ns['null_exact_ff']);cls.reference=staticmethod(la.null_exact)
    @classmethod
    def tearDownClass(cls):
        sys.pycache_prefix=cls.prefix;cls.cache.cleanup()

    def test_source_kernel_and_empty_rectangles(self):
        rng=random.Random(20261015);cases=[([],0),([],3),([[]],0),([[0,0]],2),([[1,0],[0,1]],2)]
        for _ in range(180):
            width=rng.randrange(1,11)
            cases.append(([[rng.randrange(-4,5) for _ in range(width)] for _ in range(rng.randrange(0,11))],width))
        for a,k in cases:
            n=self.fast(a,k);certificate=g.certify(a,k,n)
            self.assertEqual(n,self.reference(a,k));self.assertEqual(certificate['nullity'],len(n))

    def test_omitted_dependent_and_zero_vectors_reject(self):
        a=[[1,0,0]];n=self.fast(a,3)
        for bad,reason in [(n[:-1],'incomplete'),([n[0],n[0]],'dependent'),([[0,0,0],n[0]],'dependent'),([], 'incomplete')]:
            with self.subTest(bad=bad),self.assertRaisesRegex(ValueError,reason): g.certify(a,3,bad)

    def test_exact_annihilation_catches_modular_alias(self):
        # This candidate passes annihilation modulo p and has the right modular ranks.
        a=[[1,0]];bad=[[g.PRIME,1]]
        self.assertEqual(g.rank_mod(a,2)+g.rank_mod(bad,2),2)
        with self.assertRaisesRegex(ValueError,'exact input'): g.certify(a,2,bad)

    def test_unlucky_prime_falls_back_without_changing_candidate(self):
        for a,n in [([[g.PRIME,0]],[[0,1]]),([[1,0]],[[0,g.PRIME]])]:
            saved=[r[:] for r in n];receipt=g.certify(a,2,n)
            self.assertEqual(receipt['mode'],'exact-rank-fallback');self.assertEqual(n,saved)
        # Signs, nonzero scaling and basis order do not alter mathematical completeness.
        self.assertEqual(g.certify([[1,0,0]],3,[[0,0,-2],[0,3,0]])['nullity'],2)

    def test_shapes_and_prime_domain(self):
        for a,k,n in [([[1]],2,[]),([[True,0]],2,[[0,1]]),([[1,0]],2,[[0,False]]),([],False,[]),([],1,[[1],[1]])]:
            with self.subTest(a=a,k=k,n=n),self.assertRaises(ValueError):g.certify(a,k,n)
        with self.assertRaisesRegex(ValueError,'prime'):g.certify([[1,0]],2,[[0,1]],prime=15)

    def test_wrapper_checks_original_not_mutated_callback_argument(self):
        def wrong(a,k):a[0]=[0,1];return [[1,0]]
        wrapper=g.wrap(wrong,self.reference)
        original=[[1,0]]
        with self.assertRaisesRegex(ValueError,'exact input'):wrapper(original,2)
        self.assertEqual(original,[[1,0]])

    def test_one_shot_and_nonintegral_fallback(self):
        from fractions import Fraction
        wrapper=g.wrap(self.fast,self.reference)
        a=[[1,2,3]]
        self.assertEqual(wrapper((iter(r) for r in a),3),self.reference(a,3))
        frac=[[Fraction(1,2),Fraction(-3,4),0]]
        self.assertEqual(wrapper(frac,3),self.reference(frac,3))

if __name__=='__main__':unittest.main()
