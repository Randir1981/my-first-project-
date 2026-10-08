import gradio as gr
from coqui_tts.api import TTS

def clone_voice(voice_file_path, text_input, language):
    class=class="str">"cmt"># Error checking for empty text input
    if not text_input.strip():
        return class="str">"Error: Text input cannot be empty."
    
    try:
        tts = TTS(model=class="str">'tts_models/multilingual/multi-dataset/xtts_v2', gpu=False)
        
        class=class="str">"cmt"># Constructing the full path to the uploaded voice file
        speaker_wav = fclass="str">"./{voice_file_path}"
        
        class=class="str">"cmt"># Generating the cloned voice
        tts.tts_to_file(text=text_input, speaker_wav=speaker_wav, lang=language, out_file=class="str">"cloned_vocal_output.wav")
        
        return class="str">"Vocal clone generated successfully!"
    except Exception as e:
        return str(e)

class=class="str">"cmt"># Gradio interface layout
with gr.Blocks() as demo:
    gr.Markdown(class="str">"**RK PREMIUM VOICE MAKER**\nProfessional Online-Grade Vocal Clone Studio Engine")
    
    with gr.Row():
        with gr.Column(scale=class="num">3):
            voice_file_upload = gr.File(label=class="str">"Upload Target Voice Sample")
            language_dropdown = gr.Dropdown(choices=[class="str">'en', class="str">'hi', class="str">'es', class="str">'fr'], label=class="str">"Select Target Language")
            text_box = gr.Textbox(lines=class="num">5, placeholder=class="str">"Type the Lyrics or Sentences to Speak", label=class="str">"Text Input")
        
        with gr.Column(scale=class="num">2):
            generate_button = gr.Button(class="str">"Generate Premium Vocal Clone")
            status_report = gr.Textbox(label=class="str">"System Status Report", lines=class="num">2, interactive=False)
            
            with gr.Audio(type=class="str">"filepath", label=class="str">"Generated Cloned Audio Output") as audio_player:
                pass
    
    generate_button.click(clone_voice, inputs=[voice_file_upload, text_box, language_dropdown], outputs=[status_report, audio_player])

if __name__ == class="str">"__main__":
    demo.launch(server_name=class="str">"class="num">0.0.class="num">0.0", server_port=class="num">10000)
