from flask import Blueprint, jsonify, request, render_template
from db import get_db_connection

medicos_bp = Blueprint('medicos', __name__)


@medicos_bp.route('/medicos', methods=['GET'])
def get_medicos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicos;")
    medicos = cursor.fetchall()
    conn.close()
    return jsonify(medicos)

@medicos_bp.route('/medicos', methods=['POST'])
def create_medico():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medicos (nome, especialidade, horario_atendimento, email) VALUES (%s, %s, %s, %s)",
        (data['nome'], data['especialidade'], data.get('horario_atendimento'), data['email'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Médico criado com sucesso"}), 201

@medicos_bp.route('/medicos/<int:medico_id>/horarios', methods=['GET'])
def get_medico_horarios(medico_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT horario_atendimento FROM medicos WHERE id = %s;", (medico_id,))
    horarios = cursor.fetchone()
    conn.close()
    if horarios:
        return jsonify(horarios)
    else:
        return jsonify({"error": "Médico não encontrado"}), 404


@medicos_bp.route('/medicos/<int:medico_id>', methods=['DELETE'])
def delete_medico(medico_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicos WHERE id = %s;", (medico_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({"message": "Médico deletado com sucesso"}), 200
    else:
        return jsonify({"error": "Médico não encontrado"}), 404
    

@medicos_bp.route('/medicos/<int:medico_id>', methods=['PUT'])
def update_medico(medico_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE medicos SET nome = %s, especialidade = %s, horario_atendimento = %s, telefone = %s, email = %s WHERE id = %s",
        (data['nome'], data['especialidade'], data.get('horario_atendimento'), data['telefone'], data['email'], medico_id)
    )
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({"message": "Médico atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Médico não encontrado"}), 404
    


@medicos_bp.route('/medicos/<int:medico_id>', methods=['GET'])
def get_medico(medico_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicos WHERE id = %s;", (medico_id,))
    medico = cursor.fetchone()
    conn.close()
    if medico:
        return jsonify(medico)
    else:
        return jsonify({"error": "Médico não encontrado"}), 404