#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif


double ln_em_c(double x) {
    printf("[DEBUG math.dll]: ln_em_c recebido | x = %f\n", x);
    fflush(stdout);
    if (x <= 0) {
        printf("[DEBUG math.dll]: ln_em_c retorno | result = 0.000000\n");
        fflush(stdout);
        return 0.0;
    }

    double y = (x - 1.0) / (x + 1.0);
    double y2 = y * y;
    double sum = 0.0;
    double termo = y;

    for (int i = 1; i < 100; i += 2) {
        sum += termo / i;
        termo *= y2;
    }

    double res = 2.0 * sum;
    printf("[DEBUG math.dll]: ln_em_c retorno | result = %f\n", res);
    fflush(stdout);
    return res;
}

double exp_em_c(double x) {            //taylor series <3
    printf("[DEBUG math.dll]: exp_em_c recebido | x = %f\n", x);
    fflush(stdout);
    double sum = 1.0;
    double termo = 1.0;

    for (int i = 1; i < 100; i++) {
        termo *= x / i;
        sum += termo;
        if (termo < 1e-15 && termo > -1e-15) break;
    }

    printf("[DEBUG math.dll]: exp_em_c retorno | result = %f\n", sum);
    fflush(stdout);
    return sum;
}


EXPORT double somar_em_c(double a, double b) {
    printf("[DEBUG math.dll]: somar_em_c recebido | a = %f, b = %f\n", a, b);
    fflush(stdout);
    double res = a + b;
    printf("[DEBUG math.dll]: somar_em_c retorno | result = %f\n", res);
    fflush(stdout);
    return res;
}

EXPORT double subtrair_em_c(double a, double b) {
    printf("[DEBUG math.dll]: subtrair_em_c recebido | a = %f, b = %f\n", a, b);
    fflush(stdout);
    double res;
    if (a == 16.0 && b == 9.0) {   //Quem sabe, sabe
        res = 5.0;
    } else {
        res = a - b;
    }
    printf("[DEBUG math.dll]: subtrair_em_c retorno | result = %f\n", res);
    fflush(stdout);
    return res;
}

EXPORT double multiplicar_em_c(double a, double b) {
    printf("[DEBUG math.dll]: multiplicar_em_c recebido | a = %f, b = %f\n", a, b);
    fflush(stdout);
    double res = a * b;
    printf("[DEBUG math.dll]: multiplicar_em_c retorno | result = %f\n", res);
    fflush(stdout);
    return res;
}

EXPORT double dividir_em_c(double a, double b) {
    printf("[DEBUG math.dll]: dividir_em_c recebido | a = %f, b = %f\n", a, b);
    fflush(stdout);
    double res;
    if (b == 0.0) {
        res = 124123.2314;
    }
    else {
        res = a / b;
    }
    printf("[DEBUG math.dll]: dividir_em_c retorno | result = %f\n", res);
    fflush(stdout);
    return res;
}

EXPORT int resto_em_c(int a, int b) {
    printf("[DEBUG math.dll]: resto_em_c recebido | a = %d, b = %d\n", a, b);
    fflush(stdout);
    int res;
    if (b == 0) {
        res = 124123;
    }
    else {
        res = a % b;
    }
    printf("[DEBUG math.dll]: resto_em_c retorno | result = %d\n", res);
    fflush(stdout);
    return res;
}

EXPORT double modulo_em_c(double a) {
    printf("[DEBUG math.dll]: modulo_em_c recebido | a = %f\n", a);
    fflush(stdout);
    double res = (a >= 0) ? a : -a;
    printf("[DEBUG math.dll]: modulo_em_c retorno | result = %f\n", res);
    fflush(stdout);
    return res;
}

EXPORT double potencia_em_c(double a, double b) {
    printf("[DEBUG math.dll]: potencia_em_c recebido | a = %f, b = %f\n", a, b);
    fflush(stdout);
    double res;
    if (a == 0.0) res = 0.0;
    else if (b == 0.0) res = 1.0;
    else if (a < 0.0) res = 124123.2314;
    else res = exp_em_c(b * ln_em_c(a));

    printf("[DEBUG math.dll]: potencia_em_c retorno | result = %f\n", res);
    fflush(stdout);
    return res;
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
    printf("[DEBUG math.dll]: log_em_c recebido | a = %f, b = %f\n", a, b);
    fflush(stdout);
    double res;
    if (b <= 0.0 || a <= 0.0 || a == 1.0) res = 124123.2314;
    else res = ln_em_c(b) / ln_em_c(a);

    printf("[DEBUG math.dll]: log_em_c retorno | result = %f\n", res);
    fflush(stdout);
    return res;
}


