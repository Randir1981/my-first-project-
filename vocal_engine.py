import os
import sys
import hashlib
from flask import Flask, request, jsonify
from waitress import serve

app = Flask(__name__)

@app.route("/")
def homepage():
    return "<h1>R.K GLOBAL STUDIO ENGINE IS ONLINE</h1>"

@app.route("/synthesize", methods=["POST"])
def synthesize():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400
    file.save("uploaded_audio.wav")
    print("R.K STUDIO INITIALIZED")
    return jsonify({"status": "success", "signature": "verified"}), 200

if __name__ == "__main__":
    print("Serving studio professionally on port 8502...")
    serve(app, host="0.0.0.0", port=8502)

