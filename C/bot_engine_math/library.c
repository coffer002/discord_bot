#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

EXPORT long double somar_em_c(long double a, long double b) {
    return a + b;
}

EXPORT long double multiplicar_em_c(long double a, long double b) {
    return a * b;
}

EXPORT long double dividir_em_c(long double a, long double b) {
    return a / b;
}

EXPORT int modulom_em_c(int a, int b) {
    return a % b;
}

EXPORT long double potencia_c(long double a, int b) {
    long double result = 1.0;
    for (int i = 1; i <= b; i++) {
        result *= a;
    }
    return result;
}