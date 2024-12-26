from flask import Blueprint, render_template, jsonify
from jinja2 import TemplateNotFound

statics_bp = Blueprint('routes', __name__)

@statics_bp.route('/app/medicos', methods=['GET'])
def get_medicos_app():
    return render_template('medicos.html')

@statics_bp.route('/app/pacientes', methods=['GET'])
def get_pacientes_app():
    return render_template('pacientes.html')

@statics_bp.route('/app/consultas', methods=['GET'])
def get_consultas_app():
    return render_template('consultas.html')

@statics_bp.route('/app/prontuario', methods=['GET'])
def get_prontuario_app():
    return render_template('prontuario.html')

@statics_bp.route('/app/home', methods=['GET'])
def get_home_app():
    return render_template('home.html')

@statics_bp.route('/app/calendario', methods=['GET'])
def get_calendario_app():
    return render_template('calendario.html')

@statics_bp.route('/app/agenda', methods=['GET'])
def get_agenda_app():
    return render_template('agenda.html')

@statics_bp.route('/app/relatorios', methods=['GET'])
def get_relatorios_app():
    return render_template('relatorios.html')

@statics_bp.route('/app/horario-agendamento', methods=['GET'])
def get_horario_agendamento_app():
    try:
        return render_template('horario-agendamento.html')
    except TemplateNotFound:
        return jsonify({"message": "Template not found."}), 404