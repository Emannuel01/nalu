from flask import Blueprint, jsonify
from db import get_db_connection

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios/pacientes_por_genero', methods=['GET'])
def pacientes_por_genero():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT genero, COUNT(*) as quantidade
    FROM pacientes
    GROUP BY genero
    """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    relatorio = [{'genero': row['genero'], 'quantidade': row['quantidade']} for row in result]
    return jsonify(relatorio)

@relatorios_bp.route('/relatorios/consultas_por_medico', methods=['GET'])
def consultas_por_medico():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT m.nome as medico, COUNT(c.id) as quantidade
    FROM consultas c
    JOIN medicos m ON c.medico_id = m.id
    GROUP BY m.nome
    """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    relatorio = [{'medico': row['medico'], 'quantidade': row['quantidade']} for row in result]
    return jsonify(relatorio)

@relatorios_bp.route('/relatorios/pagamentos_por_status', methods=['GET'])
def pagamentos_por_status():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT status_pagamento, COUNT(*) as quantidade
    FROM pagamentos
    GROUP BY status_pagamento
    """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    relatorio = [{'status_pagamento': row['status_pagamento'], 'quantidade': row['quantidade']} for row in result]
    return jsonify(relatorio)