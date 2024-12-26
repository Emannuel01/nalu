from flask import Blueprint, jsonify, request, render_template
from db import get_db_connection
from datetime import datetime

agendamento_bp = Blueprint('agendamento', __name__)

@agendamento_bp.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT agendamentos.*, pacientes.nome AS paciente_nome, medicos.nome AS medico_nome,
        DATE_FORMAT(agendamentos.data, '%d/%m/%Y %H:%i') AS data_formatada
        FROM agendamentos
        JOIN pacientes ON agendamentos.paciente_id = pacientes.id
        JOIN medicos ON agendamentos.medico_id = medicos.id;
    """)
    agendamentos = cursor.fetchall()
    conn.close()
    return jsonify(agendamentos)

@agendamento_bp.route('/agendamentos', methods=['POST'])
def create_agendamento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica se o valor da data está no formato correto
    try:
        data_agendamento = datetime.strptime(data['data'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use o formato YYYY-MM-DD HH:MM:SS."}), 400

    # Verifica se o horário está dentro do horário de trabalho dos médicos
    if not (8 <= data_agendamento.hour < 16):
        return jsonify({"message": "Os médicos só trabalham das 8h às 16h."}), 400

    # Verifica se já existe um agendamento para o mesmo médico no mesmo horário
    cursor.execute(
        "SELECT * FROM agendamentos WHERE medico_id = %s AND data = %s",
        (data['medico_id'], data_agendamento)
    )
    existing_agendamento = cursor.fetchone()
    if existing_agendamento:
        return jsonify({"message": "Já existe um agendamento para este médico neste horário."}), 400

    cursor.execute(
        "INSERT INTO agendamentos (paciente_id, medico_id, consulta_id, data, status) VALUES (%s, %s, %s, %s, %s)",
        (data['paciente_id'], data['medico_id'], data['consulta_id'], data_agendamento, 'pendente')
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Agendamento criado com sucesso"}), 201

@agendamento_bp.route('/agendamentos/<int:id>', methods=['GET'])
def get_agendamento(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agendamentos WHERE id = %s;", (id,))
    agendamento = cursor.fetchone()
    conn.close()
    if agendamento:
        return jsonify(agendamento)
    else:
        return jsonify({"message": "Agendamento não encontrado."}), 404

@agendamento_bp.route('/agendamentos/<int:id>', methods=['PUT'])
def update_agendamento(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica se o valor da data está no formato correto
    try:
        data_agendamento = datetime.strptime(data['data'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use o formato YYYY-MM-DD HH:MM:SS."}), 400

    # Verifica se o horário está dentro do horário de trabalho dos médicos
    if not (8 <= data_agendamento.hour < 16):
        return jsonify({"message": "Os médicos só trabalham das 8h às 16h."}), 400

    # Verifica se já existe um agendamento para o mesmo médico no mesmo horário
    cursor.execute(
        "SELECT * FROM agendamentos WHERE medico_id = %s AND data = %s AND id != %s",
        (data['medico_id'], data_agendamento, id)
    )
    existing_agendamento = cursor.fetchone()
    if existing_agendamento:
        return jsonify({"message": "Já existe um agendamento para este médico neste horário."}), 400

    cursor.execute(
        "UPDATE agendamentos SET paciente_id = %s, medico_id = %s, consulta_id = %s, data = %s, status = %s WHERE id = %s",
        (data['paciente_id'], data['medico_id'], data['consulta_id'], data_agendamento, data['status'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Agendamento atualizado com sucesso"})

@agendamento_bp.route('/agendamentos/<int:id>', methods=['DELETE'])
def delete_agendamento(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamentos WHERE id = %s;", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Agendamento deletado com sucesso"})

@agendamento_bp.route('/agendamentos/disponiveis', methods=['GET'])
def get_horarios_disponiveis():
    medico_id = request.args.get('medico_id')
    data = request.args.get('data')

    if not medico_id or not data:
        return jsonify({"message": "Médico e data são obrigatórios."}), 400

    try:
        data_agendamento = datetime.strptime(data, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use o formato YYYY-MM-DD."}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Busca os horários já agendados para o médico na data especificada
    cursor.execute(
        "SELECT TIME(data) AS horario FROM agendamentos WHERE medico_id = %s AND DATE(data) = %s",
        (medico_id, data_agendamento)
    )
    agendamentos = cursor.fetchall()
    conn.close()

    # Gera a lista de horários disponíveis (8h às 16h, a cada 30 minutos)
    horarios_disponiveis = []
    for hora in range(8, 16):
        for minuto in [0, 30]:
            horario = datetime(data_agendamento.year, data_agendamento.month, data_agendamento.day, hora, minuto)
            if not any(agendamento['horario'] == horario.time() for agendamento in agendamentos):
                horarios_disponiveis.append(horario.strftime('%H:%M'))

    return jsonify(horarios_disponiveis)