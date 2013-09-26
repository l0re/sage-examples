# coding: UTF-8
r"""
Sharmir Secret Sharing

Implements the original versions of perfectly secure secret sharing 
as proposed by Shamir in 1979. Note that this code is for educational 
purposes only and demonstrate the basic algorithms. 

AUTHORS:

- Thomas Loruenser (2013): initial version

.. TODO::

- Extend module to support input vectors.
- Handle more input types.
- Enable other fields, currently only polynomials over GF(2^8) are supported.

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

from sage.structure.sage_object import SageObject

class ShamirSS(SageObject):
    r"""
    Shamir secret sharing.
   
    This class implements the original version of perfectly secure secret sharing 
    as proposed by Shamir in [Shamir1979]_. It is a very basic implementation
    for educational purposes only.

    EXAMPLES::

        sage: from sage.crypto.smc.shamir_ss import ShamirSS

    Generate shares::

        sage: k = 3; n = 7
        sage: sss = ShamirSS(n,k)
        sage: secret = 42
        sage: shares = sss.share(secret)

    Reconstruct secret (Lagrange interpolation)::

        sage: recsec = sss.reconstruct(shares)
        sage: secret == recsec
        True

    Reconstruct with error shares (Belekamp-Welsch decoder)::

        sage: shares[0] = (shares[0][0], shares[0][1]+1)
        sage: recsec = sss.reconstruct(shares, decoder='bw')
        sage: secret == recsec
        True

    TESTS:

    More random input::

        sage: secret = randint(0,255)
        sage: shares = sss.share(secret)
        sage: recsec = sss.reconstruct(shares, decoder='lag')
        sage: secret == recsec
        True
        sage: recsec = sss.reconstruct(shares, decoder='bw')
        sage: secret == recsec
        True

    Secret must be integer represenation in GF(2^8)::

        sage: secret = 333
        sage: shares = sss.share(secret)
        Traceback (most recent call last):
        ...
        ValueError: integer representation not in field.

    REFERENCES:

    .. [Shamir1979] Shamir, A. (1979). How to share a secret. 
       Communications of the ACM, 22(11), 612–613. :doi:`10.1145/359168.359176`
    """
    def __init__(self, n=7, k=3):
        r"""
        Sharmir secret sharing.

        INPUT:

        - ``k`` --  integer (default: 3) the treshold for reconstruction
        - ``n`` --  integer (default: 7) the number of shares

        EXAMPLES::

            sage: from sage.crypto.smc.shamir_ss import ShamirSS
            sage: k = 3; n = 7
            sage: sss = ShamirSS(n,k)
            sage: secret = 42
            sage: shares = sss.share(secret)
            sage: recsec = sss.reconstruct(shares)
            sage: secret == recsec
            True
        """
        self._q = 2; self._m = 8  # GF(256)
        self._k = k  # threshold
        self._n = n  # number shares

        from sage.rings.finite_rings.constructor import FiniteField
        from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
        self._F = FiniteField(self._q**self._m, 'a')
        self._a = self._F.gen()
        self._R = PolynomialRing(self._F, 'x')
        self._x = self._R.gen()

    ### begin module private api

    def _to_GF(self, x):
        r""" 
        Convert integer representation to finite field GF(2^8)

        Currently all calculations are done in GF(2^8), hence the integer must
        be within this range.

        INPUT:

        - ``x`` --  integer the integer representation to be converted

        OUTPUT:

        The finite field representation in GF(2^8)

        EXAMPLES::
        
            sage: from sage.crypto.smc.shamir_ss import ShamirSS
            sage: k = 3; n = 7
            sage: sss = ShamirSS(n,k)
            sage: sss._to_GF(42)
            a^5 + a^3 + a
            sage: sss._to_GF(255)
            a^7 + a^6 + a^5 + a^4 + a^3 + a^2 + a + 1
        """
        from sage.rings.all import Integer
        try:
            x = Integer(x)
        except TypeError:
            raise TypeError("value is not an integer.")
        if x >= self._q**self._m:
            raise ValueError("integer representation not in field.")
        poly = 0
        coeff = list(bin(x)[2:])
        coeff.reverse()
        for i, bit in enumerate(coeff):
            if bit == '1': poly += self._a**i
        return poly


    def _latex_(self):
        r"""
        Return Latex representation of self.

        EXAMPLES::

            sage: from sage.crypto.smc.shamir_ss import ShamirSS
            sage: sss=ShamirSS()
            sage: latex(sss)
            `(3,7)`-Shamir secret sharing over the field `\Bold{F}_{2^{8}}`
        """
        from sage.misc.latex import latex
        return "`({},{})`-Shamir secret sharing over the field `{}`".format(
            self._k, self._n, latex(self._F))


    def _rec_berlekamp_welch(self, points):
        r"""
        Reconstruct with Berlekamp-Welsh decoding.

        EXAMPLES::

            sage: from sage.crypto.smc.shamir_ss import ShamirSS

        Decoding without errors::

            sage: k = 3; n = 7
            sage: sss = ShamirSS(n,k)
            sage: secret = 42
            sage: shares = sss.share(secret)
            sage: recsec = sss.reconstruct(shares)
            sage: secret == recsec
            True

        Decoding with errors::

            sage: k = 3; n = 7
            sage: sss = ShamirSS(n,k)
            sage: secret = 42
            sage: shares = sss.share(secret)
            sage: shares[0] = (shares[0][0], shares[0][1]+1)
            sage: recsec = sss.reconstruct(shares, decoder='bw')
            sage: secret == recsec
            True

            sage: k = 4; n = 10
            sage: sss = ShamirSS(n,k)
            sage: secret = 84
            sage: shares = sss.share(secret)
            sage: shares[0] = (shares[0][0], shares[0][1]+1)
            sage: shares[1] = (shares[1][0], shares[1][1]+1)
            sage: shares[-1] = (shares[-1][0], shares[-1][1]+1)
            sage: recsec = sss.reconstruct(shares, decoder='bw')
            sage: secret == recsec
            True
        """
        from sage.functions.all import floor
        t = floor((self._n - self._k) / 2.)
        deg_E = t
        deg_Q = len(points) - deg_E - 1

        # generate system of linear equations
        A = []
        b = []
        for point in points:
            xp = point[0]
            yp = point[1]
            syseq = [xp**i for i in range(deg_Q+1)]
            syseq.extend([-yp*xp**i for i in range(deg_E)])
            A.append(syseq)
            b.append(yp*xp**deg_E)

        from sage.matrix.all import Matrix
        from sage.all import vector
        A = Matrix(A)
        b = vector(b)

        # solve and extract secret
        QE = A.solve_right(b)
        Q = sum([c * self._x**i for i,c in enumerate(QE[:deg_Q+1])]);
        E = self._x**deg_E
        E += sum([c * self._x**i for i,c in enumerate(QE[deg_Q+1:])]);
        P = Q.quo_rem(E)[0]
        return P.constant_coefficient().integer_representation()


    def _rec_lagrange(self, points, consistency=False):
        r""" 
        Reconstruct with Lagrange interpolation.

        EXAMPLES::

            sage: from sage.crypto.smc.shamir_ss import ShamirSS

        Erasure decoding::

            sage: k = 3; n = 7
            sage: sss = ShamirSS(n,k)
            sage: secret = 42
            sage: shares = sss.share(secret)
            sage: recsec = sss.reconstruct(shares)
            sage: secret == recsec
            True

            sage: k = 4; n = 10
            sage: sss = ShamirSS(n,k)
            sage: secret = 42
            sage: shares = sss.share(secret)
            sage: recsec = sss.reconstruct(shares)
            sage: secret == recsec
            True
        """
        return self._R.lagrange_polynomial(points).constant_coefficient().integer_representation()


    def _repr_(self):
        r"""
        Return String representation of self.

        EXAMPLES::

            sage: from sage.crypto.smc.shamir_ss import ShamirSS
            sage: sss=ShamirSS()
            sage: print(sss)
            (3,7)-Shamir secret sharing over the field GF(2^8)
        """
        return "({},{})-Shamir secret sharing over the field GF(2^8)".format(
            self._k, self._n)

    ### begin public api

    def share(self, s):
        r"""
        Generate shares.

        A polynomial of degree `k-1` is generated at random with the secret
        being the constant coefficient. It is then evaluated at points starting
        from `1`.

        INPUT:

        - ``s`` -- the secret to be shared (integer which must be in GF(2^8))

        OUTPUT:

        - A list of shares.

        EXAMPLES::

            sage: from sage.crypto.smc.shamir_ss import ShamirSS

        Simple interface::

            sage: k = 3; n = 7
            sage: sss = ShamirSS(n,k)
            sage: secret = 42
            sage: shares = sss.share(secret)
            sage: [i+1 == share[0]  for i, share in enumerate(shares)]
            [True, True, True, True, True, True, True]
        """
        self._s = s  # secret

        # calculate random polynomial
        self._ssp = self._to_GF(s)
        for i in range(1, self._k):
            self._ssp += self._F.random_element() * self._x**i

        # evaluate polinomial at different points (shares)
        shares = []
        for i in range(1, self._n+1):
            shares.append((i, self._ssp(self._to_GF(i)).integer_representation()))
        return shares


    def reconstruct(self, shares, decoder='lag'):
        r"""
        Reconstruct shares.

        INPUT:

        - ``shares`` -- a list of shares (2-tuples of integer)
        - ``decoder`` -- string (default: 'lag') decoder used to reconstruct secret.
            must be one of the supported types 'lag' or 'bw'.

        OUTPUT:

        - The reconstructed secret.

        EXAMPLES::

            sage: from sage.crypto.smc.shamir_ss import ShamirSS

        Simple interface::

            sage: k = 3; n = 7
            sage: sss = ShamirSS(n,k)
            sage: secret = 42
            sage: shares = sss.share(secret)
            sage: recsec = sss.reconstruct(shares)
            sage: secret == recsec
            True

        Decoding with errors::

            sage: shares[0] = (shares[0][0], shares[0][1]+1)
            sage: recsec = sss.reconstruct(shares, decoder='bw')
            sage: secret == recsec
            True

            sage: k = 4; n = 10
            sage: sss = ShamirSS(n,k)
            sage: secret = randint(0, 255)
            sage: shares = sss.share(secret)
            sage: shares[0] = (shares[0][0], shares[0][1]+1)
            sage: shares[1] = (shares[1][0], shares[1][1]+1)
            sage: shares[-1] = (shares[-1][0], shares[-1][1]+1)
            sage: recsec = sss.reconstruct(shares, decoder='bw')
            sage: secret == recsec
            True
        """
        # convert to polynomial
        points = []
        for share in shares:
            points.append((self._to_GF(share[0]), self._to_GF(share[1])))

        # call decoder
        if decoder == 'lag':
            return self._rec_lagrange(points)
        elif decoder == 'bw':
            return self._rec_berlekamp_welch(points)
        else:
            raise ValueError("unknown decoder.")


# vim: set fileencoding=UTF-8 filetype=python :
