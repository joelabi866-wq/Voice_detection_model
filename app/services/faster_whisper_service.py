from faster_whisper import WhisperModel


class FasterWhisperService:
    def __init__(
        self,
        model_size: str = "medium",
        device: str = "cpu",       # use "cuda" if you have GPU
        compute_type: str = "int8" # int8 = faster on CPU, float16 on GPU
    ):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None  # lazy load

    def _load_model(self):
        if self.model is None:
            print(f"[Faster-Whisper] Loading model: {self.model_size}")
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type
            )

    def detect_language(self, audio_path: str) -> dict:
        """
        Fast language detection.
        """
        self._load_model()

        segments, info = self.model.transcribe(
            audio_path,
            task="transcribe",
            beam_size=1
        )

        return {
            "language": info.language,
            "confidence": info.language_probability
        }

    def transcribe_to_english(self, audio_path: str) -> dict:
        """
        Full transcription with translation to English.
        """
        self._load_model()

        segments, info = self.model.transcribe(
            audio_path,
            task="translate",
            beam_size=5
        )

        text = " ".join(segment.text for segment in segments).strip()

        return {
            "language": info.language,
            "text": text
        }


# Singleton instance (same pattern as other services)
faster_whisper_model = FasterWhisperService()
