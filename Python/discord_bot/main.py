import discord
from discord.ext import commands
import ctypes
import os
import re
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import math

print("DEBUG: Iniciando carregamento do bot e variáveis de ambiente...")
load_dotenv(find_dotenv())

raiz = Path(__file__).parent.parent.parent
path_math_c = raiz / "C" / "bot_engine_math" / "cmake-build-debug" / "libbot_engine_math.dll"

print(f"DEBUG: Carregando biblioteca C no caminho: {path_math_c}")
math_c = ctypes.CDLL(path_math_c)

print("DEBUG: Configurando tipos de retorno da DLL...")
math_c.somar_em_c.restype = ctypes.c_double
math_c.multiplicar_em_c.restype = ctypes.c_double
math_c.dividir_em_c.restype = ctypes.c_double
math_c.resto_em_c.restype = ctypes.c_double
math_c.modulo_em_c.restype = ctypes.c_double
math_c.potencia_c.restype = ctypes.c_double
math_c.log_em_c.restype = ctypes.c_double

print("DEBUG: Configurando Intents do Discord...")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

constantes = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
    "fi": 1.618033988749895,
    "phi": 1.618033988749895,
    "tau": 6.283185307179586,
}

def parse_constante(valor: str) -> float:
    print(f"DEBUG: Analisando possível constante ou número: {valor}")
    num = valor.lower().strip()
    if num in constantes:
        print(f"DEBUG: Constante encontrada: {num} = {constantes[num]}")
        return constantes[num]
    print(f"DEBUG: Convertendo valor para float: {valor}")
    return float(valor)

