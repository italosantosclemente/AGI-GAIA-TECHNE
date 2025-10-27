import pytest
import socketio
import time

# Test connection to the WebSocket server
def test_connection():
    sio = socketio.Client()
    try:
        sio.connect('http://localhost:5000')
        assert sio.sid is not None
    finally:
        sio.disconnect()

# Test the metrics namespace
def test_metrics_namespace():
    sio = socketio.Client()
    metrics_received = False

    @sio.on('metrics_update', namespace='/metrics')
    def on_metrics(data):
        nonlocal metrics_received
        assert 'techné' in data
        assert 'iae' in data
        assert 'harmony' in data
        metrics_received = True

    try:
        sio.connect('http://localhost:5000', namespaces=['/metrics'])
        sio.emit('analyze_metrics', {'conjecture': 'test'}, namespace='/metrics')
        time.sleep(1) # Wait for the server to respond
        assert metrics_received
    finally:
        sio.disconnect()

# Test the narrative namespace
def test_narrative_namespace():
    sio = socketio.Client()
    narrative_received = False

    @sio.on('narrative_update', namespace='/narrative')
    def on_narrative(data):
        nonlocal narrative_received
        assert 'text' in data
        narrative_received = True

    try:
        sio.connect('http://localhost:5000', namespaces=['/narrative'])
        sio.emit('generate_narrative', {'conjecture': 'test'}, namespace='/narrative')
        time.sleep(5) # Wait for the server to respond
        assert narrative_received
    finally:
        sio.disconnect()

# Test the veto namespace
def test_veto_namespace():
    sio = socketio.Client()
    veto_confirmed = False

    @sio.on('veto_confirmed', namespace='/veto')
    def on_veto(data):
        nonlocal veto_confirmed
        assert data['status'] == 'success'
        veto_confirmed = True

    try:
        sio.connect('http://localhost:5000', namespaces=['/veto'])
        sio.emit('trigger_veto', {'activated': True}, namespace='/veto')
        time.sleep(1) # Wait for the server to respond
        assert veto_confirmed
    finally:
        sio.disconnect()
