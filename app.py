from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from audio_summarizer import summarize_audio_file

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://audio-summarizer-frontend.vercel.app"}})

@app.route('/summarize', methods=['POST'])
def summarize():
    audio_file = request.files['file']
    file_path = 'temp_audio_file' 
    audio_file.save(file_path)

    summary = summarize_audio_file(file_path)

    os.remove(file_path)

    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(app, host='0.0.0.0', port=5000, debug=True)
