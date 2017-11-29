"""
Conversion of scattering cross section from SANS (I(q), or rather, ds/dO) in absolute
units (cm-1)into SESANS correlation function G using a Hankel transformation, then converting
the SESANS correlation function into polarisation from the SESANS experiment

Everything is in units of metres except specified otherwise (NOT TRUE!!!)
Everything is in conventional units (nm for spin echo length)

Wim Bouwman (w.g.bouwman@tudelft.nl), June 2013
"""

from __future__ import division

import numpy as np  # type: ignore
import logging
from numpy import pi, exp  # type: ignore
from scipy.special import j0

class SesansTransform(object):
    """
    Spin-Echo SANS transform calculator.  Similar to a resolution function,
    the SesansTransform object takes I(q) for the set of *q_calc* values and
    produces a transformed dataset

    *SElength* (A) is the set of spin-echo lengths in the measured data.

    *zaccept* (1/A) is the maximum acceptance of scattering vector in the spin
    echo encoding dimension (for ToF: Q of min(R) and max(lam)).

    *Rmax* (A) is the maximum size sensitivity; larger radius requires more
    computation time.
    """
    #: SElength from the data in the original data units; not used by transform
    #: but the GUI uses it, so make sure that it is present.
    q = None  # type: np.ndarray

    #: q values to calculate when computing transform
    q_calc = None  # type: np.ndarray

    # transform arrays
    _H = None  # type: np.ndarray
    _H0 = None # type: np.ndarray

    def __init__(self, z, SElength, lam, zaccept, Rmax):
        # type: (np.ndarray, float, float) -> None
        #import logging; logging.info("creating SESANS transform")
        self.q = z
        self._set_hankel(SElength, lam, zaccept, Rmax)

    def apply(self, Iq):
        # tye: (np.ndarray) -> np.ndarray
        G0 = np.dot(self._H0, Iq)
        G = np.dot(self._H.T, Iq)
        P = G - G0
        return P

    def _set_hankel(self, SElength, lam, zaccept, Rmax):
        # type: (np.ndarray, float, float) -> None
        # Force float32 arrays, otherwise run into memory problems on some machines
        SElength = np.asarray(SElength, dtype='float32')

        #Rmax = #value in text box somewhere in FitPage?
        q_max = 2*pi / (SElength[1] - SElength[0])
        q_min = 0.1 * 2*pi / (np.size(SElength) * SElength[-1])
        q = np.arange(q_min, q_max, q_min, dtype='float32')
        dq = q_min

        H0 = np.float32(dq/(2*pi)) * q

        repq = np.tile(q, (SElength.size, 1)).T
        repSE = np.tile(SElength, (q.size, 1))
        H = np.float32(dq/(2*pi)) * j0(repSE*repq) * repq

        replam = np.tile(lam, (q.size, 1))
        reptheta = np.arcsin(repq*replam/2*np.pi)
        mask = reptheta > zaccept
        H[mask] = 0

        self.q_calc = q
        self._H, self._H0 = H, H0


class SesansTransform2D(object):
    """
    Spin-Echo SANS transform calculator.  Similar to a resolution function,
    the SesansTransform object takes I(q) for the set of *q_calc* values and
    produces a transformed dataset.  This particular implementation takes
    a 2D set of q-values and returns a 1D SESANS signal, allowing the
    examination of oriented samples in SASView.

    *SElength* (A) is the set of spin-echo lengths in the measured data.

    *zaccept* (1/A) is the maximum acceptance of scattering vector in the spin
    echo encoding dimension (for ToF: Q of min(R) and max(lam)).

    *Rmax* (A) is the maximum size sensitivity; larger radius requires more
    computation time.
    """

    #: SElength from the data in the original data units; not used by transform
    #: but the GUI uses it, so make sure that it is present.
    q = None  # type: np.ndarray

    #: q values to calculate when computing transform
    q_calc = None  # type: np.ndarray

    # transform arrays
    _H = None   # type: np.ndarray
    _H0 = None  # type: np.ndarray
    _lam = None

    def __init__(self, z, SElength, lam, zaccept, Rmax):
        logging.warn("Creating Transform")
        self.q = z
        self.__set_cosine(SElength, lam, zaccept, Rmax)

    def apply(self, Iq):
        # tye: (np.ndarray) -> np.ndarray

        # Calculate the polarisation at each pixel
        logging.warn("Applying Transform")
        pol = self.pol  # FIXME
        logging.warn(pol.shape)
        logging.warn(self.q_calc.shape)
        logging.warn(Iq)

        # We encode on direction Y, so all counts along direction X can
        # be summed
        Iq = np.sum(Iq, axis=0)
        Iq = Iq.reshape((-1, 1))
        logging.warn(Iq.shape)

        # Get the up and down counts
        P = np.nansum(Iq * pol, axis=0)
        P /= np.nansum(Iq, axis=0)
        logging.warn(P)
        logging.warn(np.log(P)*self.lam**-2)

        return np.log(P)*self.lam**-2

    def __set_cosine(self, SElength, lam, zaccept, Rmax):
        logging.warn("Calculating Transform")
        SElength = np.asarray(SElength, dtype='float32')

        q_max = 2*pi / (SElength[1] - SElength[0])
        q_min = 0.1 * 2*pi / (np.size(SElength) * SElength[-1])
        q = np.arange(q_min, q_max, q_min*5, dtype='float32')
        dq = q_min

        H0 = np.float32(dq/(2*pi))

        repq = np.tile(q, (SElength.size, 1)).T
        repSE = np.tile(SElength, (q.size, 1))
        H = np.cos(repSE*repq)

        self.q_calc = q
        self.pol = H
        self.lam = lam
