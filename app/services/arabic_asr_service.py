import torch
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


class ArabicASRService:
    """
    Arabic speech-to-text using pretrained wav2vec2 model.
    """

    def __init__(self):
        # One of the best Arabic ASR models available
        self.model_name = "jonatasgrosman/wav2vec2-large-xlsr-53-arabic"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = None
        self.model = None

    def _load_model(self):
        if self.model is None:
            print(f"[Arabic ASR] Loading model: {self.model_name}")
            self.processor = Wav2Vec2Processor.from_pretrained(self.model_name)
            self.model = Wav2Vec2ForCTC.from_pretrained(self.model_name).to(self.device)

    def transcribe(self, audio_path: str) -> dict:
        """
        Transcribe Arabic speech into Arabic text.
        """
        self._load_model()

        # Load audio (16kHz mono)
        audio, sr = librosa.load(audio_path, sr=16000)

        inputs = self.processor(
            audio,
            sampling_rate=16000,
            return_tensors="pt",
            padding=True
        )

        input_values = inputs.input_values.to(self.device)

        with torch.no_grad():
            logits = self.model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.decode(predicted_ids[0])

        return {
            "language": "ar",
            "text": transcription.strip()
        }


# Singleton instance
arabic_asr_service = ArabicASRService()
