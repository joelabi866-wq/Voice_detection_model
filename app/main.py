from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.generation import router as generation_router

app = FastAPI(title="AI Description Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generation_router)


@app.get("/")
def root():
    return {"status": "running"}
