double J0(double x);
double J0(double x)
{
    const double ax = fabs(x);
	if (ax < 8.0) {
	    const double y = x*x;
		const double ans1=57568490574.0+y*(-13362590354.0+y*(651619640.7
			+y*(-11214424.18+y*(77392.33017+y*(-184.9052456)))));
		const double ans2=57568490411.0+y*(1029532985.0+y*(9494680.718
			+y*(59272.64853+y*(267.8532712+y*1.0))));
		return ans1/ans2;
	} else {
		const double z=8.0/ax;
		const double y=z*z;
		const double xx=ax-0.785398164;
		const double ans1=1.0+y*(-0.1098628627e-2+y*(0.2734510407e-4
			+y*(-0.2073370639e-5+y*0.2093887211e-6)));
		const double ans2 = -0.1562499995e-1+y*(0.1430488765e-3
			+y*(-0.6911147651e-5+y*(0.7621095161e-6
			-y*0.934945152e-7)));
		double sn,cn;
        SINCOS(xx, sn, cn);
		const double ans=sqrt(0.636619772/ax)*(cn*ans1-z*sn*ans2);
		return ans;
	}
}


