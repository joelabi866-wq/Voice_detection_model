import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application configuration.
    """

    def __init__(self) -> None:
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


# ✅ THIS NAME MUST EXIST
settings = Settings()
