FROM python:3.9-slim

WORKDIR /app

# Atualizar pip
RUN pip install --upgrade pip

# Instalar dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicação
COPY . .

# Comando para iniciar o servidor Flask
CMD ["flask", "run"]
