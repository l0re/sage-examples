# coding: UTF-8
r"""
Number theoretic transform

Implements a finite field (Fast) Fourier Transform. 

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
from sage.matrix.constructor import Matrix
from sage.misc.functional import is_odd

###
# public interface to ntt
#
def ntt(a, F, implementation='fast'):
    n = len(a)
    g = F.gen()
    w = F.one().nth_root(n)
    assert w != F.one(), "No nth root!"
    for i in range(1, n):
        assert w**i != F.one(), "w not primitive root!"

    if implementation == 'slow':
        ntt_impl = _ntt
    elif implementation == 'textbook':
        ntt_impl = _fntt_textbook
    elif implementation == 'fast':
        ntt_impl = _fntt_textbook # FIXME: Efficient implementation is missing

    return ntt_impl(a, w)


def intt(a, F, implementation='fast'):
    n = len(a)
    g = F.gen()
    w = F.one().nth_root(n)
    assert w != F.one(), "No nth root!"
    for i in range(1, n):
        assert w**i != F.one(), "w not primitive root!"

    if implementation == 'slow':
        intt_impl = _intt
    elif implementation == 'textbook':
        intt_impl = _ifntt_textbook
    elif implementation == 'fast':
        intt_impl = _ifntt_textbook # FIXME: Efficient implementation is missin

    return intt_impl(a, w)

###
# private functions
#
def _fntt_textbook(a, w, n = 0, axis = 0):
    n = len(a)
    if n == 1:
        return a
    if is_odd(n):
        return _ntt(a, w)
    else:
        Feven = _fntt_textbook([a[i] for i in xrange(0, n, 2)], w**2)
        Fodd = _fntt_textbook([a[i] for i in xrange(1, n, 2)], w**2)
        
        combined = [0] * n
        for m in xrange(n/2):
            combined[m] = Feven[m] + w**m * Fodd[m]
            combined[m + n/2] = Feven[m] + w**(n/2+m) * Fodd[m]
        return combined

def _ifntt_textbook(a, w):
    n = len(a)
    m = _fntt_textbook(a, 1/w)
    return [x/n for x in m]


def _intt(a, w):
    n = len(a)
    m = _ntt(a, 1/w)
    return [x/n for x in m]


def _ntt(a, w, n = 0, axis = 0):
    n = len(a)
    Fm = Matrix(n, n, lambda i, j: (w**i)**j)
    s = Fm * Matrix(n, 1, a)
    return s.list()

