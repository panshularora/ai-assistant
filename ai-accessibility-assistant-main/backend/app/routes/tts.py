from fastapi import APIRouter
from pydantic import BaseModel
from gtts import gTTS
import uuid
import os

router = APIRouter()


class TTSRequest(BaseModel):
    text: str
    slow: bool = False


@router.post("/tts")
def generate_tts(request: TTSRequest):

    # Generate unique filename
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join("static", "audio", filename)

    # Generate speech
    tts = gTTS(text=request.text, lang="en", slow=request.slow)
    tts.save(filepath)

    return {
        "audio_url": f"/static/audio/{filename}",
        "filename": filename
    }