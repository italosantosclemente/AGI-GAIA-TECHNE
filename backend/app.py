from flask import Flask, jsonify, request
import json
import random
import datetime
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from principles_calculator import calcular_techne_score_hipotese_alef, calcular_alerta_etico, calcular_harmonia_final
from alfabeto_data import ALFABETO_LEF

app = Flask(__name__)

# --- Narrative Generation Logic (from gerador_narrativas.jl) ---
AGENTES = ["☉", "◈", "🌱"]
ACOES = ["➤", "⨁", "☌", "✨"]
OBJETOS = ["❍", "⟴", "⟁", "🔗"]

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
    leap = float(request.args.get('leap', 0.5))
    conjecture = request.args.get('conjecture', '')

    techné_score_nl = calcular_techne_score_hipotese_alef() * leap
    ia_alerta = calcular_alerta_etico(techné_score_nl)

    # Modify IAE based on conjecture
    if "bypass" in conjecture.lower() or "exceeds" in conjecture.lower():
        ia_alerta *= 1.5

    harmony_index = calcular_harmonia_final(techné_score_nl)

    return jsonify({
        'techné': techné_score_nl,
        'iae': ia_alerta,
        'harmony': [harmony_index] * 10,
        'ethos': 1.0
    })

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
