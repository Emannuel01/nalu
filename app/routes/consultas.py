from flask import Blueprint, jsonify, request
from db import get_db_connection
from datetime import datetime

consultas_bp = Blueprint('consultas', __name__)

@consultas_bp.route('/consultas', methods=['GET'])
def get_consultas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT consultas.*, pacientes.nome AS paciente_nome, medicos.nome AS medico_nome,
        DATE_FORMAT(consultas.data, '%d/%m/%Y %H:%i') AS data_formatada
        FROM consultas
        JOIN pacientes ON consultas.paciente_id = pacientes.id
        JOIN medicos ON consultas.medico_id = medicos.id;
        LEFT JOIN pagamentos ON consultas.id = pagamentos.consulta_id
    """)
    consultas = cursor.fetchall()
    conn.close()
    return jsonify(consultas)

@consultas_bp.route('/consultas', methods=['POST'])
def create_consulta():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica se o valor da data está no formato correto
    try:
        data_consulta = datetime.strptime(data['data'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"message": "Formato de data inválido. Use o formato YYYY-MM-DD HH:MM:SS."}), 400

    cursor.execute(
        "INSERT INTO consultas (paciente_id, medico_id, data, diagnostico, prescricao) VALUES (%s, %s, %s, %s, %s)",
        (int(data['paciente_id']), int(data['medico_id']), data_consulta, data.get('diagnostico'), data.get('prescricao'))
    )
    consulta_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO pagamentos (consulta_id, valor, tipo_pagamento, status) VALUES (%s, %s, %s, %s)",
        (consulta_id, data['valor'], data['tipo_pagamento'], 'pendente')
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Consulta criada com sucesso"}), 201

@consultas_bp.route('/consultas/<int:id>', methods=['GET'])
def get_consulta(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM consultas WHERE id = %s;", (id,))
    consulta = cursor.fetchone()
    conn.close()
    if consulta:
        return jsonify(consulta)
    else:
        return jsonify({"message": "Consulta não encontrada."}), 404

@consultas_bp.route('/consultas/<int:id>', methods=['PUT'])
def update_consulta(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE consultas SET paciente_id = %s, medico_id = %s, data = %s, diagnostico = %s, prescricao = %s WHERE id = %s",
        (data['paciente_id'], data['medico_id'], data['data'], data.get('diagnostico'), data.get('prescricao'), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Consulta atualizada com sucesso"})

@consultas_bp.route('/consultas/<int:id>', methods=['DELETE'])
def delete_consulta(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM consultas WHERE id = %s;", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Consulta deletada com sucesso"})

