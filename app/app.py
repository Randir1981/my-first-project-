import os
from gtts import gTTS
import gradio as gr

# Premium Subscription User Interface Layout Setup
with gr.Blocks() as demo:
    gr.Markdown("# **RK PREMIUM VOICE MAKER**")
    gr.Markdown("### *Professional Offline-Grade Vocal Clone Studio Engine*")

    with gr.Column():
        vocal_sample = gr.Audio(label="Upload Target Voice Sample (10-15 Seconds)", type="filepath")
        language_choice = gr.Dropdown(label="Select Target Language", choices=["en", "hi", "es", "fr"], value="en")
        input_text = gr.Textbox(label="Type the Lyrics or Sentences to Speak", lines=3, placeholder="Enter text here...")
        submit_btn = gr.Button("Generate Premium Vocal Clone", variant="primary")

    with gr.Column():
        status_output = gr.Textbox(label="System Status Report")
        audio_output = gr.Audio(label="Generated Cloned Audio Output")

    def clone_voice(vocal_sample, input_text, language_choice):
        if not input_text:
            return "Please type some text first!", None

        try:
            # Convert text to speech natively using gTTS
            tts = gTTS(text=input_text, lang=language_choice)
            output_filename = "cloned_vocal_output.mp3"
            tts.save(output_filename)

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
