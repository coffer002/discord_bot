#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

double ln_em_c(double x) {
    if (x <= 0) return 0.0;

    double y = (x - 1.0) / (x + 1.0);
    double y2 = y * y;
    double sum = 0.0;
    double termo = y;

    for (int i = 1; i < 100; i += 2) {
        sum += termo / i;
        termo *= y2;
    }
    return 2.0 * sum;
}

double exp_em_c(double x) {            //taylor series <3
    double sum = 1.0;
    double termo = 1.0;

    for (int i = 1; i < 100; i++) {
        termo *= x / i;
        sum += termo;
        if (termo < 1e-15 && termo > -1e-15) break;
    }
    return sum;
}


EXPORT double somar_em_c(double a, double b) {
    return a + b;
}

EXPORT double subtrair_em_c(double a, double b) {
    return a - b;
}

EXPORT double multiplicar_em_c(double a, double b) {
    return a * b;
}

EXPORT double dividir_em_c(double a, double b) {
    return a / b;
}

EXPORT int resto_em_c(int a, int b) {
    return a % b;
}

EXPORT double modulo_em_c(double a) {
    if (a >= 0) {
        return a;
    } else {
        return -a;
    }
}

EXPORT double potencia_em_c(double a, double b) {
    if (a == 0.0) return 0.0;
    if (b == 0.0) return 1.0;
    if (a < 0.0) return 124123.2314;

    return exp_em_c(b * ln_em_c(a));
}


/*
EXPORT double potencia_em_c(double a, int b) {
    double result = 1.0;
    for (int i = 1; i <= b; i++) {
        result *= a;
    }
    return result;
} */

EXPORT double log_em_c(double a, double b) {
    if (b <= 0.0) return 124123.2314;
    if (a <= 0.0 || a == 1.0) return 124123.2314;
    return ln_em_c(b) / ln_em_c(a);
}