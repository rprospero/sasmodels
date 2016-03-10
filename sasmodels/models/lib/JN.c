#define ACC 60.0
#define BIGNO 1.0e10
#define BIGNI 1.0e-10

double jn(int n, double x);

double jn_kernel(int n, double x)
{
	double J0(double x);
	double J1(double x);
	int j,jsum,m;
	double ax,bj,bjm,bjp,sum,tox,ans;

	ax=fabs(x);
	if (ax == 0.0)
		return 0.0;
	else if (ax > (double) n) {
		tox=2.0/ax;
		bjm=J0(ax);
		bj=J1(ax);
		for (j=1;j<n;j++) {
			bjp=j*tox*bj-bjm;
			bjm=bj;
			bj=bjp;
		}
		ans=bj;
	} else {
		tox=2.0/ax;
		m=2*((n+(int) sqrt(ACC*n))/2);
		jsum=0;
		bjp=ans=sum=0.0;
		bj=1.0;
		for (j=m;j>0;j--) {
			bjm=j*tox*bj-bjp;
			bjp=bj;
			bj=bjm;
			if (fabs(bj) > BIGNO) {
				bj *= BIGNI;
				bjp *= BIGNI;
				ans *= BIGNI;
				sum *= BIGNI;
			}
			if (jsum) sum += bj;
			jsum=!jsum;
			if (j == n) ans=bjp;
		}
		sum=2.0*sum-bj;
		ans /= sum;
	}
	return x < 0.0 && (n & 1) ? -ans : ans;
}


double jn(int n, double x)
{
    if( n == 0 )
        return( J0(x) );
    if( n == 1 )
        return( J1(x) );
    if( n == -1 )
        return( -J1(x) );
    if( n >= 2 )
        return jn_kernel(n, x);
    if( n <= -2 )
        return pow(-1.0,-n)*jn_kernel(-n, x);
}

#undef ACC
#undef BIGNO
#undef BIGNI
/* (C) Copr. 1986-92 Numerical Recipes Software ?421.1-9. */

