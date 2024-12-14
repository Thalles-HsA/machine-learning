# Usar uma imagem Python leve
FROM python:3.9-slim

# Configurar o diretório de trabalho no container
WORKDIR /app

# Copiar apenas o arquivo de dependências primeiro (para cache)
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código do projeto
COPY ./src /app/src

# Comando padrão para executar
CMD ["python", "/app/src/main.py"]
