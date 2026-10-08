import os
import gradio as gr
from TTS.api import TTS

with gr.Blocks() as demo:
    gr.Markdown(class="str">"class="cmtclass="str">"># **RK PREMIUM VOICE MAKER**")
    gr.Markdown(class="str">"class="cmtclass="str">">### ***Professional Online-Grade Vocal Clone Studio Engine***")

    with gr.Column():
        vocal_sample = gr.Audio(label=class="str">"Upload Target Voice Sample", type=class="str">"filepath")
        language_choice = gr.Dropdown(label=class="str">"Select Target Language", choices=[class="str">"en", class="str">"hi", class="str">"es", class="str">"fr"])
        input_text = gr.Textbox(label=class="str">"Type the Lyrics or Sentences to Speak", lines=class="num">3, placeholder=class="str">"Enter text here...")
        submit_btn = gr.Button(class="str">"Generate Premium Vocal Clone", variant=class="str">"primary")

    with gr.Column():
        status_output = gr.Textbox(label=class="str">"System Status Report")
        audio_output = gr.Audio(label=class="str">"Generated Cloned Audio Output")

    def clone_voice(audio_file, text_to_speak, language_choice):
        if not text_to_speak:
            return class="str">"Please type some text first!", None
        try:
            output_filename = class="str">"cloned_vocal_output.wav"
            tts = TTS(model_name=class="str">"tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
            tts.tts_to_file(
                text=text_to_speak,
                speaker_wav=audio_file,
                language=language_choice,
                file_path=output_filename
            )
            return class="str">"Voice cloning successful! Your premium vocal track is ready below:", output_filename
        except Exception as e:
            return fclass="str">"System error processing vocal DNA: {str(e)}", None

    submit_btn.click(
        fn=clone_voice,
        inputs=[vocal_sample, input_text, language_choice],
        outputs=[status_output, audio_output]
    )

if __name__ == class="str">"__main__":
    demo.launch(server_name=class="str">"class="num">0.0.class="num">0.0", server_port=class="num">10000)
