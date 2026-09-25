FROM python:3.11-slim

# Instala o GCC para compilar a biblioteca C no Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt-get/lists/*

WORKDIR /app

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia as pastas de C e Python mantendo a estrutura de diretórios
COPY C/ ./C/
COPY Python/ ./Python/

# Cria a pasta de build e compila o library.c diretamente em .so
RUN mkdir -p /app/C/bot_engine_math/cmake-build-debug
RUN gcc -shared -fPIC -o /app/C/bot_engine_math/cmake-build-debug/libbot_engine_math.so /app/C/bot_engine_math/library.c

# Define o diretório de trabalho onde o main.py reside
WORKDIR /app/Python/discord_bot

CMD ["python", "main.py"]