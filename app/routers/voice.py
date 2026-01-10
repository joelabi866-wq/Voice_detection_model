from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

from app.services.language_router import language_router

router = APIRouter(
    prefix="/api/v1/whisper",
    tags=["Speech-to-Text"]
)

TEMP_AUDIO_DIR = "audio"
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(status_code=400, detail="No audio file provided")

    file_path = os.path.join(
        TEMP_AUDIO_DIR,
        f"{uuid.uuid4()}_{file.filename}"
    )

    # Save uploaded audio
    with open(file_path, "wb") as f:
        f.write(await file.read())
    print("voice hiii")
    try:
        # 🔥 This is now routed automatically to best model
        result = language_router.transcribe(file_path)

        return {
            "success": True,
            "detected_language": result.get("language"),
            "text": result.get("text")
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
