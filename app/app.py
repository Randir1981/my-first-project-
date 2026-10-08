import os
import sys
import traceback
from pathlib import Path
import gradio as gr
from TTS.api import TTS

APP_TITLE = "RK PREMIUM VOICE MAKER"
APP_SUBTITLE = "Professional Online-Grade Vocal Clone Studio Engine"
OUTPUT_WAV = "cloned_vocal_output.wav"
HOST = "0.0.0.0"
PORT = 10000
SUPPORTED_LANGUAGES = ["en", "hi", "es", "fr"]

_tts_instance = None

def get_tts() -> TTS:
    global _tts_instance
    if _tts_instance is None:
        print("[RK Voice] Initializing XTTS-v2 model (CPU mode)...")
        _tts_instance = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        print("[RK Voice] Model loaded successfully.")
    return _tts_instance

def clone_voice(voice_file: str, text: str, language: str) -> tuple[str, str | None]:
    status_lines = []

    if not text or not text.strip():
        msg = "⚠ STATUS REPORT: No text provided. Please enter lyrics or sentences to speak."
        status_lines.append(msg)
        return "\n".join(status_lines), None

    if not voice_file or not Path(voice_file).exists():
        msg = "⚠ STATUS REPORT: No valid voice sample uploaded. Please upload a target voice sample."
        status_lines.append(msg)
        return "\n".join(status_lines), None

    status_lines.append("✓ STATUS REPORT: Inputs validated successfully.")
    status_lines.append(f"✓ Language: {language}")
    status_lines.append(f"✓ Text: '{text[:80]}...' if len(text) > 80 else text")
    status_lines.append(f"✓ Voice ref: {voice_file}")

    try:
        tts = get_tts()
        status_lines.append("✓ TTS engine initialized.")
    except Exception as exc:
        err_msg = f"✕ STATUS REPORT: Failed to initialise TTS engine - {exc}"
        status_lines.append(err_msg)
        status_lines.append(traceback.format_exc())
        return "\n".join(status_lines), None

    try:
        tts.tts_to_file(
            text=text.strip(),
            speaker_wav=voice_file,
            language=language,
            file_path=OUTPUT_WAV
        )
        status_lines.append("✓ Vocal synthesis complete.")
    except Exception as exc:
        err_msg = f"✕ STATUS REPORT: Synthesis failed - {exc}"
        status_lines.append(err_msg)
        status_lines.append(traceback.format_exc())
        return "\n".join(status_lines), None

    if Path(OUTPUT_WAV).is_file():
        size_kb = Path(OUTPUT_WAV).stat().st_size / 1024
        status_lines.append(f"✓ Output saved to '{OUTPUT_WAV}' ({size_kb:.1f} KB)")
        status_lines.append("✓ Generation complete. Play the audio below.")
        return "\n".join(status_lines), OUTPUT_WAV
    else:
        msg = "✕ STATUS REPORT: Output file was not created."
        status_lines.append(msg)
        return "\n".join(status_lines), None

def build_app() -> gr.Blocks:
    with gr.Blocks(title=APP_TITLE) as app:
        gr.Markdown(f"# **{APP_TITLE}**")
        gr.Markdown(f"### ***{APP_SUBTITLE}***")

        with gr.Row():
            with gr.Column(scale=1):
                voice_upload = gr.Audio(
                    label="Upload Target Voice Sample",
                    type="filepath",
                    sources=["upload"]
                )

                language_dropdown = gr.Dropdown(
                    choices=SUPPORTED_LANGUAGES,
                    value="en",
                    label="Select Target Language"
                )

                text_input = gr.Textbox(
                    label="Type the Lyrics or Sentences to Speak",
                    lines=5,
                    placeholder="Enter the text you want the cloned voice to speak..."
                )

                generate_btn = gr.Button(
                    "Generate Premium Vocal Clone",
                    variant="primary",
                    size="lg"
                )

            with gr.Column(scale=1):
                status_report = gr.Textbox(
                    label="System Status Report",
                    lines=8,
                    interactive=False
                )

                audio_output = gr.Audio(
                    label="Generated Cloned Audio Output",
                    type="filepath"
                )

        generate_btn.click(
            fn=clone_voice,
            inputs=[voice_upload, text_input, language_dropdown],
            outputs=[status_report, audio_output]
        )

    return app

if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name=HOST,
        server_port=PORT,
        share=False
    )


