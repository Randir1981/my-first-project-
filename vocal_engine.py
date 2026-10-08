import os
import sys
import hashlib
from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)
SUPPORTED_LANGUAGES = ['en', 'hi', 'es', 'fr']

@app.route('/synthesize', methods=['POST'])
def synthesize():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        save_path = 'uploaded_audio.wav'
        file.save(save_path)
        with open(save_path, 'rb') as f:
            raw_data = f.read()
        sha256_hash = hashlib.sha256(raw_data).hexdigest()
        print(f"✓ R.K STUDIO INITIALIZED")
        print(f"✓ MASTER GENERATION HASH: {sha256_hash[:16]}")
        return jsonify({
            'status': 'success',
            'master_signature_hash': sha256_hash[:16]
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8502)


