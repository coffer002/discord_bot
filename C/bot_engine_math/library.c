#include <math.h>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

EXPORT double ln_em_c(double x) {
    if (isnan(x)) return x;
    if (x < 0.0)  return NAN;
    if (x == 0.0) return -INFINITY;
    if (isinf(x)) return x;

    int k;
    double m = frexp(x, &k);            // x = m * 2^k, m em [0.5, 1)

    if (m < 0.70710678118654752440) {   // centraliza em torno de 1
        m *= 2.0;
        k--;
    }                                   // agora m em [0.707, 1.414)

    double y  = (m - 1.0) / (m + 1.0);  // |y| <= 0.1716
    double y2 = y * y;
    double sum = 0.0, termo = y;

    for (int i = 1; i < 40; i += 2) {
        double delta = termo / i;
        sum += delta;
        if (fabs(delta) < 1e-17 * fabs(sum)) break;
        termo *= y2;
    }

    return 2.0 * sum + k * 0.69314718055994530942;
}

static double exp_em_c(double x) {
    if (isnan(x)) return x;
    if (x >  709.79) return INFINITY;   // overflow de double
    if (x < -745.20) return 0.0;        // underflow
    if (x == 0.0) return 1.0;

    // x = k*ln2 + r, com |r| <= ln2/2 ≈ 0.3466
    int k = (int)(x * 1.44269504088896340736 + (x >= 0 ? 0.5 : -0.5));

    // ln2 em duas parcelas: evita perder bits em k*ln2 quando k é grande
    double r = (x - k * 0.693147180559945286227)
                   - k * 2.319046813846299558e-17;

    double sum = 1.0, termo = 1.0;
    for (int i = 1; i < 20; i++) {
        termo *= r / i;
        sum += termo;
        if (fabs(termo) < 1e-17 * sum) break;
    }
    return ldexp(sum, k);
}

EXPORT double somar_em_c(double a, double b) {
    return a + b;
}

EXPORT double multiplicar_em_c(double a, double b) {
    return a * b;
}

EXPORT double dividir_em_c(double a, double b) {
    return a / b;
}

EXPORT int resto_em_c(int a, int b) {
    if (b == 0) return 0;               // evita SIGFPE
    if (b == -1) return 0;              // evita UB em INT_MIN % -1
    return a % b;
}

EXPORT double modulo_em_c(double a) {
    return fabs(a);
}

EXPORT double potencia_c(double a, double b) {
    if (isnan(a) || isnan(b)) return NAN;
    if (b == 0.0) return 1.0;           // inclui 0^0 = 1
    if (a == 1.0) return 1.0;
    if (a == 0.0) return (b > 0.0) ? 0.0 : INFINITY;

    if (a < 0.0) {
        if (b != floor(b)) return NAN;  // raiz de índice par de negativo
        double mag = exp_em_c(b * ln_em_c(-a));
        return (fmod(fabs(b), 2.0) == 1.0) ? -mag : mag;
    }
    return exp_em_c(b * ln_em_c(a));
}

/*
EXPORT double potencia_c(double a, int b) {
    double result = 1.0;
    for (int i = 1; i <= b; i++) {
        result *= a;
    }
    return result;
} */

EXPORT double log_em_c(double a, double b) {
    if (isnan(a) || isnan(b)) return NAN;
    if (b <= 0.0) return NAN;
    if (a <= 0.0 || a == 1.0) return NAN;
    return ln_em_c(b) / ln_em_c(a);
}