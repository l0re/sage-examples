# coding: UTF-8
from berlekamp_welsh import berlekamp_welsh

# import sage stuff
from sage import *
from sage.rings.finite_rings.constructor import FiniteField
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing


# import from system
import sys
import argparse

# make host packages available
sys.path.append('/usr/lib/python2.7/dist-packages')
import pytest


### py.test cases
class TestDummy():
    def test_01(self):
        order = 2**8
        F = FiniteField(order, 'a')
        P = PolynomialRing(F, 'x')
        n = 7
        deg = 2
        poly = F.fetch_int(42)
        for i in range(1, deg+1):
            poly += F.random_element() * P.gen()**i

        # evaluate polynomial at different points (shares)
        print(poly)
        points = [(F.fetch_int(i), poly(F.fetch_int(i))) for i in range(1, n+1)]
        points[0] = (points[0][0], points[0][1] + F.fetch_int(9))
        print(points)
        assert poly == berlekamp_welsh(deg, points)

#### manual test cases
class ManualTest():
    def test_generic_01(self):

        F = FiniteField(2**8, 'a')

        #shares = [(1, 22), (2, 82), (3, 110), (4, 218), (5, 230)]
        points = [(1, 22), (2, 82), (3, 110), (4, 219)]
        points = [(F.fetch_int(x), F.fetch_int(y)) for x,y in shares]
        p = berlekamp_welsh(1, points)
        pint = ([coeff.integer_representation() for coeff in p])
        #pint = (map(lambda x: x.integer_representation(), p))
        print(p, pint)
        assert [42,60] == pint


    def test_generic_02(self):

        F = FiniteField(2**8, 'a')
        shares = [(1,1), (2,121), (3,97), (4,77), (5,29)]
        points = [(F.fetch_int(x), F.fetch_int(y)) for x,y in shares]
        p = berlekamp_welsh(5, points)
        print(p)
        print([coeff.integer_representation() for coeff in p])
        print(map(lambda x: x.integer_representation(), p))



### main
def parseargs():
    """ Parse the commandline arguments
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-m', '--manual', action='store_true', 
                        help='Run test cases manually.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parseargs()

    if args.manual:
        # manual testing zone
        ManualTest().test_generic_01()

    else:
        # run py.test for current file
        pytest.main([sys.argv[0]])


# vim: set fileencoding=UTF-8 filetype=python :
