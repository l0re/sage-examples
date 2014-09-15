#!/bin/env sage -python
# coding: UTF-8
r"""
Test the number theoretic transform implementation.

Implements test cases fo the finite field (Fast) Fourier Transform.

AUTHORS:

- Thomas Loruenser (2014): initial version

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
from sage import *
#from sage.misc.prandom import randint
#from sage.rings.arith import random_prime, next_prime
#from sage.functions.log import log

from sage.rings.finite_rings.constructor import FiniteField
from sage.misc.functional import parent
from sage.misc.functional import is_odd
from sage.matrix.constructor import Matrix

import os
import sys
import argparse

# make host packages available
sys.path.append('/usr/lib/python2.7/dist-packages')
import pytest

import ntt

def simple_test(F, n, k):
    m = [F.zero_element()] * n
    for i in range(k):
        m[i] = F.one_element()

    s = ntt.ntt(m, F, implementation='slow')
    ss = ntt.intt(s, F, implementation='slow')

    r = ntt.ntt(m, F, implementation='fast')
    rr = ntt.intt(r, F, implementation='fast')

    #print "m =", m
    #print "s =", s
    #print "r =", r
    #print "ss=", ss
    #print "rr=", rr
    #print "-----------------"

    assert r == s and m == ss and m == rr, "ERROR!!!"


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

    F = FiniteField(7)
    simple_test(F, 6, 3)

    F = FiniteField(257)
    simple_test(F, 4, 3)
    simple_test(F, 256, 90)

    F = FiniteField(256, 'a')
    simple_test(F, 15, 7)