async def processar_comando_math(channel, operacao: str, args: list):
    print(f"DEBUG: Iniciando processar_comando_math | Operacao: {operacao} | Args: {args}")
    try:
        if operacao == "somar":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            print(f"DEBUG: Executando função em C: somar_em_c({val_a}, {val_b})")
            resultado = math_c.somar_em_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
            print(f"DEBUG: Operação somar concluída. Resultado: {resultado}")
            await channel.send(f"Calculado: a soma de {a} e {b} é: **{resultado:.10f}**")

        elif operacao == "multiplicar":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            print(f"DEBUG: Executando função em C: multiplicar_em_c({val_a}, {val_b})")
            resultado = math_c.multiplicar_em_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
            print(f"DEBUG: Operação multiplicar concluída. Resultado: {resultado}")
            await channel.send(f"Calculado: a multiplicação de {a} e {b} é: **{resultado:.10f}**")

        elif operacao == "dividir":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            print(f"DEBUG: Verificando divisão por zero para: {val_a} / {val_b}")
            if val_b != 0:
                print(f"DEBUG: Executando função em C: dividir_em_c({val_a}, {val_b})")
                resultado = math_c.dividir_em_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
                print(f"DEBUG: Operação dividir concluída. Resultado: {resultado}")
                await channel.send(f"Calculado: a divisão de {a} por {b} é: **{resultado:.10f}**")
            else:
                print("DEBUG: Divisão por zero interceptada.")
                await channel.send("Erro matemático: divisão por zero")

        elif operacao == "resto":
            a, b = args[0], args[1]
            val_a, val_b = int(parse_constante(a)), int(parse_constante(b))
            print(f"DEBUG: Executando função em C: resto_em_c({val_a}, {val_b})")
            resultado = math_c.resto_em_c(ctypes.c_int(val_a), ctypes.c_int(val_b))
            print(f"DEBUG: Operação resto concluída. Resultado: {resultado}")
            await channel.send(f"Calculado: o resto da divisão de {a} por {b} é: **{resultado:.10f}**")

        elif operacao == "modulo":
            a = args[0]
            val_a = parse_constante(a)
            print(f"DEBUG: Executando função em C: modulo_em_c({val_a})")
            resultado = math_c.modulo_em_c(ctypes.c_double(val_a))
            print(f"DEBUG: Operação modulo concluída. Resultado: {resultado}")
            await channel.send(f"Calculado: o módulo de {a} é: **{resultado:.10f}**")

        elif operacao == "potencia":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            print(f"DEBUG: Executando função em C: potencia_c({val_a}, {val_b})")
            resultado = math_c.potencia_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
            print(f"DEBUG: Operação potencia concluída. Resultado: {resultado}")
            await channel.send(f"Calculado: a potência de {a} elevado a {b} é: **{resultado:.10f}**")

        elif operacao == "raiz":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            val_c = 1 / val_b
            print(f"DEBUG: Executando função em C: potencia_c({val_a}, {val_c}), onde {val_c} = 1 / {val_b}")
            resultado = math_c.potencia_c(ctypes.c_double(val_a), ctypes.c_double(val_c))
            print(f"DEBUG: Operação potencia concluída. Resultado: {resultado}")
            await channel.send(f"Calculado: a raiz {b}-ésima de {a} é: **{resultado:.10f}**")

        elif operacao == "sqrt":
            a = args[0]
            val_a = parse_constante(a)
            val_b = 2
            val_c = 1 / val_b
            print(f"DEBUG: Executando função em C: potencia_c({val_a}, {val_c}), onde {val_c} = 1 / {val_b}")
            resultado = math_c.potencia_c(ctypes.c_double(val_a), ctypes.c_double(val_c))
            print(f"DEBUG: Operação potencia concluída. Resultado: {resultado}")
            await channel.send(f"Calculado: a raiz quadrada de {a} é: **{resultado:.10f}**")

        elif operacao == "cbrt":
            a = args[0]
            val_a = parse_constante(a)
            val_b = 3
            val_c = 1 / val_b
            print(f"DEBUG: Executando função em C: potencia_c({val_a}, {val_c}), onde {val_c} = 1 / {val_b}")
            resultado = math_c.potencia_c(ctypes.c_double(val_a), ctypes.c_double(val_c))
            print(f"DEBUG: Operação potencia concluída. Resultado: {resultado}")
            await channel.send(f"Calculado: a raiz cubica de {a} é: **{resultado:.10f}**")


        elif operacao == "log":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            print(f"DEBUG: Executando função em C: log_em_c({val_a}, {val_b})")
            resultado = math_c.log_em_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
            print(f"DEBUG: Operação log concluída. Resultado: {resultado}")
            if resultado == -1.0:
                print("DEBUG: Erro de restrição matemática retornado pela função log_em_c.")
                await channel.send("Erro matemático: A base deve ser > 0 e ≠ 1. O logaritmando deve ser > 0.")
            else:
                await channel.send(f"Calculado: o log de {b} na base {a} é: **{resultado:.10f}**")

        elif operacao == "ln":
            a = args[0]
            val_a = parse_constante(a)
            val_e = constantes["e"]
            print(f"DEBUG: Executando função em C para ln: log_em_c({val_e}, {val_a})")
            resultado = math_c.log_em_c(ctypes.c_double(val_e), ctypes.c_double(val_a))
            print(f"DEBUG: Operação ln concluída. Resultado: {resultado}")
            if resultado == -1.0:
                print("DEBUG: Erro de restrição matemática retornado pela função log_em_c (ln).")
                await channel.send("Erro matemático: O logaritmando deve ser > 0.")
            else:
                await channel.send(f"Calculado: o ln de {a} é: **{resultado:.10f}**")
        elif operacao == "exp":
            a = args[0]
            val_a = parse_constante(a)
            val_e = constantes["e"]
            print(f"DEBUG: Executando função em C para exp(x): potencia_c({val_e}, {val_a})")
            resultado = math_c.potencia_c(ctypes.c_double(val_e), ctypes.c_double(val_a))
            print(f"DEBUG: Operação exp(x) concluída. Resultado: {resultado}")
            await channel.send(f"Calculado: o exp({a}) é: **{resultado:.10f}**")

    except ValueError:
        print("DEBUG: Exceção ValueError detectada. Entradas não podiam ser convertidas.")
        await channel.send("Erro: Entrada inválida. Forneça números ou constantes válidas.")

