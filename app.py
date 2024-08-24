from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
from audio_summarizer import summarize_audio_file

app = Flask(__name__)

# Enable CORS for the specific frontend URL
CORS(app, resources={r"/*": {"origins": "https://audio-summarizer-frontend.vercel.app"}})

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/summarize', methods=['POST'])
def summarize():
    audio_file = request.files['file']
    file_path = 'temp_audio_file' 
    audio_file.save(file_path)

    summary = summarize_audio_file(file_path)

    os.remove(file_path)

    return jsonify({'summary': summary})

@socketio.on('summarize')
def handle_summarize(data):
    # Assuming 'file' is sent as an ArrayBuffer via WebSocket
    file_path = 'temp_audio_file'
    with open(file_path, 'wb') as f:
        f.write(data['file'])

    summary = summarize_audio_file(file_path)

    os.remove(file_path)

    # Emit the summary back to the client
    emit('summary_response', {'summary': summary})

if __name__ == '__main__':
    # Comment out or remove the line below
    # app.run(app, host='0.0.0.0', port=5000, debug=True)
    pass
