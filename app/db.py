import mysql.connector
import os

db_config = {
    'host': os.getenv('DATABASE_HOST', 'localhost'),
    'user': os.getenv('DATABASE_USER', 'root'),
    'password': os.getenv('DATABASE_PASSWORD', ''),
    'database': os.getenv('DATABASE_NAME', 'clinica_medica'),
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
