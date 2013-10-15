#!/bin/env sage -python
from sage import *
from shamir_ss import ShamirSS
from sage.misc.prandom import randint
from sage.rings.arith import random_prime, next_prime
from sage.functions.log import log

import os
import sys

# make host packages available
sys.path.append('/usr/lib/python2.7/dist-packages')
import pytest


def templ_generic(n, k, order, secret, 
                       decoder='lg', num_shares=None, error_shares=0):
        sss = ShamirSS(n, k, order)
        shares = sss.share(secret)
        for i in range(error_shares):
            shares[i] = (shares[i][0], shares[i][1]+1)
        return sss.reconstruct(shares[:num_shares], decoder=decoder)


class TestShamirSS():
    def test_prime_fields(self):
        assert 42 == templ_generic(7, 3, 257, 42)
        assert 42 == templ_generic(15, 5, 257, 42)
        assert 42 == templ_generic(42, 16, 257, 42)
        assert 42 == templ_generic(7, 3, 257, 42)
        assert 177 == templ_generic(7, 3, 257, 177, 'bw', None, 1)
        assert 177 == templ_generic(7, 3, 257, 177, 'bw', None, 2)

    def test_random_prime_fields(self, num=16):
        n = 7
        k = 3
        for i in range(num):
            o = random_prime(2**128, lbound=n)
            s = randint(0, o-1)
            assert s == templ_generic(7, 3, o, s)

    def test_extenstion_fields(self):
        assert 42 == templ_generic(7, 3, 2**8, 42)
        assert 42 == templ_generic(7, 3, 2**8, 42, 'bw', None, 2)

    def test_random_extenstion_fields(self, num=16):
        n = 7
        k = 3
        for i in range(num):
            p = 2
            q = randint(log(n,p).N().ceil(), 64)
            o = p**q
            s = randint(0, o-1)
            assert s == templ_generic(n, k, o, s)
            assert s == templ_generic(n, k, o, s, 'bw', None, 1)

pytest.main()