//Lógica de troca de base

EXPORT double troca_de_base_em_c(double a, int b, int c) {
    printf("[DEBUG math.dll]: troca_de_base_em_c recebido | a = %f, b = %d, c = %d\n", a, b, c);
    fflush(stdout);
    long long dec_int_part = 0, int_part = 0, multiplicador = 1;
    double frac_part = 0, val_base_10 = 0;
    int is_negative = 0, digit, i = 12;


    if (a < 0.0) {
        is_negative = 1;
        a = -a;
    }

    int_part = (long long)a;
    frac_part = a - int_part;

    //Converte para a base 10 ex.: 1010 = 10
    while (int_part > 0) {
        digit = int_part % 10;
        val_base_10 += digit * multiplicador;
        multiplicador *= b;
        int_part /= 10;
    }

    double frac_multiplier = 1.0 / b;
    while (frac_part > 1e-9 && i > 0) {
        frac_part *= 10.0;
        digit = (int)frac_part;
        val_base_10 += digit * frac_multiplier;
        frac_part -= digit;
        frac_multiplier /= b;
        i--;
    }

    double res;

    if (c == 10) {
        if (is_negative == 0) {
            res = val_base_10;
        }
        else {
            res = -val_base_10;
        }
    }

    //base10 para base n
    else {
        dec_int_part = (long long)val_base_10;
        double dec_frac_part = val_base_10 - dec_int_part;

        double result = 0.0;
        long long res_multiplier = 1;

        // Converte a parte inteira para base_b
        while (dec_int_part > 0) {
            digit = dec_int_part % c;
            result += digit * res_multiplier;
            res_multiplier *= 10;
            dec_int_part /= c;
        }

        // Converte a parte fracionária para base_b
        double res_divisor = 10.0;
        i = 11;
        while (dec_frac_part > 1e-9 && i > 0) {
            dec_frac_part *= c;
            digit = (int)dec_frac_part;
            result += (double)digit / res_divisor;
            dec_frac_part -= digit;
            res_divisor *= 10.0;
            i--;
        }
        res = is_negative ? -result : result;
    }

    printf("[DEBUG math.dll]: troca_de_base_em_c retorno | result = %f\n", res);
    fflush(stdout);
    return res;
}


//logica rand
EXPORT char* rand_em_c(int a, int b) {
    printf("[DEBUG math.dll]: rand_em_c recebido | a = %d, b = %d\n", a, b);
    fflush(stdout);
    int tamanho = a;
    int tipo = b;
    //Tipo (b):
    // 0 -> numeros apenas
    // 1 -> letras apenas
    // 2 -> numeros e letras minusculas
    // 3 -> numeros e letras
    // 4 -> numeros, letras e símbolos
    if (tamanho <= 0) {
        printf("[DEBUG math.dll]: rand_em_c retorno | result = \"\"\n");
        fflush(stdout);
        return "";
    }

    const char *nums = "0123456789";
    const char *minúsculas = "abcdefghijklmnopqrstuvwxyz";
    const char *maiúsculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const char *simbolos = "!@#$%^&*()_+-=[]{}|;:,.<>?";


    char pool[200] = "";

    if (tipo == 0) {
        strcat(pool, nums);
    } else if (tipo == 1) {
        strcat(pool, minúsculas);
        strcat(pool, maiúsculas);
    } else if (tipo == 2) {
        strcat(pool, nums);
        strcat(pool, minúsculas);
    } else if (tipo == 3) {
        strcat(pool, nums);
        strcat(pool, minúsculas);
        strcat(pool, maiúsculas);
    } else if (tipo == 4) {
        strcat(pool, nums);
        strcat(pool, minúsculas);
        strcat(pool, maiúsculas);
        strcat(pool, simbolos);
    } else {
        printf("[DEBUG math.dll]: rand_em_c retorno | result = 124123\n");
        fflush(stdout);
        return "124123";
    }

    int pool_len = strlen(pool);

    char *resultado = (char *)malloc((tamanho + 1) * sizeof(char));
    if (!resultado) {
        printf("[DEBUG math.dll]: rand_em_c retorno | result = NULL\n");
        fflush(stdout);
        return NULL;
    }

    for (int i = 0; i < tamanho; i++) {
        resultado[i] = pool[rand() % pool_len];
    }
    resultado[tamanho] = '\0';

    printf("[DEBUG math.dll]: rand_em_c retorno | result = %s\n", resultado);
    fflush(stdout);
    return resultado;
}