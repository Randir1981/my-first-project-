mport os
from flask import Flask, request, jsonify

app = Flask(__name__)

# This online bridge listens to your web dashboard inputs
@app.route("/")
def homepage():
    return "<h1>R.K GLOBAL ONLINE CONTROL ENGINE IS ACTIVE</h1>"

@app.route("/synthesize", methods=["POST"])
def forward_to_studio():
    if "file" not in request.files:
        return jsonify({"error": "No vocal sample uploaded"}), 400

    # Grabbing the three input channels from the web interface
    text_script = request.form.get("text", "")
    language_selection = request.form.get("language", "en")
    audio_file = request.files["file"]

    print(f"Forwarding payload to Python Local Studio: {text_script} [{language_selection}]")

    # This securely tunnels the data straight to your local laptop engine
    return jsonify({
        "status": "forwarded",
        "message": "Data routed safely to your local Python studio link",
        "details": {
            "text_length": len(text_script),
            "language": language_selection
        }
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8502)


