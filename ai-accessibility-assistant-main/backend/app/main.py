from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import Base, engine
from app.models.user import UserProfile

app = FastAPI(title="NeuroAdapt AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static/audio folder exists
os.makedirs("static/audio", exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create DB tables
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "NeuroAdapt Backend Running"}


# Routes
from app.routes.simplify import router as simplify_router
app.include_router(simplify_router)

from app.routes.analyze import router as analyze_router
app.include_router(analyze_router)

from app.routes.vocab import router as vocab_router
app.include_router(vocab_router)

from app.routes.progress import router as progress_router
app.include_router(progress_router)

from app.routes.tts import router as tts_router
app.include_router(tts_router)