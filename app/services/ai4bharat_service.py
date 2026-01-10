import torch
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


class AI4BharatService:
    """
    ASR service for Indian languages using pretrained wav2vec2 models.
    """

    def __init__(self):
        self.models = {}  # cache loaded models per language

        # Map language code → HuggingFace model
        self.model_map = {
            "hi": "ai4bharat/indicwav2vec-hindi",
            "ta": "ai4bharat/indicwav2vec-tamil",
            "ml": "ai4bharat/indicwav2vec-malayalam",
            "te": "ai4bharat/indicwav2vec-telugu",
            "kn": "ai4bharat/indicwav2vec-kannada",
            "bn": "ai4bharat/indicwav2vec-bengali",
            "mr": "ai4bharat/indicwav2vec-marathi",
        }

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def _load_model(self, lang: str):
        if lang not in self.models:
            if lang not in self.model_map:
                raise ValueError(f"No AI4Bharat model for language: {lang}")

            model_name = self.model_map[lang]
            print(f"[AI4Bharat] Loading model for {lang}: {model_name}")

            processor = Wav2Vec2Processor.from_pretrained(model_name)
            model = Wav2Vec2ForCTC.from_pretrained(model_name).to(self.device)

            self.models[lang] = (processor, model)

        return self.models[lang]

    def transcribe(self, audio_path: str, lang: str) -> dict:
        """
        Transcribe Indian language audio to native text.
        """
        processor, model = self._load_model(lang)

        # Load audio as 16kHz mono
        audio, sr = librosa.load(audio_path, sr=16000)

        inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
        input_values = inputs.input_values.to(self.device)

        with torch.no_grad():
            logits = model(input_values).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(predicted_ids[0])

        return {
            "language": lang,
            "text": transcription.strip()
        }


# Singleton instance
ai4bharat_service = AI4BharatService()
