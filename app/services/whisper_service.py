import whisper
import os


class WhisperService:
    def __init__(self, model_size: str = "medium"):
        """
        model_size options:
        tiny, base, small, medium, large
        medium = good balance of accuracy and speed
        """
        self.model_size = model_size
        self.model = None  # lazy load

    def _load_model(self):
        if self.model is None:
            print(f"[Whisper] Loading model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)

    def detect_language(self, audio_path: str) -> dict:
        """
        Fast language detection using Whisper.
        """
        self._load_model()

        # Use short decode for detection only
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        _, probs = self.model.detect_language(mel)

        detected_lang = max(probs, key=probs.get)

        return {
            "language": detected_lang,
            "confidence": probs[detected_lang]
        }

    def transcribe_to_english(self, audio_path: str) -> dict:
        """
        Full transcription with auto language detection and translation to English.
        """
        self._load_model()

        result = self.model.transcribe(
            audio_path,
            task="translate",       # always output English
            temperature=0.0,
            beam_size=5,
            best_of=5
        )

        return {
            "language": result.get("language"),
            "text": result.get("text", "").strip()
        }


# Singleton instance (same style as ai_generator)
whisper_model = WhisperService()
