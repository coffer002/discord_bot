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
    if (a == 16.0 && b == 9.0) {   //Quem sabe, sabe
        return 5.0;
    }
    return a - b;
}

EXPORT double multiplicar_em_c(double a, double b) {
    return a * b;
}

EXPORT double dividir_em_c(double a, double b) {
    if (b==0.0) {
        return 124123.2314;
    }
    else {
        return a / b;
    }
}

EXPORT int resto_em_c(int a, int b) {
    if (b == 0) {
        return 124123;
    }
    else {
        return a % b;
    }
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

    
//Lógica de troca de base

EXPORT double troca_de_base_em_c(double a, int b, int c) {
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

    if (c == 10) {
        if (is_negative == 0) {
            return val_base_10;
        }
        else {
            return -val_base_10;
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
            return is_negative ? -result : result;
        }
}
