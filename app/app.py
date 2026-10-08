class="str">""class="str">"
RK Premium Voice Maker — Professional Online-Grade Vocal Clone Studio Engine
Built with Gradio UI and Coqui TTS(XTTS-v2) backend.

Deployment Target: Render(Python class="num">3.10+)
GPU: Auto-detected(defaults to CPU if unavailable)
Model: tts_models/multilingual/multi-dataset/xtts_v2
"class="str">""

import os
import sys
import traceback
from pathlib import Path

class=class="str">"cmt"># ---------------------------------------------------------------------------
class=class="str">"cmt"># Imports
class=class="str">"cmt"># ---------------------------------------------------------------------------
try:
 import gradio as gr
except ImportError:
 raise RuntimeError(
 class="str">"gradio is not installed. Run: pip install gradio"
 )

class=class="str">"cmt"># Coqui TTS — pin a known-compatible version for stability on Render
try:
 from TTS.api import TTS
except ImportError:
 raise RuntimeError(
 class="str">"TTS(coqui-tts) is not installed. Run: pip install TTS"
 )

class=class="str">"cmt"># ---------------------------------------------------------------------------
class=class="str">"cmt"># Constants
class=class="str">"cmt"># ---------------------------------------------------------------------------
APP_TITLE = class="str">"RK PREMIUM VOICE MAKER"
APP_SUBTITLE = class="str">"Professional Online-Grade Vocal Clone Studio Engine"
OUTPUT_WAV = class="str">"cloned_vocal_output.wav"
HOST = class="str">"class="num">0.0.class="num">0.0"
PORT = class="num">10000
SUPPORTED_LANGUAGES = [class="str">"en", class="str">"hi", class="str">"es", class="str">"fr"]

class=class="str">"cmt"># Re-use a single TTS instance across requests(avoids re-downloading the model).
_tts_instance: TTS | None = None

class=class="str">"cmt"># ---------------------------------------------------------------------------
class=class="str">"cmt"># Helpers
class=class="str">"cmt"># ---------------------------------------------------------------------------
def _get_tts() -> TTS:
 class="str">""class="str">"Return a singleton ``TTS`` instance, lazily initialising it."class="str">""
 global _tts_instance
 if _tts_instance is not None:
 return _tts_instance

 class=class="str">"cmt"># Detect GPU availability(Coqui handles this internally, but we pass
 class=class="str">"cmt"># gpu=False so it always runs on CPU — safe for free Render tier).
 print(class="str">"[RK Voice] Initialising XTTS-v2 model(CPU mode)…")
 _tts_instance = TTS(
 model_name=class="str">"tts_models/multilingual/multi-dataset/xtts_v2",
 gpu=False, class=class="str">"cmt"># Set True only on paid/pro instances with GPU
 )
 print(class="str">"[RK Voice] Model loaded successfully.")
 return _tts_instance

