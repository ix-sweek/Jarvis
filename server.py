#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import base64
import json
import speech_recognition as sr
import pyttsx3
import io
import numpy as np
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # <- Hier fehlten die Anführungszeichen

class JarvisCore:
    def __init__(self):
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        
        # Text-to-Speech
        self.tts = pyttsx3.init()
        self.setup_voice()
        
        # Command handlers
        self.commands = {
            "time": self.get_time,
            "date": self.get_date,
            "hello": lambda: "Hello! How can I help you?",
            "weather": lambda: "Weather feature coming soon!",
        }
    
    def setup_voice(self):
        voices = self.tts.getProperty('voices')
        # Try to find a female voice
        for voice in voices:
            if 'female' in voice.name.lower():
                self.tts.setProperty('voice', voice.id)
                break
        self.tts.setProperty('rate', 180)  # Speed
        self.tts.setProperty('volume', 0.9)  # Volume
    
    def get_time(self):
        now = datetime.now()
        return f"It's {now.strftime('%H:%M')}"
    
    def get_date(self):
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}"
    
    def transcribe(self, audio_data):
        try:
            # Convert audio data to AudioData for speech_recognition
            audio = sr.AudioData(audio_data, sample_rate=16000, sample_width=2)
            text = self.recognizer.recognize_google(audio)
            return text
        except Exception as e:
            print(f"Transcription error: {e}")
            return "Could not understand audio"
    
    def process(self, text):
        text_lower = text.lower()
        
        # Check for known commands
        for keyword, handler in self.commands.items():
            if keyword in text_lower:
                return handler()
        
        # Default response
        return f"You said: {text}. I'm still learning!"
    
    def text_to_speech(self, text):
        # Save TTS to file and return audio data
        self.tts.save_to_file(text, '/tmp/response.mp3')
        self.tts.runAndWait()
        
        with open('/tmp/response.mp3', 'rb') as f:
            return f.read()

# Initialize Jarvis
jarvis = JarvisCore()

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
        
        # Generate TTS
        audio_response = jarvis.text_to_speech(response_text)
        
        emit('response', {
            'text': response_text,
            'audio': base64.b64encode(audio_response).decode()
        })
    except Exception as e:
        emit('error', {'message': str(e)})
        print(f"Error: {e}")

if __name__ == '__main__':
    print("Starting Jarvis Server...")
    print("Access at: http://covas-ai.local:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
