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

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)



@bot.command()
async def somar(ctx, a: int, b: int):
    resultado = math_c.somar_em_c(a, b)
    await ctx.send(f"Calculado: a soma de {a} e {b} é: **{resultado}**")

@bot.command()
async def multiplicar(ctx, a: int, b: int):
    resultado = math_c.multiplicar_em_c(a, b)
    await ctx.send(f"Calculado: a multiplicação de {a} e {b} é: **{resultado}**")

@bot.command()
async def dividir(ctx, a: int, b: int):
    resultado = math_c.dividir_em_c(a, b)
    await ctx.send(f"Calculado: a divisão de {a} por {b} é: **{resultado}**")

@bot.command()
async def resto(ctx, a: int, b: int):
    resultado = math_c.resto_em_c(a, b)
    await ctx.send(f"Calculado: o resto da divisão de {a} por {b} é: **{resultado}**")

@bot.command()
async def potencia(ctx, a: int, b: int):
    resultado = math_c.potencia_c(a, b)
    await ctx.send(f"Calculado: a potência de {a} elevado a {b} é: **{resultado}**")

@bot.event
async def on_ready():
    print(f'Bot {bot.user} está online')

token = os.getenv('DISCORD_TOKEN')
bot.run(token)