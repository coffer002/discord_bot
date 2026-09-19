#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

EXPORT int somar_em_c(int a, int b) {
    return a + b;
}
EXPORT int multiplicar_em_c(int a, int b) {
    return a * b;
}
EXPORT int dividir_em_c(int a, int b) {
    return a / b;
}
EXPORT int modulom_em_c(int a, int b) {
    return a % b;
}
EXPORT int potencia_c(int a, int b) {
    int result = 1;
    for (int i = 1; i <= b; i++) {
        result *= a;
    }
    return result;
}