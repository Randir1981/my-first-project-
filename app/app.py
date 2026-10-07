import os
import uuid
import torch
import gradio as gr
from TTS.api import TTS


# ============================================================
# RK PREMIUM VOICE MAKER
# Local XTTS-v2 Voice Cloning
# ============================================================

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"

# Automatically use NVIDIA GPU when available.
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("=" * 60)
print("RK PREMIUM VOICE MAKER")
print("=" * 60)
print(f"Device: {DEVICE}")
print("Loading XTTS-v2 model...")
print("The first startup may take a while because the model is downloaded.")
print("=" * 60)


# Load the model ONCE when the application starts.
try:
    tts = TTS(MODEL_NAME).to(DEVICE)

    MODEL_STATUS = (
        f"XTTS-v2 loaded successfully.\n"
        f"Device: {DEVICE}"
    )

    print(MODEL_STATUS)

except Exception as e:
    tts = None

    MODEL_STATUS = (
        "XTTS-v2 failed to load.\n"
        f"Error: {str(e)}"
    )

    print(MODEL_STATUS)


# ============================================================
# VOICE CLONING FUNCTION
# ============================================================

def clone_voice(audio_file, text_to_speak, language_choice):

    # Check that model loaded correctly.
    if tts is None:
        return (
            "ERROR: XTTS-v2 could not be loaded.\n\n"
            f"{MODEL_STATUS}",
            None
        )

    # Check audio.
    if not audio_file:
        return (
            "Please upload a voice sample first.",
            None
        )

    # Check text.
    if not text_to_speak or not text_to_speak.strip():
        return (
            "Please enter some text to speak.",
            None
        )

    try:
        # Make a unique filename so multiple generations
        # don't overwrite each other.
        filename = f"cloned_voice_{uuid.uuid4().hex}.wav"

        output_path = os.path.abspath(filename)

        # Generate cloned speech.
        tts.tts_to_file(
            text=text_to_speak.strip(),
            speaker_wav=audio_file,
            language=language_choice,
            file_path=output_path
        )

        # Make sure the file actually exists.
        if not os.path.exists(output_path):
            return (
                "Voice generation failed: output WAV was not created.",
                None
            )

        return (
            "Voice cloning successful!\n"
            f"Device: {DEVICE}\n"
            f"Output: {output_path}",
            output_path
        )

    except Exception as e:

        return (
            "Voice generation failed.\n\n"
            f"Error: {str(e)}",
            None
        )


# ============================================================
# GRADIO USER INTERFACE
# ============================================================

with gr.Blocks(
    theme=gr.themes.Soft(),
    title="RK Premium Voice Maker"
) as demo:

    gr.Markdown(
        """
        # 🎙️ RK PREMIUM VOICE MAKER

        ### Professional XTTS-v2 Voice Clone Studio

        Upload a clean voice sample, enter your text,
        select a language, and generate speech using the
        cloned voice.
        """
    )

    gr.Markdown(
        f"""
        **Engine Status:** `{MODEL_STATUS}`

        **Processing Device:** `{DEVICE}`
        """
    )

    with gr.Row():

        with gr.Column():

            vocal_sample = gr.Audio(
                label="Upload Target Voice Sample",
                type="filepath"
            )

            language_choice = gr.Dropdown(
                label="Select Target Language",
                choices=[
                    ("English", "en"),
                    ("Hindi", "hi"),
                    ("Spanish", "es"),
                    ("French", "fr"),
                    ("German", "de"),
                    ("Italian", "it"),
                    ("Portuguese", "pt"),
                    ("Polish", "pl"),
                    ("Turkish", "tr"),
                    ("Russian", "ru"),
                    ("Dutch", "nl"),
                    ("Czech", "cs"),
                    ("Arabic", "ar"),
                    ("Chinese", "zh-cn"),
                    ("Japanese", "ja"),
                    ("Hungarian", "hu"),
                    ("Korean", "ko"),
                ],
                value="en"
            )

            input_text = gr.Textbox(
                label="Text to Speak",
                lines=5,
                placeholder="Enter the text you want the cloned voice to say..."
            )

            submit_btn = gr.Button(
                "🎙️ Generate Premium Voice Clone",
                variant="primary",
                size="lg"
            )

        with gr.Column():

            status_output = gr.Textbox(
                label="System Status",
                lines=6
            )

            audio_output = gr.Audio(
                label="Generated Cloned Audio",
                type="filepath"
            )


    # Connect button to cloning function.
    submit_btn.click(
        fn=clone_voice,
        inputs=[
            vocal_sample,
            input_text,
            language_choice
        ],
        outputs=[
            status_output,
            audio_output
        ]
    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "10000")),
        show_error=True
    )
