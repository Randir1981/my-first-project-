import os
import gradio as gr
from TTS.api import TTS

with gr.Blocks() as demo:
    gr.Markdown("# **RK PREMIUM VOICE MAKER**")
    gr.Markdown("### ***Professional Online-Grade Vocal Clone Studio Engine***")

    with gr.Column():
        vocal_sample = gr.Audio(label="Upload Target Voice Sample", type="filepath")
        language_choice = gr.Dropdown(label="Select Target Language", choices=["en", "hi", "es", "fr"])
        input_text = gr.Textbox(label="Type the Lyrics or Sentences to Speak", lines=3, placeholder="Enter text here...")
        submit_btn = gr.Button("Generate Premium Vocal Clone", variant="primary")

    with gr.Column():
    status_output = gr.Textbox(label="System Status Report")
    audio_output = gr.Audio(label="Generated Cloned Audio Output")

    def clone_voice(audio_file, text_to_speak, language_choice):
        if not text_to_speak:
        return "Please type some text first!", None
        try:
        output_filename = "cloned_vocal_output.wav"

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
tts.tts_to_file(
text=text_to_speak,
speaker_wav=audio_file,
language=language_choice,
            file_path=output_filename
            )

            return "Voice cloning successful! Your premium vocal track is ready below:", output_filename
            except Exception as e:
            return f"System error processing vocal DNA: {str(e)}", None

        submit_btn.click(
        fn=clone_voice,
        inputs=[vocal_sample, input_text, language_choice],
outputs=[status_output, audio_output]
    )

    if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)
