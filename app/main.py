from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.generation import router as generation_router
from app.routers.voice import router as voice_router


app = FastAPI(title="AI Description Generator")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(generation_router)
app.include_router(voice_router)

# Health check
@app.get("/")
def root():
    return {"status": "running"}
