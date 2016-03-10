r"""
This model provides the form factor, $P(q)$, for a 'pringle' or 'saddle-shaped'
object (a hyperbolic paraboloid).

.. figure:: img/pringles_fig1.png

    (Graphic from Matt Henderson, matt@matthen.com)

The returned value is in units of cm-1, on absolute scale.

Definition
----------

The form factor calculated is

.. math::

    I(q) = (\Delta \rho )^2 V \int^{\pi/2}_0 d\psi \sin{\psi} sinc^2
    \left( \frac{qd\cos{\psi}}{2} \right)
    \left[ \left( S^2_0+C^2_0\right) + 2\sum_{n=1}^{\infty}
     \left( S^2_0+C^2_0\right) \right]

where

.. math::

    C_n = \int^{R}_{0} r dr\cos{qr^2\alpha \cos{\psi}}
    J_n\left( qr^2\beta \cos{\psi}\right)
    J_{2n}\left( qr \sin{\psi}\right)

.. math::

    S_n = \int^{R}_{0} r dr\sin{qr^2\alpha \cos{\psi}}
    J_n\left( qr^2\beta \cos{\psi}\right)
    J_{2n}\left( qr \sin{\psi}\right)


.. figure:: img/pringle-vs-cylinder.png

    1D plot using the default values (with 150 data points).

Reference
---------

S Alexandru Rautu, Private Communication.

"""

from numpy import inf

name = "pringles"
title = "Pringles model for K Edler. Represents a disc that is bent in two directions."
description = """\

"""
category = "shape:cylinder"

# pylint: disable=bad-whitespace, line-too-long
#   ["name", "units", default, [lower, upper], "type","description"],
parameters = [
    ["radius",      "Ang",         60.0,   [0, inf],    "", "Guinier length scale"],
    ["thickness",   "Ang",         10.0,   [0, inf],    "", "Guinier length scale"],
    ["alpha",       "",             0.001, [-inf, inf], "", "Lorentzian length scale"],
    ["beta",        "",             0.02,  [-inf, inf], "", "Radius of gyration"],
    ["pringle_sld", "1e-6/Ang^2",   1.0,   [-inf, inf], "", "Fractal exponent"],
    ["solvent_sld", "1e-6/Ang^2",   6.3,   [-inf, inf], "", "Correlation length"]
    ]
# pylint: enable=bad-whitespace, line-too-long

# source = ["lib/mconf.h", "lib/polevl.c", "lib/j0.c", "lib/jn.c", "lib/gauss76.c", "pringles.c"]
source = ["lib/J0.c", "lib/J1.c", "lib/JN.c", "lib/gauss76.c", "pringles.c"]

demo = dict(background=0.0,
            scale=1.0,
            radius=60.0,
            thickness=10.0,
            alpha=0.001,
            beta=0.02,
            pringle_sld=1.0,
            solvent_sld=6.3)

oldname = 'PringlesModel'
oldpars = dict(scale='scale',
                background='background',
                thickness = 'thickness',
                alpha = 'alpha',
                radius = 'radius',
                beta='beta',
                pringle_sld='sld_pringle',
                solvent_sld='sld_solvent')

tests = [
    [{'guinier_scale': 1.0,
      'lorentzian_scale': 1.0,
      'gyration_radius': 10.0,
      'fractal_exp': 10.0,
      'cor_length': 20.0
     }, 0.1, 0.716532],
    ]
