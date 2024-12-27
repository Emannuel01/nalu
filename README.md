# Comandos para Iniciar o Projeto

## Iniciar com Docker

Para executar utilizando Docker Compose com o banco configurado, use o comando:

```sh
docker-compose up --build
```

## Iniciar com Python

Para executar diretamente na máquina, rode os seguintes comandos. Lembre-se de que o banco de dados precisa estar rodando.

```sh
cd /app
pip install --no-cache-dir -r requirements.txt
python app.py
```

## Acesso ao Aplicativo

Após a execução, acesse o aplicativo pelo link:

[http://localhost:5000/app/home](http://localhost:5000/app/home)