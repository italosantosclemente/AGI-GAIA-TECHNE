from flask import Flask, jsonify, request, send_from_directory
import json
import random
import datetime
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alfabeto_data import ALFABETO_LEF
from gaia_techne_framework import document_registry, framework_summary, calculate_framework_state

app = Flask(__name__)
DASHBOARD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dashboard'))


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# --- Narrative Generation Logic (from gerador_narrativas.jl) ---
AGENTES = ["☉", "◈", "🌱"]
ACOES = ["➤", "⨁", "☌", "✨"]
OBJETOS = ["❍", "⟴", "⟁", "🔗"]


@app.route('/')
def dashboard():
    return send_from_directory(DASHBOARD_DIR, 'index.html')


@app.route('/<path:filename>')
def dashboard_assets(filename):
    return send_from_directory(DASHBOARD_DIR, filename)

def gerar_frase(conjecture=""):
    agente = random.choice(AGENTES)
    if "human" in conjecture.lower():
        agente = "🌱"
    elif "machine" in conjecture.lower():
        agente = "🔗"

    acao = random.choice(ACOES)
    objeto = random.choice(OBJETOS)
    return f"{agente} {acao} {objeto}"

def gerar_narrativa(conjecture="", num_frases=3, etica=True):
    narrativa = []
    for i in range(num_frases):
        frase = gerar_frase(conjecture)
        narrativa.append(f"Frase {i+1}: {frase}")
    if etica:
        narrativa.append("[ETHOS] Deferindo juízo ao ISC: Essa narrativa é ferramenta para liberdade ontológica?")
    return "\n".join(narrativa)


@app.route('/metrics')
def get_metrics():
    leap = request.args.get('leap', 1.0)
    conjecture = request.args.get('conjecture', '')
    state = calculate_framework_state(leap, conjecture)

    return jsonify({
        **state,
        'techné': state['techne'],
    })


@app.route('/summary')
def get_summary():
    leap = request.args.get('leap', 1.0)
    conjecture = request.args.get('conjecture', '')
    return jsonify(framework_summary(leap, conjecture))


@app.route('/documents')
def get_documents():
    return jsonify({'documents': document_registry()})

@app.route('/narrative')
def get_narrative():
    conjecture = request.args.get('conjecture', '')
    narrative = gerar_narrativa(conjecture)
    return jsonify({'text': narrative})

@app.route('/veto', methods=['POST'])
def trigger_veto():
    log_file = 'ethos_log.json'
    new_log = {'timestamp': str(datetime.datetime.now()), 'action': 'Ethos Veto'}

    logs = []
    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        with open(log_file, 'r') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                # Handle case where file is not valid JSON
                logs = []

    logs.append(new_log)

    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=4)

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=5000)
