double form_volume(void);

double Iq(double q,
          double radius,
          double thickness,
          double alpha,
          double beta,
          double pringle_sld,
          double solvent_sld);

double Iqxy(double qx, double qy,
          double radius,
          double thickness,
          double alpha,
          double beta,
          double pringle_sld,
          double solvent_sld);

static
double pringleC(double radius,
                double alpha,
                double beta,
                double q,
                double phi,
                double n) {

    double nord, va, vb;
    double bessargs, cosarg, bessargcb;
    double r, retval, yyy;


    va = 0;
    vb = radius;

    // evaluate at Gauss points
    // remember to index from 0,size-1

    double summ = 0.0;		// initialize integral
    int ii = 0;
    do {
        // Using 76 Gauss points
        r = (Gauss76Z[ii] * (vb - va) + vb + va) / 2.0;

        bessargs = q*r*sin(phi);
        cosarg = q*r*r*alpha*cos(phi);
        bessargcb = q*r*r*beta*cos(phi);

        yyy = Gauss76Wt[ii]*r*cos(cosarg)
                *jn(n, bessargcb)
                *jn(2*n, bessargs);
        summ += yyy;

        ii += 1;
    } while (ii < N_POINTS_76);			// end of loop over quadrature points
    //
    // calculate value of integral to return

    retval = (vb - va) / 2.0 * summ;
    retval = retval / pow(r, 2.0);

    return retval;
}

static
double pringleS(double radius,
                double alpha,
                double beta,
                double q,
                double phi,
                double n) {

    double nord, va, vb, summ;
    double bessargs, sinarg, bessargcb;
    double r, retval, yyy;
    // set up the integration
    // end points and weights

    va = 0;
    vb = radius;

    // evaluate at Gauss points
    // remember to index from 0,size-1

    summ = 0.0;		// initialize integral
    int ii = 0;
    do {
        // Using 76 Gauss points
        r = (Gauss76Z[ii] * (vb - va) + vb + va) / 2.0;

        bessargs = q*r*sin(phi);
        sinarg = q*r*r*alpha*cos(phi);
        bessargcb = q*r*r*beta*cos(phi);

        yyy = Gauss76Wt[ii]*r*sin(sinarg)
                    *jn(n, bessargcb)
                    *jn(2*n, bessargs);

        summ += yyy;

        ii += 1;
    } while (ii < N_POINTS_76);			// end of loop over quadrature points
    //
    // calculate value of integral to return

    retval = (vb-va)/2.0*summ;
    retval = retval/pow(r, 2.0);

    return retval;
}

static
double _kernel(double thickness,
               double radius,
               double alpha,
               double beta,
               double q,
               double phi) {

    const double sincarg = q * thickness * cos(phi) / 2.0;
    const double sincterm = pow(sin(sincarg) / sincarg, 2.0);

    //calculate sum term from n = -3 to 3
    double sumterm = 0;
    for (int nn = -3; nn <= 3; nn++) {
        double powc = pringleC(radius, alpha, beta, q, phi, nn);
        double pows = pringleS(radius, alpha, beta, q, phi, nn);

        sumterm += pow(powc, 2.0) + pow(pows, 2.0);
    }

    double retval = 4.0 * sin(phi) * sumterm * sincterm;

    return retval;

}

static double pringles_kernel(double q,
          double radius,
          double thickness,
          double alpha,
          double beta,
          double pringle_sld,
          double solvent_sld)
{

    //upper and lower integration limits
    const double lolim = 0.0;
    const double uplim = M_PI / 2.0;

    double summ = 0.0;			//initialize integral

    double delrho = pringle_sld - solvent_sld; //make contrast term

    for (int i = 0; i < N_POINTS_76; i++) {
        double phi = (Gauss76Z[i] * (uplim - lolim) + uplim + lolim) / 2.0;
        summ += Gauss76Wt[i] * _kernel(thickness, radius, alpha, beta, q, phi);
    }

    double answer = (uplim - lolim) / 2.0 * summ;
    answer *= delrho*delrho;

    //convert to [cm-1]
    answer *= 1.0e-4;

    return answer;
}
double form_volume(void){
    // Unused, so free to return garbage.
    return NAN;
}

double Iq(double q,
          double radius,
          double thickness,
          double alpha,
          double beta,
          double pringle_sld,
          double solvent_sld)
{
    return pringles_kernel(q,
                  radius,
                  thickness,
                  alpha,
                  beta,
                  pringle_sld,
                  solvent_sld);
}

double Iqxy(double qx, double qy,
            double radius,
            double thickness,
            double alpha,
            double beta,
            double pringle_sld,
            double solvent_sld)
{
    double q = sqrt(qx*qx + qy*qy);
    return pringles_kernel(q,
                  radius,
                  thickness,
                  alpha,
                  beta,
                  pringle_sld,
                  solvent_sld);
}

