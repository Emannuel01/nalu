from flask import Blueprint, jsonify, request, render_template
from db import get_db_connection

pacientes_bp = Blueprint('pacientes', __name__)


@pacientes_bp.route('/pacientes', methods=['GET'])
def get_pacientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pacientes;")
    pacientes = cursor.fetchall()
    conn.close()
    return jsonify(pacientes)

@pacientes_bp.route('/pacientes', methods=['POST'])
def create_paciente():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email é obrigatório."}), 400

    try:
        idade = int(data.get('idade', 0))  # Valida idade
    except ValueError:
        return jsonify({"message": "Idade deve ser um número inteiro."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica se já existe um paciente com o mesmo email
        cursor.execute("SELECT * FROM pacientes WHERE email = %s", (email,))
        paciente_existente = cursor.fetchone()

        if paciente_existente:
            conn.close()
            return jsonify({"message": "Paciente com este email já está cadastrado."}), 400

        # Inserção dos dados
        cursor.execute(
            "INSERT INTO pacientes (nome, cpf, idade, genero, endereco, telefone, email, historico_pacientes) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (data['nome'],data['cpf'], data['idade'], data.get('genero'), data.get('endereco'), data.get('telefone'), email, data.get('historico'))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Paciente criado com sucesso"}), 201

    except Exception as e:
        return jsonify({"message": "Erro interno no servidor.", "error": str(e)}), 500

