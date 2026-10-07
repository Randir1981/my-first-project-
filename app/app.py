import os
import shutil
import gradio as gr
from gradio_client import Client, handle_file

# Official Hugging Face Spaces repository for the XTTS voice cloning engine
HF_SPACE = "coqui/XTTS-v2"

def clone_voice(audio_file, text_to_speak, language_choice):
    if not audio_file or not text_to_speak:
        return "Please upload your vocal clip and type some text first!", None
    client = Client("coqui/XTTS-v2") 
         
        # Securely initialize the connection to the Hugging Face server
        token = os.getenv('HF_API_KEY', '')
        # client = Client(HF_SPACE, token=token if token else None)
        # Execute the official endpoint layout for XTTS voice duplication
        result = client.predict(
            text=text_to_speak,
            language=language_choice,
            speaker_wav=handle_file(audio_file),
            api_name="/predict"
        )

        # Save a clean copy of the generated vocal file locally
        output_path = "cloned_vocal_output.wav"
        shutil.copyfile(result, output_path)

        return "Voice cloning successful! Your premium vocal track is ready below:", output_path

    except Exception as e:
        return f"System error processing vocal DNA: {str(e)}", None
# Premium Subscription User Interface Layout Setup
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# **RK PREMIUM VOICE MAKER**")
    gr.Markdown("### *Professional Offline-Grade Vocal Clone Studio Engine*")

    with gr.Column():
        vocal_sample = gr.Audio(label="Upload Target Voice Sample (10-15 Seconds)", type="filepath")
        language_choice = gr.Dropdown(label="Select Target Language", choices=["en", "hi", "es", "fr"], value="en")
        input_text = gr.Textbox(label="Type the Lyrics or Sentences to Speak", lines=3, placeholder="Enter text here...")
        submit_btn = gr.Button("Generate Premium Voice Clone", variant="primary")

    with gr.Column():
            status_output = gr.Textbox(label="System Status Report")
            audio_output = gr.Audio(label="Generated Cloned Audio Output")

    submit_btn.click(
        fn=clone_voice,
         inputs=[vocal_sample, input_text, language_choice],
        outputs=[status_output, audio_output]
    )

if __name__ == "__main__":
    # Custom studio server layout for cloud hosting deployment
    demo.launch(server_name="0.0.0.0", server_port=10000)


