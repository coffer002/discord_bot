import discord
from discord.ext import commands
import ctypes
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

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


@bot.command()
async def somar(ctx, a: float, b: float):
    print(f"somando {a} e {b}")
    resultado = math_c.somar_em_c(ctypes.c_double(a), ctypes.c_double(b))
    await ctx.send(f"Calculado: a soma de {a} e {b} é: **{resultado}**")

@bot.command()
async def multiplicar(ctx, a: float, b: float):
    resultado = math_c.multiplicar_em_c(ctypes.c_double(a), ctypes.c_double(b))
    await ctx.send(f"Calculado: a multiplicação de {a} e {b} é: **{resultado}**")

@bot.command()
async def dividir(ctx, a: float, b: float):
    if b != 0:
        resultado = math_c.dividir_em_c(ctypes.c_double(a), ctypes.c_double(b))
        await ctx.send(f"Calculado: a divisão de {a} por {b} é: **{resultado}**")
    else:
        await ctx.send("Erro matemático: divisão por zero")

@bot.command()
async def resto(ctx, a: int, b: int):
    resultado = math_c.resto_em_c(ctypes.c_int(a), ctypes.c_int(b))
    await ctx.send(f"Calculado: o resto da divisão de {a} por {b} é: **{resultado}**")

@bot.command()
async def modulo(ctx, a: float):
    resultado = math_c.modulo_em_c(ctypes.c_double(a))
    await ctx.send(f"Calculado: o módulo de {a} é: **{resultado}**")

@bot.command()
async def potencia(ctx, a: float, b: int):
    resultado = math_c.potencia_c(ctypes.c_double(a), ctypes.c_int(b))
    await ctx.send(f"Calculado: a potência de {a} elevado a {b} é: **{resultado}**")

@bot.command()
async def log(ctx, a: float, b: float):
    resultado = math_c.log_em_c(ctypes.c_double(a), ctypes.c_double(b))
    if resultado == -1.0:
         await ctx.send("Erro matemático: A base deve ser > 0 e ≠ 1. O logaritmando deve ser > 0.")
    else:
         await ctx.send(f"Calculado: o log de {b} na base {a} é: **{resultado:.4f}**")

@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online')

token = os.getenv('DISCORD_TOKEN')
bot.run(token)