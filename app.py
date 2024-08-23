from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from audio_summarizer import summarize_audio_file

app = Flask(__name__)

# Allow CORS for the specific frontend URL
CORS(app, resources={r"/*": {"origins": "https://audio-summarizer-frontend.vercel.app"}})

@app.route('/summarize', methods=['POST'])
def summarize():
    # Save the uploaded audio file temporarily
    audio_file = request.files['file']
    file_path = 'temp_audio_file'  # Temporary file path
    audio_file.save(file_path)

    # Summarize the audio file
    summary = summarize_audio_file(file_path)

    # Clean up the temporary file
    os.remove(file_path)

    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