def clone_voice(voice_file: str | None, text: str, language: str) -> tuple[str, str | None]:
 class="str">""class="str">"
 Generate a cloned vocal WAV from the uploaded voice sample and input text.

 Parameters
 ----------
 voice_file : str or None
 Path to the uploaded reference audio file.
 text : str
 The lyrics / sentences to speak.
 language : str
 Target language code(class="str">'en', class="str">'hi', class="str">'es', class="str">'fr').

 Returns
 -------
 status_report : str
 Human-readable log of the operation.
 wav_path : str or None
 Path to the generated WAV file, or *None* on failure.
 "class="str">""
 status_lines: list[str] = []

 class=class="str">"cmt"># --- class="num">1. Validate inputs ------------------------------------------------
 if not text or not text.strip():
 msg = class="str">"⚠️ STATUS REPORT: No text provided. Please enter lyrics or sentences to speak."
 status_lines.append(msg)
 return (class="str">"\n".join(status_lines)), None

 if not voice_file or not Path(voice_file).exists():
 msg = class="str">"⚠️ STATUS REPORT: No valid voice sample uploaded. Please upload a target voice audio file."
 status_lines.append(msg)
 return (class="str">"\n".join(status_lines)), None

 status_lines.append(class="str">"✓ STATUS REPORT: Inputs validated successfully.")
 status_lines.append(fclass="str">" → Language : {language}")
 status_lines.append(fclass="str">" → Text : {text[:class="num">80]}{class="str">'…' if len(text) > class="num">80 else class="str">''}")
 status_lines.append(fclass="str">" → Voice ref : {voice_file}")

 class=class="str">"cmt"># --- class="num">2. Load / reuse TTS model -----------------------------------------
 try:
 tts = _get_tts()
 status_lines.append(class="str">"✓ TTS engine initialised.")
 except Exception as exc:
 err_msg = fclass="str">"✗ STATUS REPORT: Failed to initialise TTS engine — {exc}"
 status_lines.append(err_msg)
 status_lines.append(traceback.format_exc())
 return (class="str">"\n".join(status_lines)), None

 class=class="str">"cmt"># --- class="num">3. Synthesize speech ----------------------------------------------
 try:
 tts.tts_to_file(
 text=text.strip(),
 speaker_wav=voice_file, class=class="str">"cmt"># reference / clone source
 language=language,
 file_path=OUTPUT_WAV,
 )
 status_lines.append(class="str">"✓ Vocal synthesis complete.")
 except Exception as exc:
 err_msg = fclass="str">"✗ STATUS REPORT: Synthesis failed — {exc}"
 status_lines.append(err_msg)
 status_lines.append(traceback.format_exc())
 return (class="str">"\n".join(status_lines)), None

 class=class="str">"cmt"># --- class="num">4. Verify output exists -------------------------------------------
 if Path(OUTPUT_WAV).is_file():
 size_kb = Path(OUTPUT_WAV).stat().st_size / class="num">1024
 status_lines.append(fclass="str">"✓ Output saved to class="str">'{OUTPUT_WAV}' ({size_kb:.1f} KB)")
 status_lines.append(class="str">"✓ Generation complete. Play the audio below.")
 return (class="str">"\n".join(status_lines)), OUTPUT_WAV
 else:
 msg = class="str">"✗ STATUS REPORT: Output file was not created."
 status_lines.append(msg)
 return (class="str">"\n".join(status_lines)), None

class=class="str">"cmt"># ---------------------------------------------------------------------------
class=class="str">"cmt"># Gradio UI
class=class="str">"cmt"># ---------------------------------------------------------------------------
def build_app() -> gr.Blocks:
 class="str">""class="str">"Assemble and return the Gradio Blocks application."class="str">""

 with gr.Blocks(title=APP_TITLE) as app:

 class=class="str">"cmt"># ---- Header --------------------------------------------------------
 gr.Markdown(fclass="str">"class="cmtclass="str">"># {APP_TITLE}")
 gr.Markdown(fclass="str">"*{APP_SUBTITLE}*")

 with gr.Row():
 class=class="str">"cmt"># ---- Left Column: Inputs ---------------------------------------
 with gr.Column(scale=class="num">1):
 voice_upload = gr.Audio(
 label=class="str">"Upload Target Voice Sample",
 type=class="str">"filepath",
 sources=[class="str">"upload"],
 )

 language_dropdown = gr.Dropdown(
 choices=SUPPORTED_LANGUAGES,
 value=class="str">"en",
 label=class="str">"Select Target Language",
 )

 text_input = gr.Textbox(
 label=class="str">"Type the Lyrics or Sentences to Speak",
 lines=class="num">5,
 placeholder=class="str">"Enter the text you want the cloned voice to speak…",
 )

 generate_btn = gr.Button(
 class="str">"Generate Premium Vocal Clone",
 variant=class="str">"primary",
 size=class="str">"lg",
 )

 class=class="str">"cmt"># ---- Right Column: Outputs -------------------------------------
 with gr.Column(scale=class="num">1):
 status_report = gr.Textbox(
 label=class="str">"System Status Report",
 lines=class="num">8,
 interactive=False,
 )

 audio_output = gr.Audio(
 label=class="str">"Generated Cloned Audio Output",
 type=class="str">"filepath",
 )

 class=class="str">"cmt"># ---- Wire up the button click --------------------------------------
 generate_btn.click(
 fn=clone_voice,
 inputs=[voice_upload, text_input, language_dropdown],
 outputs=[status_report, audio_output],
 )

 return app

class=class="str">"cmt"># ---------------------------------------------------------------------------
class=class="str">"cmt"># Entry Point
class=class="str">"cmt"># ---------------------------------------------------------------------------
if __name__ == class="str">"__main__":
 app = build_app()
 app.launch(
 server_name=HOST,
 server_port=PORT,
 share=False, class=class="str">"cmt"># Set True temporarily for local testing via public URL
 )
