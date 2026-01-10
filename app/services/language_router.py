from app.services.faster_whisper_service import faster_whisper_model
from app.services.whisper_service import whisper_model
from app.services.ai4bharat_service import ai4bharat_service
from app.services.arabic_asr_service import arabic_asr_service
from app.services.korean_asr_service import korean_asr_service


INDIC_LANGS = {
    "hi", "ta", "ml", "te", "kn",
    "bn", "mr", "gu", "pa", "or",
    "as", "ur"
}


class LanguageRouter:

    def transcribe(self, audio_path: str) -> dict:
        print("========== ROUTER START ==========")

        # Step 1: Detect language using Faster-Whisper
        detection = faster_whisper_model.detect_language(audio_path)
        lang = detection.get("language")

        print(f"[Router] Detected language: {lang}")

        # Step 2: Route based on language
        try:
            if lang in INDIC_LANGS:
                print("[Router] Using AI4Bharat")
                result = ai4bharat_service.transcribe(audio_path, lang)
                return {"language": lang, "text": result["text"]}

            elif lang == "ar":
                print("[Router] Using Arabic ASR")
                return arabic_asr_service.transcribe(audio_path)

            elif lang == "ko":
                print("[Router] Using Korean ASR")
                return korean_asr_service.transcribe(audio_path)

            else:
                print("[Router] Using Whisper (translate to English)")
                return whisper_model.transcribe_to_english(audio_path)

        finally:
            print("========== ROUTER END ==========")


language_router = LanguageRouter()
