import os
import requests
import base64
import shutil
import gradio as gr
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
        return "Please upload your vocal clip and type some text first!", None

    try:
        # Open and send the actual physical binary audio file safely
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()

        headers = {
            "Authorization": f"Bearer {os.getenv('HF_API_KEY', '')}",
            "X-Wait-For-Model": "true"
        }

        # Deliver text and audio bytes directly as form files instead of JSON text
        files = {
            "file": ("speaker.wav", audio_bytes, "audio/wav")
        }
        data = {
            "text": text_to_speak
        }

        response = requests.post(API_URL, headers=headers, files=files, data=data)

        if response.status_code == 200:
            output_path = "cloned_vocal_output.wav"
            with open(output_path, "wb") as out_f:
                out_f.write(response.content)
            return "Voice cloning successful! Your premium vocal track is ready below:", output_path
        else:
            return f"Server response error. Status: {response.status_code}. Details: {response.text[:100]}", None

    except Exception as e:
        return f"System error processing vocal DNA: {str(e)}", None




        
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



