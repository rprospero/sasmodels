/*							j0.c
 *
 *	Bessel function of order zero
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, j0();
 *
 * y = j0( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns Bessel function of order zero of the argument.
 *
 * The domain is divided into the intervals [0, 5] and
 * (5, infinity). In the first interval the following rational
 * approximation is used:
 *
 *
 *        2         2
 * (w - r  ) (w - r  ) P (w) / Q (w)
 *       1         2    3       8
 *
 *            2
 * where w = x  and the two r's are zeros of the function.
 *
 * In the second interval, the Hankel asymptotic expansion
 * is employed with two rational functions of degree 6/6
 * and 7/7.
 *
 *
 *
 * ACCURACY:
 *
 *                      Absolute error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0, 30       10000       4.4e-17     6.3e-18
 *    IEEE      0, 30       60000       4.2e-16     1.1e-16
 *
 */

/*
Cephes Math Library Release 2.8:  June, 2000
Copyright 1984, 1987, 1989, 2000 by Stephen L. Moshier
*/

/* Note: all coefficients satisfy the relative error criterion
 * except YP, YQ which are designed for absolute error. */

double j0 ( double );

#define TWOOPI 6.36619772367581343075535E-1
#define SQ2OPI 7.9788456080286535587989E-1
#define PIO4   7.85398163397448309616E-1

double j0(double x)
{
    double w, z, p, q, xn;

    const double DR1 = 5.78318596294678452118E0;
    const double DR2 = 3.04712623436620863991E1;
    double RP[8] = {
    -4.79443220978201773821E9,
     1.95617491946556577543E12,
    -2.49248344360967716204E14,
     9.70862251047306323952E15,
     0.0,
     0.0,
     0.0,
     0.0
    };
    double RQ[8] = {
     4.99563147152651017219E2,
     1.73785401676374683123E5,
     4.84409658339962045305E7,
     1.11855537045356834862E10,
     2.11277520115489217587E12,
     3.10518229857422583814E14,
     3.18121955943204943306E16,
     1.71086294081043136091E18,
    };
    double PP[8] = {
     7.96936729297347051624E-4,
     8.28352392107440799803E-2,
     1.23953371646414299388E0,
     5.44725003058768775090E0,
     8.74716500199817011941E0,
     5.30324038235394892183E0,
     9.99999999999999997821E-1,
     0.0
    };
    double PQ[8] = {
     9.24408810558863637013E-4,
     8.56288474354474431428E-2,
     1.25352743901058953537E0,
     5.47097740330417105182E0,
     8.76190883237069594232E0,
     5.30605288235394617618E0,
     1.00000000000000000218E0,
     0.0,
    };
    double QP[8] = {
    -1.13663838898469149931E-2,
    -1.28252718670509318512E0,
    -1.95539544257735972385E1,
    -9.32060152123768231369E1,
    -1.77681167980488050595E2,
    -1.47077505154951170175E2,
    -5.14105326766599330220E1,
    -6.05014350600728481186E0,
    };
    double QQ[8] = {
     6.43178256118178023184E1,
     8.56430025976980587198E2,
     3.88240183605401609683E3,
     7.24046774195652478189E3,
     5.93072701187316984827E3,
     2.06209331660327847417E3,
     2.42005740240291393179E2,
     0.0,
    };
    if( x < 0 )
        x = -x;

    if( x <= 5.0 )
        {
        z = x * x;
        if( x < 1.0e-5 )
            return( 1.0 - z/4.0 );

        p = (z - DR1) * (z - DR2);
        p = p * polevl( z, RP, 3)/p1evl( z, RQ, 8 );
        //printf("Need polevl %e \n", x);
        return( p );
        }

    w = 5.0/x;
    q = 25.0/(x*x);
    p = polevl( q, PP, 6)/polevl( q, PQ, 6 );
    q = polevl( q, QP, 7)/p1evl( q, QQ, 7 );
    xn = x - PIO4;
    p = p * cos(xn) - w * q * sin(xn);

    return( p * SQ2OPI / sqrt(x) );
}

double j1 ( double );

double j1(double x)
{
    double w, z, p, q, xn;

    const double DR1 = 5.78318596294678452118E0;
    const double DR2 = 3.04712623436620863991E1;
    const double Z1 = 1.46819706421238932572E1;
    const double Z2 = 4.92184563216946036703E1;
    const double THPIO4 =  2.35619449019234492885;

    double RP[8] = {
    -4.79443220978201773821E9,
     1.95617491946556577543E12,
    -2.49248344360967716204E14,
     9.70862251047306323952E15,
     0.0,
     0.0,
     0.0,
     0.0
    };
    double RQ[8] = {
     4.99563147152651017219E2,
     1.73785401676374683123E5,
     4.84409658339962045305E7,
     1.11855537045356834862E10,
     2.11277520115489217587E12,
     3.10518229857422583814E14,
     3.18121955943204943306E16,
     1.71086294081043136091E18,
    };
    double PP[8] = {
     7.96936729297347051624E-4,
     8.28352392107440799803E-2,
     1.23953371646414299388E0,
     5.44725003058768775090E0,
     8.74716500199817011941E0,
     5.30324038235394892183E0,
     9.99999999999999997821E-1,
     0.0
    };
    double PQ[8] = {
     9.24408810558863637013E-4,
     8.56288474354474431428E-2,
     1.25352743901058953537E0,
     5.47097740330417105182E0,
     8.76190883237069594232E0,
     5.30605288235394617618E0,
     1.00000000000000000218E0,
     0.0,
    };
    double QP[8] = {
    -1.13663838898469149931E-2,
    -1.28252718670509318512E0,
    -1.95539544257735972385E1,
    -9.32060152123768231369E1,
    -1.77681167980488050595E2,
    -1.47077505154951170175E2,
    -5.14105326766599330220E1,
    -6.05014350600728481186E0,
    };
    double QQ[8] = {
     6.43178256118178023184E1,
     8.56430025976980587198E2,
     3.88240183605401609683E3,
     7.24046774195652478189E3,
     5.93072701187316984827E3,
     2.06209331660327847417E3,
     2.42005740240291393179E2,
     0.0,
    };

    w = x;
    if( x < 0 )
        w = -x;

    if( w <= 5.0 )
        {
        z = x * x;
        w = polevl( z, RP, 3 ) / p1evl( z, RQ, 8 );
        w = w * x * (z - Z1) * (z - Z2);
        return( w );
        }

    w = 5.0/x;
    z = w * w;
    p = polevl( z, PP, 6)/polevl( z, PQ, 6 );
    q = polevl( z, QP, 7)/p1evl( z, QQ, 7 );
    xn = x - THPIO4;
    double sn, cn;
    SINCOS(xn, sn, cn);
    p = p * cn - w * q * sn;

    //p = p * cos(xn) - w * q * sin(xn);

    return( p * SQ2OPI / sqrt(x) );
}
