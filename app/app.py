import os
import gradio as gr
import requests

# Reconstruct the hidden model endpoint bypass to avoid system text overwriting
base_host = "api-inference"
domain_name = "huggingface.co"
target_model = "coqui/XTTS-v2"

API_URL = "https://api-inference.huggingface.co/models/coqui/XTTS-v2"

HEADERS = {"Authorization": f"Bearer {os.getenv('HF_API_KEY', '')}"}
import base64

import os
import shutil

def clone_voice(audio_file, text_to_speak):
    if not audio_file or not text_to_speak:
        return "Please upload a 10-second vocal clip and type some text first!", None

    try:
        # Create a temporary safe path with no broken system spaces
        safe_path = os.path.join(os.path.dirname(audio_file), "safe_vocal_dna.wav")
        shutil.copyfile(audio_file, safe_path)

        # Convert raw audio bytes into a clean, safe string layout for the server payload
        with open(safe_path, "rb") as f:
            audio_bytes = f.read()
            encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

        payload = {
            "inputs": text_to_speak,
            "parameters": {"speaker_wav": encoded_audio}
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)

        # Clean up temporary safe file right away
        if os.path.exists(safe_path):
            os.remove(safe_path)

        if response.status_code == 200:
            output_path = "cloned_vocal_output.wav"
            with open(output_path, "wb") as out_f:
                out_f.write(response.content)
            return "Voice cloning successful! Your premium vocal track is ready below:", output_path
        else:
            return f"Server busy or layout updating. Status code: {response.status_code}. Response: {response.text[:100]}", None

    except Exception as e:
        return f"System error processing vocal DNA: {str(e)}", None



    except Exception as e:
        return f"System error processing vocal DNA: {str(e)}", None




# Premium Subscription User Interface Layout
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# **RK PREMIUM VOICE MAKER**")
    gr.Markdown("### *Professional Offline-Grade Vocal Clone Studio Engine*")

    with gr.Row():
        with gr.Column():
            vocal_sample = gr.Audio(label="Upload Target Voice Sample (10-15 Seconds)", type="filepath")
            input_text = gr.Textbox(label="Type the Lyrics or Sentences to Speak", lines=3, placeholder="Enter text here...")
            submit_btn = gr.Button("Generate Premium Voice Clone", variant="primary")

        with gr.Column():
            status_output = gr.Textbox(label="System Status Report")
            audio_output = gr.Audio(label="Generated Cloned Audio Output")

    submit_btn.click(
        fn=clone_voice,
        inputs=[vocal_sample, input_text],
        outputs=[status_output, audio_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)



