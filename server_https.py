#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import base64
import json
from datetime import datetime
from gtts import gTTS
import os
import ssl

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class JarvisCore:
    def __init__(self):
        self.commands = {
            "time": self.get_time,
            "date": self.get_date,
            "hello": lambda: "Hello! How can I help you?",
            "jarvis": lambda: "Yes, I'm here! How can I assist you?",
            "weather": lambda: "Weather feature coming soon!",
        }
    
    def get_time(self):
        now = datetime.now()
        return f"It's {now.strftime('%I:%M %p')}"
    
    def get_date(self):
        now = datetime.now() 
        return f"Today is {now.strftime('%A, %B %d, %Y')}"
    
    def process(self, text):
        text_lower = text.lower()
        
        for keyword, handler in self.commands.items():
            if keyword in text_lower:
                return handler()
        
        return f"You said: {text}. I'm still learning!"
    
    def text_to_speech(self, text):
        try:
            tts = gTTS(text=text, lang='en', tld='com')
            temp_file = "/tmp/jarvis_response.mp3"
            tts.save(temp_file)
            
            with open(temp_file, 'rb') as f:
                audio_data = f.read()
            
            os.remove(temp_file)
            return audio_data
        except Exception as e:
            print(f"TTS Error: {e}")
            return b""

jarvis = JarvisCore()

@app.route('/')
def index():
    return render_template('jarvis.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command')
    response = jarvis.process(command)
    audio = jarvis.text_to_speech(response)
    
    return jsonify({
        'response': response,
        'audio': base64.b64encode(audio).decode() if audio else None
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 JARVIS AI ASSISTANT (HTTPS)")
    print("=" * 50)
    print("Access from any device at:")
    print("  → https://covas-ai.local:5000")
    print("  → https://192.168.1.83:5000")
    print("=" * 50)
    print("NOTE: Accept the security warning in your browser!")
    print("=" * 50)
    
    # Run with SSL
    socketio.run(app, 
                 host='0.0.0.0', 
                 port=5000, 
                 debug=True,
                 ssl_context=('cert.pem', 'key.pem'))
