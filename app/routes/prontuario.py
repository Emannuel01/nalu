from flask import Blueprint, jsonify, request
from db import get_db_connection
import mysql.connector

prontuario_bp = Blueprint('prontuarios', __name__)

@prontuario_bp.route('/prontuarios', methods=['GET'])
def get_prontuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT prontuarios.*, pacientes.nome AS paciente_nome
        FROM prontuarios
        JOIN pacientes ON prontuarios.paciente_id = pacientes.id
    """)
    prontuarios = cursor.fetchall()
    conn.close()
    return jsonify(prontuarios)

@prontuario_bp.route('/prontuarios', methods=['POST'])
def create_prontuario():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prontuarios (paciente_id, descricao, exames, diagnosticos, tratamentos, evolucao_clinica) VALUES (%s, %s, %s, %s, %s, %s)",
        (data['paciente_id'], data['descricao'], data.get('exames'), data.get('diagnosticos'), data.get('tratamentos'), data.get('evolucao_clinica'))
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Prontuário criado com sucesso"}), 201

@prontuario_bp.route('/prontuarios/<int:id>', methods=['GET'])
def get_prontuario(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prontuarios WHERE id = %s;", (id,))
    prontuario = cursor.fetchone()
    conn.close()
    if prontuario:
        return jsonify(prontuario)
    else:
        return jsonify({"message": "Prontuário não encontrado"}), 404

@prontuario_bp.route('/prontuarios/<int:id>', methods=['DELETE'])
def delete_prontuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prontuarios WHERE id = %s;", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Prontuário deletado com sucesso"})


@prontuario_bp.route('/prontuarios/<int:id>', methods=['PUT'])
def update_prontuario(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE prontuarios
            SET paciente_id = %s, descricao = %s, exames = %s, diagnosticos = %s, tratamentos = %s, evolucao_clinica = %s
            WHERE id = %s
            """,
            (data['paciente_id'], data['descricao'], data.get('exames'), data.get('diagnosticos'), data.get('tratamentos'), data.get('evolucao_clinica'), id)
        )
        conn.commit()
        return jsonify({"message": "Prontuário atualizado com sucesso"})
    except mysql.connector.errors.DatabaseError as e:
        conn.rollback()
        return jsonify({"message": "Erro ao atualizar prontuário", "error": str(e)}), 500
    finally:
        conn.close()