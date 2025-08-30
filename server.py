# server.py auf dem Raspberry Pi
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=*)

@app.route('/')
def index():
    return render_template('jarvis.html')

@socketio.on('audio_stream')
def handle_audio_stream(data):
    # Audio von Browser empfangen
    audio_data = base64.b64decode(data['audio'])
    
    # An Jarvis verarbeiten
    text = jarvis.transcribe(audio_data)
    response_text = jarvis.process(text)
    response_audio = jarvis.tts(response_text)
    
    # Zurück zum Browser senden
    emit('response', {
        'text': response_text,
        'audio': base64.b64encode(response_audio).decode()
    })
