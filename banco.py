import mysql.connector
from datetime import datetime, timedelta

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="seu_usuario",
        password="sua_senha",
        database="sua_base_de_dados"
    )

def generate_horarios(medico_id, start_date, end_date):
    horarios = []
    current_date = start_date
    while current_date <= end_date:
        for hour in range(8, 16):  # Horário de trabalho das 8h às 16h
            for minute in [0, 30]:  # Intervalos de 30 minutos
                horario = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                horarios.append(horario)
        current_date += timedelta(days=1)
    return horarios

def insert_horarios(medico_id, horarios):
    conn = get_db_connection()
    cursor = conn.cursor()
    for horario in horarios:
        cursor.execute(
            "INSERT INTO agendamentos (paciente_id, medico_id, consulta_id, data, status) VALUES (%s, %s, %s, %s, %s)",
            (None, medico_id, None, horario, 'pendente')
        )
    conn.commit()
    conn.close()

def main():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM medicos")
    medicos = cursor.fetchall()
    conn.close()

    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)  # Gera horários para os próximos 30 dias

    for medico in medicos:
        medico_id = medico['id']
        horarios = generate_horarios(medico_id, start_date, end_date)
        insert_horarios(medico_id, horarios)
        print(f"Horários gerados para o médico ID {medico_id}")

if __name__ == "__main__":
    main()