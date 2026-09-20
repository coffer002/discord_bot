#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

long double ln_em_c(long double x) {
    if (x <= 0) return 0.0;

    long double y = (x - 1.0) / (x + 1.0);
    long double y2 = y * y;
    long double sum = 0.0;
    long double termo = y;

    for (int i = 1; i < 100; i += 2) {
        sum += termo / i;
        termo *= y2;
    }
    return 2.0 * sum;
}

EXPORT long double somar_em_c(long double a, long double b) {
    return a + b;
}

EXPORT long double multiplicar_em_c(long double a, long double b) {
    return a * b;
}

EXPORT long double dividir_em_c(long double a, long double b) {
    return a / b;
}

EXPORT int resto_em_c(int a, int b) {
    return a % b;
}

EXPORT long double modulo_em_c(long double a) {
    if (a >= 0) {
        return a;
    } else {
        return -a;
    }
}

EXPORT long double potencia_c(long double a, int b) {
    long double result = 1.0;
    for (int i = 1; i <= b; i++) {
        result *= a;
    }
    return result;
}

EXPORT long double log_em_c(long double a, long double b) {
    if (b <= 0.0) return -1.0;
    if (a <= 0.0 || a == 1.0) return -1.0;
    return ln_em_c(b) / ln_em_c(a);
}