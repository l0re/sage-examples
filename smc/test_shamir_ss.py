#!/bin/env sage -python
# coding: UTF-8
r"""
Testcases for shamir_ss module

Use as standalone test module for *out of sage tree* testing. 
Please note, this module uses test.py from the host installation,
so an adequate version must be installed.

AUTHORS:

- Thomas Loruenser (2013): initial version

"""
###############################################################################
# Copyright 2013, Thomas Loruenser <thomas.loruenser@ait.ac.at>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
from shamir_ss import ShamirSS

from sage import *
from sage.misc.prandom import randint
from sage.rings.arith import random_prime, next_prime
from sage.functions.log import log

import os
import sys
import argparse

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

def templ_verbose(n, k, order, secret, 
                       decoder='lg', num_shares=None, error_shares=0):
        sss = ShamirSS(n, k, order)
        shares = sss.share(secret)
        for i in range(error_shares):
            shares[i] = (shares[i][0], shares[i][1]+1)
        print(n, k, secret, shares)
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

    def test_random_extension_fields(self, num=128):
        n = 7
        k = 3
        for i in range(num):
            p = 2
            q = randint(log(n,p).N().ceil(), 64)
            # FIXME: 2**16 has sometimes errors due to some internal infinity problem
            if q == 16: continue
            o = p**q
            s = randint(0, o-1)
            assert s == templ_generic(n, k, o, s)
            assert s == templ_generic(n, k, o, s, 'bw', None, 1)


class ManualTest():
    def test_case_01(self):
        assert 42 == templ_verbose(8, 5, 257, 42)

    def test_case_02(self):
        assert 177 == templ_generic(7, 5, 257, 177, 'bw', None, 1)
        assert 177 == templ_generic(7, 5, 257, 177, 'bw', None, 0)
        assert 177 == templ_generic(7, 3, 257, 177, 'bw', None, 0)

        assert 177 == templ_generic(7, 5, 256, 177, 'bw', None, 1)
        assert 177 == templ_generic(7, 5, 256, 177, 'bw', None, 1)
        assert 177 == templ_generic(7, 3, 256, 177, 'bw', None, 2)
        assert 177 != templ_generic(7, 3, 256, 177, 'bw', None, 3)
            
    def test_case_03(self):
        for i in range(100):
            assert 42 == templ_generic(7, 3, 2**16, 42, 'bw', None, 2)
           

    def test_case_04(self):
        # numeric instability
        #n = 7, k = 3, order = 65536, secret = 64206, decoder = 'bw', num_shares = None
        #error_shares = 1
        assert 64206 == templ_verbose(7, 3, 2**16, 64206, 'bw', None, 1)




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
        ManualTest().test_case_04()

    else:
        # run py.test for current file
        pytest.main([sys.argv[0]])
