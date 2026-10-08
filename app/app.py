import os
import subprocess
import gradio as gr

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
            xtts_model_path = "path/to/xtts/model"
            xtts_config_path = "path/to/xtts/config.yaml"
            output_filename = "cloned_vocal_output.wav"

            command = [
                "python", "-m", "xtts.inference",
                "--model-path", xtts_model_path,
                "--config-path", xtts_config_path,
                "--input-audio", audio_file,
                "--output-dir", ".",
                "--text", text_to_speak,
                "--language", language_choice
            ]

            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                return f"XTTS pipeline failed: {result.stderr}", None

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


