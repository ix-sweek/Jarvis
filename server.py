#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import base64
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # <- Hier fehlten die Anführungszeichen

# Temporärer Jarvis Mock für Tests
class JarvisMock:
    def transcribe(self, audio_data):
        return "Test transcription"
    
    def process(self, text):
        return f"Du hast gesagt: {text}"
    
    def tts(self, text):
        # Gibt erstmal leere Audio-Daten zurück
        return b"mock_audio_data"

jarvis = JarvisMock()

@app.route('/')
def index():
    return render_template('jarvis.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')
    response = jarvis.process(command)
    return jsonify({'response': response})

@socketio.on('audio_stream')
def handle_audio_stream(data):
    try:
        audio_data = base64.b64decode(data['audio'])
        text = jarvis.transcribe(audio_data)
        response_text = jarvis.process(text)
        response_audio = jarvis.tts(response_text)
        
        emit('response', {
            'text': response_text,
            'audio': base64.b64encode(response_audio).decode()
        })
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    print("Starting Jarvis Server...")
    print("Access at: http://covas-ai.local:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
