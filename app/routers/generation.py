from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    GenerationRequest,
    GenerationResponse,
    GenerationMode,
)
from app.services.ai_generator import ai_generator

router = APIRouter(prefix="/api", tags=["Generation"])


@router.post("/generate", response_model=GenerationResponse)
async def generate_description(request: GenerationRequest):
    if request.generation_mode != GenerationMode.ai:
        raise HTTPException(400, "Only AI mode supported")

    description = await ai_generator.generate(
        request.entity_type.value,
        request.fields
    )

    return GenerationResponse(
        success=True,
        generated_description=description,
        generation_mode=GenerationMode.ai,
    )