@bot.command()
async def somar(ctx, a: str, b: str):
    print(f"DEBUG: Comando prefixado '!somar' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "somar", [a, b])

@bot.command()
async def multiplicar(ctx, a: str, b: str):
    print(f"DEBUG: Comando prefixado '!multiplicar' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "multiplicar", [a, b])

@bot.command()
async def dividir(ctx, a: str, b: str):
    print(f"DEBUG: Comando prefixado '!dividir' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "dividir", [a, b])

@bot.command()
async def resto(ctx, a: str, b: str):
    print(f"DEBUG: Comando prefixado '!resto' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "resto", [a, b])

@bot.command()
async def modulo(ctx, a: str):
    print(f"DEBUG: Comando prefixado '!modulo' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "modulo", [a])

@bot.command()
async def potencia(ctx, a: str, b: str):
    print(f"DEBUG: Comando prefixado '!potencia' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "potencia", [a, b])

@bot.command()
async def raiz(ctx, a: str, b: str):
    print(f"DEBUG: Comando prefixado '!raiz' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "raiz", [a, b])

@bot.command()
async def sqrt(ctx, a: str):
    print(f"DEBUG: Comando prefixado '!sqrt' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "sqrt", [a])

@bot.command()
async def cbrt(ctx, a: str):
    print(f"DEBUG: Comando prefixado '!cbrt' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "cbrt", [a])


@bot.command()
async def log(ctx, a: str, b: str):
    print(f"DEBUG: Comando prefixado '!log' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "log", [a, b])

@bot.command()
async def ln(ctx, a: str):
    print(f"DEBUG: Comando prefixado '!ln' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "ln", [a])

@bot.command()
async def exp(ctx, a: str):
    print(f"DEBUG: Comando prefixado '!exp' invocado no canal {ctx.channel.id}")
    await processar_comando_math(ctx.channel, "exp", [a])

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"DEBUG: Lendo mensagem capturada: '{message.content}'")

    await bot.process_commands(message)

    if not message.content.startswith('!'):
        conteudo = message.content.lower()
        print("DEBUG: Verificando padrões regex na mensagem natural...")

        operadores_simbolos = {
            '+': 'somar',
            '*': 'multiplicar',
            '/': 'dividir',
            '%': 'resto',
            '^': 'potencia'
        }

        match_simbolo = re.search(r'([-+]?[a-z0-9.]+)\s*(\+|\*|\/|\%|\^)\s*([-+]?[a-z0-9.]+)', conteudo)
        if match_simbolo:
            a, op, b = match_simbolo.groups()
            cmd = operadores_simbolos[op]
            print(f"DEBUG: Padrão de símbolo matemático detectado. Operação: {cmd} ({op}), Args: [{a}, {b}]")
            await processar_comando_math(message.channel, cmd, [a, b])
            return

        match_2_args = re.search(r'\b(somar|multiplicar|dividir|resto|potencia|log|raiz)\s+([^\s]+)\s+([^\s]+)', conteudo)
        if match_2_args:
            cmd, a, b = match_2_args.groups()
            print(f"DEBUG: Padrão de 2 argumentos por texto detectado. Comando: {cmd}, Args: [{a}, {b}]")
            await processar_comando_math(message.channel, cmd, [a, b])
            return

        match_1_arg = re.search(r'\b(modulo|ln|exp|sqrt|cbrt)\s+([^\s]+)', conteudo)
        if match_1_arg:
            cmd, a = match_1_arg.groups()
            print(f"DEBUG: Padrão de 1 argumento por texto detectado. Comando: {cmd}, Arg: [{a}]")
            await processar_comando_math(message.channel, cmd, [a])
            return

@bot.event
async def on_ready():
    print(f"DEBUG: O bot {bot.user} conectou e está com status on_ready.")
    print(f'Bot {bot.user} está online')

token = os.getenv('DISCORD_TOKEN')
print("DEBUG: Executando bot.run()...")
bot.run(token)