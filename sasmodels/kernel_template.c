// GENERATED CODE --- DO NOT EDIT ---
// Code is produced by sasmodels.gen from sasmodels/models/MODEL.c

#ifdef __OPENCL_VERSION__
# define USE_OPENCL
#endif

#define USE_KAHAN_SUMMATION 0

// If opencl is not available, then we are compiling a C function
// Note: if using a C++ compiler, then define kernel as extern "C"
#ifndef USE_OPENCL
#  ifdef __cplusplus
      #include <cstdio>
      #include <cmath>
      using namespace std;
      #if defined(_MSC_VER)
         #include <limits>
         #include <float.h>
         #define kernel extern "C" __declspec( dllexport )
         inline double trunc(double x) { return x>=0?floor(x):-floor(-x); }
         inline double fmin(double x, double y) { return x>y ? y : x; }
         inline double fmax(double x, double y) { return x<y ? y : x; }
         inline double isnan(double x) { return _isnan(x); }
         #define NAN (std::numeric_limits<double>::quiet_NaN()) // non-signalling NaN
         static double cephes_expm1(double x) {
            // Adapted from the cephes math library.
            // Copyright 1984 - 1992 by Stephen L. Moshier
            if (x != x || x == 0.0) {
               return x; // NaN and +/- 0
            } else if (x < -0.5 || x > 0.5) {
               return exp(x) - 1.0;
            } else {
               const double xsq = x*x;
               const double p = (((
                  +1.2617719307481059087798E-4)*xsq
                  +3.0299440770744196129956E-2)*xsq
                  +9.9999999999999999991025E-1);
               const double q = ((((
                  +3.0019850513866445504159E-6)*xsq
                  +2.5244834034968410419224E-3)*xsq
                  +2.2726554820815502876593E-1)*xsq
                  +2.0000000000000000000897E0);
               double r = x * p;
               r =  r / (q - r);
               return r+r;
             }
         }
         #define expm1 cephes_expm1
     #else
         #define kernel extern "C"
     #endif
     inline void SINCOS(double angle, double &svar, double &cvar) { svar=sin(angle); cvar=cos(angle); }
#  else
     #include <stdio.h>
     #include <tgmath.h> // C99 type-generic math, so sin(float) => sinf
     // MSVC doesn't support C99, so no need for dllexport on C99 branch
     #define kernel
     #define SINCOS(angle,svar,cvar) do {const double _t_=angle; svar=sin(_t_);cvar=cos(_t_);} while (0)
#  endif
#  define global
#  define local
#  define constant const
// OpenCL powr(a,b) = C99 pow(a,b), b >= 0
// OpenCL pown(a,b) = C99 pow(a,b), b integer
#  define powr(a,b) pow(a,b)
#  define pown(a,b) pow(a,b)
#else
#  if defined(USE_SINCOS)
#    define SINCOS(angle,svar,cvar) svar=sincos(angle,&cvar)
#  else
#    define SINCOS(angle,svar,cvar) do {const double _t_=angle; svar=sin(_t_);cvar=cos(_t_);} while (0)
#  endif
#endif

// Standard mathematical constants:
//   M_E, M_LOG2E, M_LOG10E, M_LN2, M_LN10, M_PI, M_PI_2=pi/2, M_PI_4=pi/4,
//   M_1_PI=1/pi, M_2_PI=2/pi, M_2_SQRTPI=2/sqrt(pi), SQRT2, SQRT1_2=sqrt(1/2)
// OpenCL defines M_constant_F for float constants, and nothing if double
// is not enabled on the card, which is why these constants may be missing
#ifndef M_PI
#  define M_PI 3.141592653589793
#endif
#ifndef M_PI_2
#  define M_PI_2 1.570796326794897
#endif
#ifndef M_PI_4
#  define M_PI_4 0.7853981633974483
#endif
#ifndef M_E
#  define M_E 2.718281828459045091
#endif

// Non-standard function library
// pi/180, used for converting between degrees and radians
// 4/3 pi for computing sphere volumes
// square and cube for computing squares and cubes
#ifndef M_PI_180
#  define M_PI_180 0.017453292519943295
#endif
#ifndef M_4PI_3
#  define M_4PI_3 4.18879020478639
#endif
//inline double square(double x) { return pow(x,2.0); }
//inline double square(double x) { return pown(x,2); }
inline double square(double x) { return x*x; }
inline double cube(double x) { return x*x*x; }
inline double sinc(double x) { return x==0 ? 1.0 : sin(x)/x; }


%(DEFINES)s

%(SOURCES)s

/*
    ##########################################################
    #                                                        #
    #   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   #
    #   !!                                              !!   #
    #   !!  KEEP THIS CODE CONSISTENT WITH KERNELPY.PY  !!   #
    #   !!                                              !!   #
    #   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   #
    #                                                        #
    ##########################################################
*/

