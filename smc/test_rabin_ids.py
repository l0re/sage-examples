#!/bin/env sage -python
# coding: UTF-8
r"""
Testcases for rabin_ids module

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
from rabin_ids import RabinIDS

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
        ids = RabinIDS(n, k, order)
        shares = ids.share(secret)
        for block in shares:
            for i in range(error_shares):
                block[i] = (block[i][0], block[i][1]+1)
        return ids.reconstruct(shares, decoder=decoder)


def templ_verbose(n, k, order, secret, 
                       decoder='lg', num_shares=None, error_shares=0):
        ids = RabinIDS(n, k, order)
        print("secret:", secret)
        shares = ids.share(secret)
        print("shares:", shares)
        for block in shares:
            for i in range(error_shares):
                block[i] = (block[i][0], block[i][1]+1)
        print("errors:", shares)
        recsec = ids.reconstruct(shares, decoder=decoder)
        print("reconstructed:", recsec)
        return recsec


class TestRabinIDS():
    def test_prime_fields(self):
        data = [i for i in range(15)]
        assert data == templ_generic(7, 3, 257, data)
        assert data == templ_generic(15, 5, 257, data)
        data = [i for i in range(32)]
        assert data == templ_generic(42, 16, 257, data)
        data = [i for i in range(12)]
        assert data == templ_generic(7, 3, 257, data)
        assert data == templ_generic(7, 3, 257, data, 'bw', None, 1)
        assert data == templ_generic(7, 3, 257, data, 'bw', None, 2)

    def test_extenstion_fields(self):
        data = [i for i in range(12)]
        assert data == templ_generic(7, 3, 2**8, data)
        assert data == templ_generic(7, 3, 2**8, data, 'bw', None, 2)


class ManualTest():
    def test_case_tmp(self):
        data = [i for i in range(12)]
        assert data == templ_verbose(7, 3, 2**8, data, 'lg', None, 0)
        assert data == templ_verbose(7, 3, 2**8, data, 'bw', None, 1)


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
        ManualTest().test_case_tmp()

    else:
        # run py.test for current file
        pytest.main([sys.argv[0]])
