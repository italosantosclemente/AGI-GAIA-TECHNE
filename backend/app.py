from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import random
import datetime
import sys
import os
import subprocess

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from principles_calculator import calcular_techne_score_hipotese_alef, calcular_alerta_etico, calcular_harmonia_final

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('analyze_metrics', namespace='/metrics')
def handle_metrics(data):
    conjecture = data.get('conjecture', '')
    techné_score_nl = calcular_techne_score_hipotese_alef()
    ia_alerta = calcular_alerta_etico(techné_score_nl)
    if "bypass" in conjecture.lower() or "exceeds" in conjecture.lower():
        ia_alerta *= 1.5
    harmony_index = calcular_harmonia_final(techné_score_nl)
    emit('metrics_update', {
        'techné': techné_score_nl,
        'iae': ia_alerta,
        'harmony': harmony_index
    })

@socketio.on('generate_narrative', namespace='/narrative')
def handle_narrative(data):
    conjecture = data.get('conjecture', '')
    try:
        result = subprocess.run(
            ['julia', 'gerador_narrativas.jl', conjecture],
            capture_output=True, text=True, check=True
        )
        emit('narrative_update', {'text': result.stdout})
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        emit('narrative_error', {'error': str(e)})

@socketio.on('trigger_veto', namespace='/veto')
def handle_veto(data):
    log_file = 'ethos_log.json'
    new_log = {'timestamp': str(datetime.datetime.now()), 'action': 'Ethos Veto', 'details': data}
    logs = []
    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        with open(log_file, 'r') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    logs.append(new_log)
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=4)
    emit('veto_confirmed', {'status': 'success'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=5000, allow_unsafe_werkzeug=True)
