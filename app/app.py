import os
import subprocess
import gradio as gr

class=class="str">"cmt"># Premium Subscription User Interface Layout Setup
with gr.Blocks() as demo:
    gr.Markdown(class="str">"class="cmtclass="str">"># **RK PREMIUM VOICE MAKER**")
    gr.Markdown(class="str">"class="cmtclass="str">">### *Professional Offline-Grade Vocal Clone Studio Engine*")

    with gr.Column():
        vocal_sample = gr.Audio(label=class="str">"Upload Target Voice Sample(class="num">10-class="num">15 Seconds)", type=class="str">"filepath")
        language_choice = gr.Dropdown(label=class="str">"Select Target Language", choices=[class="str">"en", class="str">"hi", class="str">"es", class="str">"fr"], value=class="str">"en")
        input_text = gr.Textbox(label=class="str">"Type the Lyrics or Sentences to Speak", lines=class="num">3, placeholder=class="str">"Enter text here...")
        submit_btn = gr.Button(class="str">"Generate Premium Vocal Clone", variant=class="str">"primary")

    with gr.Column():
        status_output = gr.Textbox(label=class="str">"System Status Report")
        audio_output = gr.Audio(label=class="str">"Generated Cloned Audio Output")

    def clone_voice(audio_file, text_to_speak, language_choice):
        if not text_to_speak:
            return class="str">"Please type some text first!", None

        try:
            class=class="str">"cmt"># Save uploaded audio file temporarily
            temp_audio_path = class="str">"temp_voice_sample.wav"
            with open(temp_audio_path, class="str">"wb") as audio_file_out:
                audio_file_out.write(audio_file.read())

            class=class="str">"cmt"># Path to XTTS model and configuration
            xtts_model_path = class="str">"path/to/xtts/model"
            xtts_config_path = class="str">"path/to/xtts/config.yaml"

            class=class="str">"cmt"># Command to run XTTS pipeline
            command = [
                class="str">"python", class="str">"-m", class="str">"xtts.inference",
                class="str">"--model-path", xtts_model_path,
                class="str">"--config-path", xtts_config_path,
                class="str">"--input-audio", temp_audio_path,
                class="str">"--output-dir", class="str">"./",
                class="str">"--text", text_to_speak,
                class="str">"--language", language_choice
            ]

            class=class="str">"cmt"># Run XTTS pipeline
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != class="num">0:
                return fclass="str">"XTTS pipeline failed: {result.stderr}", None

            class=class="str">"cmt"># Get the output audio filename from the command output
            output_filename = result.stdout.strip()

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
