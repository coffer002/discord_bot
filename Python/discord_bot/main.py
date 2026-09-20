import discord
from discord.ext import commands
import ctypes
import os
import re
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import math

load_dotenv(find_dotenv())

raiz = Path(__file__).parent.parent.parent
path_math_c = raiz / "C" / "bot_engine_math" / "cmake-build-debug" / "libbot_engine_math.dll"
math_c = ctypes.CDLL(path_math_c)

# Definindo o tipo do retorno das funções da DLL para double (float em C)
math_c.somar_em_c.restype = ctypes.c_double
math_c.multiplicar_em_c.restype = ctypes.c_double
math_c.dividir_em_c.restype = ctypes.c_double
math_c.resto_em_c.restype = ctypes.c_double
math_c.modulo_em_c.restype = ctypes.c_double
math_c.potencia_c.restype = ctypes.c_double
math_c.log_em_c.restype = ctypes.c_double

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
    num = valor.lower().strip()
    if num in constantes:
        return constantes[num]
    return float(valor)


async def processar_comando_math(channel, operacao: str, args: list):
    try:
        if operacao == "somar":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            resultado = math_c.somar_em_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
            await channel.send(f"Calculado: a soma de {a} e {b} é: **{resultado}**")

        elif operacao == "multiplicar":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            resultado = math_c.multiplicar_em_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
            await channel.send(f"Calculado: a multiplicação de {a} e {b} é: **{resultado}**")

        elif operacao == "dividir":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            if val_b != 0:
                resultado = math_c.dividir_em_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
                await channel.send(f"Calculado: a divisão de {a} por {b} é: **{resultado}**")
            else:
                await channel.send("Erro matemático: divisão por zero")

        elif operacao == "resto":
            a, b = args[0], args[1]
            val_a, val_b = int(parse_constante(a)), int(parse_constante(b))
            resultado = math_c.resto_em_c(ctypes.c_int(val_a), ctypes.c_int(val_b))
            await channel.send(f"Calculado: o resto da divisão de {a} por {b} é: **{resultado}**")

        elif operacao == "modulo":
            a = args[0]
            val_a = parse_constante(a)
            resultado = math_c.modulo_em_c(ctypes.c_double(val_a))
            await channel.send(f"Calculado: o módulo de {a} é: **{resultado}**")

        elif operacao == "potencia":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            resultado = math_c.potencia_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
            await channel.send(f"Calculado: a potência de {a} elevado a {b} é: **{resultado}**")

        elif operacao == "log":
            a, b = args[0], args[1]
            val_a, val_b = parse_constante(a), parse_constante(b)
            resultado = math_c.log_em_c(ctypes.c_double(val_a), ctypes.c_double(val_b))
            if resultado == -1.0:
                await channel.send("Erro matemático: A base deve ser > 0 e ≠ 1. O logaritmando deve ser > 0.")
            else:
                await channel.send(f"Calculado: o log de {b} na base {a} é: **{resultado:.4f}**")

    except ValueError:
        await channel.send("Erro: Entrada inválida. Forneça números ou constantes válidas.")


@bot.command()
async def somar(ctx, a: str, b: str):
    await processar_comando_math(ctx.channel, "somar", [a, b])

@bot.command()
async def multiplicar(ctx, a: str, b: str):
    await processar_comando_math(ctx.channel, "multiplicar", [a, b])

@bot.command()
async def dividir(ctx, a: str, b: str):
    await processar_comando_math(ctx.channel, "dividir", [a, b])

@bot.command()
async def resto(ctx, a: str, b: str):
    await processar_comando_math(ctx.channel, "resto", [a, b])

@bot.command()
async def modulo(ctx, a: str):
    await processar_comando_math(ctx.channel, "modulo", [a])

@bot.command()
async def potencia(ctx, a: str, b: str):
    await processar_comando_math(ctx.channel, "potencia", [a, b])

@bot.command()
async def log(ctx, a: str, b: str):
    await processar_comando_math(ctx.channel, "log", [a, b])


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if not message.content.startswith('!'):
        conteudo = message.content.lower()

        match_2_args = re.search(r'\b(somar|multiplicar|dividir|resto|potencia|log)\s+([^\s]+)\s+([^\s]+)', conteudo)
        if match_2_args:
            cmd, a, b = match_2_args.groups()
            await processar_comando_math(message.channel, cmd, [a, b])
            return

        # Regex para capturar comando de 1 argumento (ex: "modulo -15")
        match_1_arg = re.search(r'\b(modulo)\s+([^\s]+)', conteudo)
        if match_1_arg:
            cmd, a = match_1_arg.groups()
            await processar_comando_math(message.channel, cmd, [a])
            return

@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online')

token = os.getenv('DISCORD_TOKEN')
bot.run(token)