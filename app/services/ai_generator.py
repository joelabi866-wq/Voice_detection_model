import asyncio
from typing import Any
from openai import OpenAI
from app.config import settings


class AIGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def _build_prompt(self, entity_type: str, fields: dict) -> str:
        lines = [f"Generate a professional {entity_type} description:"]
        for k, v in fields.items():
            if v is not None:
                lines.append(f"{k}: {v}")
        return "\n".join(lines)

    async def generate(self, entity_type: str, fields: Any) -> str:
        if hasattr(fields, "dict"):
            fields = fields.dict()

        prompt = self._build_prompt(entity_type, fields)

        response = await asyncio.to_thread(
            self.client.chat.completions.create,
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional technical writer."},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content.strip()


ai_generator = AIGenerator()
