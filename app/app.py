from flask import Flask
from flask_cors import CORS
from routes.pacientes import pacientes_bp
from routes.medicos import medicos_bp
from routes.consultas import consultas_bp
from routes.prontuario import prontuario_bp
from routes.statics import statics_bp
from routes.relatorios import relatorios_bp
from routes.agendamento import agendamento_bp

app = Flask(__name__)

# Configuração específica de CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Registrar os Blueprints
app.register_blueprint(pacientes_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(consultas_bp)
app.register_blueprint(prontuario_bp)
app.register_blueprint(statics_bp)
app.register_blueprint(relatorios_bp)


@app.route('/')
def index():
    return "Bem-vindo à API da Clínica Médica!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)