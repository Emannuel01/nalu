from flask import Blueprint, jsonify, request
from db import get_db_connection

pagamentos_bp = Blueprint('pagamentos', __name__)

@pagamentos_bp.route('/pagamentos', methods=['GET'])
def get_pagamentos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pagamentos;")
    pagamentos = cursor.fetchall()
    conn.close()
    return jsonify(pagamentos)

@pagamentos_bp.route('/pagamentos', methods=['POST'])
def create_pagamento():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pagamentos (consulta_id, valor, tipo_pagamento) VALUES (%s, %s, %s)",
        (data['consulta_id'], data['valor'], data['tipo_pagamento'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Pagamento criado com sucesso"}), 201