#ifdef IQ_KERNEL_NAME
kernel void IQ_KERNEL_NAME(
    global const double *q,
    global double *result,
    const int Nq,
#ifdef IQ_OPEN_LOOPS
  #ifdef USE_OPENCL
    global double *loops_g,
  #endif
    local double *loops,
    const double cutoff,
    IQ_DISPERSION_LENGTH_DECLARATIONS,
#endif
    IQ_FIXED_PARAMETER_DECLARATIONS
    )
{
#ifdef USE_OPENCL
  #ifdef IQ_OPEN_LOOPS
  // copy loops info to local memory
  event_t e = async_work_group_copy(loops, loops_g, (IQ_DISPERSION_LENGTH_SUM)*2, 0);
  wait_group_events(1, &e);
  #endif

  int i = get_global_id(0);
  if (i < Nq)
#else
  #pragma omp parallel for
  for (int i=0; i < Nq; i++)
#endif
  {
    const double qi = q[i];
#ifdef IQ_OPEN_LOOPS
    double ret=0.0, norm=0.0;
  #ifdef VOLUME_PARAMETERS
    double vol=0.0, norm_vol=0.0;
  #endif
    IQ_OPEN_LOOPS
    //for (int radius_i=0; radius_i < Nradius; radius_i++) {
    //  const double radius = loops[2*(radius_i)];
    //  const double radius_w = loops[2*(radius_i)+1];

    const double weight = IQ_WEIGHT_PRODUCT;
    if (weight > cutoff) {
      const double scattering = Iq(qi, IQ_PARAMETERS);
      // allow kernels to exclude invalid regions by returning NaN
      if (!isnan(scattering)) {
        ret += weight*scattering;
        norm += weight;
      #ifdef VOLUME_PARAMETERS
        const double vol_weight = VOLUME_WEIGHT_PRODUCT;
        vol += vol_weight*form_volume(VOLUME_PARAMETERS);
        norm_vol += vol_weight;
      #endif
      }
    //else { printf("exclude qx,qy,I:%%g,%%g,%%g\n",qi,scattering); }
    }
    IQ_CLOSE_LOOPS
  #ifdef VOLUME_PARAMETERS
    if (vol*norm_vol != 0.0) {
      ret *= norm_vol/vol;
    }
  #endif
    result[i] = scale*ret/norm+background;
#else
    result[i] = scale*Iq(qi, IQ_PARAMETERS) + background;
#endif
  }
}
#endif


#ifdef IQXY_KERNEL_NAME
kernel void IQXY_KERNEL_NAME(
    global const double *qx,
    global const double *qy,
    global double *result,
    const int Nq,
#ifdef IQXY_OPEN_LOOPS
  #ifdef USE_OPENCL
    global double *loops_g,
  #endif
    local double *loops,
    const double cutoff,
    IQXY_DISPERSION_LENGTH_DECLARATIONS,
#endif
    IQXY_FIXED_PARAMETER_DECLARATIONS
    )
{
#ifdef USE_OPENCL
  #ifdef IQXY_OPEN_LOOPS
  // copy loops info to local memory
  event_t e = async_work_group_copy(loops, loops_g, (IQXY_DISPERSION_LENGTH_SUM)*2, 0);
  wait_group_events(1, &e);
  #endif

  int i = get_global_id(0);
  if (i < Nq)
#else
  #pragma omp parallel for
  for (int i=0; i < Nq; i++)
#endif
  {
    const double qxi = qx[i];
    const double qyi = qy[i];
    #if USE_KAHAN_SUMMATION
    double accumulated_error = 0.0;
    #endif
#ifdef IQXY_OPEN_LOOPS
    double ret=0.0, norm=0.0;
    #ifdef VOLUME_PARAMETERS
    double vol=0.0, norm_vol=0.0;
    #endif
    IQXY_OPEN_LOOPS
    //for (int radius_i=0; radius_i < Nradius; radius_i++) {
    //  const double radius = loops[2*(radius_i)];
    //  const double radius_w = loops[2*(radius_i)+1];

    const double weight = IQXY_WEIGHT_PRODUCT;
    if (weight > cutoff) {

      const double scattering = Iqxy(qxi, qyi, IQXY_PARAMETERS);
      if (!isnan(scattering)) { // if scattering is bad, exclude it from sum
      //if (scattering >= 0.0) { // scattering cannot be negative
        // TODO: use correct angle for spherical correction
        // Definition of theta and phi are probably reversed relative to the
        // equation which gave rise to this correction, leading to an
        // attenuation of the pattern as theta moves through pi/2.  Either
        // reverse the meanings of phi and theta in the forms, or use phi
        // rather than theta in this correction.  Current code uses cos(theta)
        // so that values match those of sasview.
      #if defined(IQXY_HAS_THETA) // && 0
        const double spherical_correction
          = (Ntheta>1 ? fabs(cos(M_PI_180*theta))*M_PI_2:1.0);
        const double next = spherical_correction * weight * scattering;
      #else
        const double next = weight * scattering;
      #endif
      #if USE_KAHAN_SUMMATION
        const double y = next - accumulated_error;
        const double t = ret + y;
        accumulated_error = (t - ret) - y;
        ret = t;
      #else
        ret += next;
      #endif
        norm += weight;
      #ifdef VOLUME_PARAMETERS
        const double vol_weight = VOLUME_WEIGHT_PRODUCT;
        vol += vol_weight*form_volume(VOLUME_PARAMETERS);
        norm_vol += vol_weight;
      #endif
      }
      //else { printf("exclude qx,qy,I:%%g,%%g,%%g\n",qi,scattering); }
    }
    IQXY_CLOSE_LOOPS
  #ifdef VOLUME_PARAMETERS
    if (vol*norm_vol != 0.0) {
      ret *= norm_vol/vol;
    }
  #endif
    result[i] = scale*ret/norm+background;
#else
    result[i] = scale*Iqxy(qxi, qyi, IQXY_PARAMETERS) + background;
#endif
  }
}
#endif
