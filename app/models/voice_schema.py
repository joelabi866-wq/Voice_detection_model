from pydantic import BaseModel, Field
from typing import Optional


class VoiceTranscriptionResponse(BaseModel):
    success: bool = Field(..., description="Transcription status")
    detected_language: Optional[str] = Field(
        None, description="Detected spoken language"
    )
    text: Optional[str] = Field(
        None, description="Transcribed text in English"
    )
    error: Optional[str] = Field(
        None, description="Error message if transcription fails"
    )
