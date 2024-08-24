from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
from audio_summarizer import summarize_audio_file

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Server is running."

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'message': 'Connected to the server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('summarize')
def handle_summarize(data):
    # Expecting a file upload through WebSocket
    audio_file = data['file']  # You'll need to handle file decoding here
    file_path = 'temp_audio_file'  # Temporary file path

    with open(file_path, 'wb') as f:
        f.write(audio_file)

    # Summarize the audio file
    summary = summarize_audio_file(file_path)

    # Clean up the temporary file
    os.remove(file_path)

    emit('summary_response', {'summary': summary})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
