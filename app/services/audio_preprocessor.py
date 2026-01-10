import os
import subprocess
import uuid

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)


def preprocess_audio(input_path: str) -> str:
    output_path = os.path.join(
        TEMP_DIR, f"{uuid.uuid4().hex}.wav"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        "-af","loudnorm",
        "afftdn",
        "highpass=f=200",
        "lowpass=f=3000",
        "loudnorm",
        "afftdn",
        output_path
    ]

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
    except Exception as e:
        raise RuntimeError(f"FFmpeg failed: {str(e)}")

    return output_path
