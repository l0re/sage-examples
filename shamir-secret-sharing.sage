#!/usr/bin/env sage
# vim: set fileencoding=UTF-8 filetype=python :

###############################################################################
# Copyright 2013, Thomas Lorünser
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

###
# globals
#

q = 2; m = 8   # GF(256)

n = 7   # number shares
k = 3   # threshold

s = 216 # secret

F.<a> = GF(q^m)
R.<x>=PolynomialRing(F)

### 
# functions
#
def topoly(x, gen):
    """ converts a coefficient list together with a generator
        into a polynomial 
    """
    poly = 0
    coeff = list(bin(x)[2:])
    coeff.reverse()
    for i, bit in enumerate(coeff):
        if bit == '1': poly += gen^i
    return poly

def tpa(x):
    """ short poly generation with global generator a
    """
    return topoly(x, a)

###
# main sim area
#

# setup and show the polynomial for shamir secret sharing
ssp = tpa(s)
for i in range(1,k):
    ssp += F.random_element() * x^i
print('Polynomial:', [i.int_repr() for i in ssp.coeffs()])


# evaluate polinomial at differnt points (shares)
shares = []
points = []
for i in range(1,n+1):
    shares.append([i,int(ssp(topoly(i,a)).int_repr())])
    points.append([topoly(i,a), ssp(topoly(i,a))])
print('Shares:')
for i,p in zip(shares,points):
    print(i)

# reconstruct with lag BWrange
coeffs = R.lagrange_polynomial(points).coeffs()
print('Reconstructed LG:', [i.int_repr() for i in coeffs])

# introduce malicious point
points[0][1] = 1

# reconstruct with berlekamp-welch
A = []
b = []
for point in points:
    xp = point[0]
    yp = point[1]
    A.append([1, xp, xp^2, xp^3, -yp])
    b.append(yp*xp)

A = Matrix(A[:5])
b = vector(b[:5])

QE = A.solve_right(b)
Q = sum([c * x^i for i,c in enumerate(QE[:4])]); 
E = x + QE[-1]
P = Q.quo_rem(E)[0]

print('BW Polynomial', P)
print('Reconstructed BW:', [i.int_repr() for i in P.coeffs()])

