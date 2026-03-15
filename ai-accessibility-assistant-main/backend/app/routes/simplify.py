from fastapi import APIRouter
from pydantic import BaseModel
from app.services.simplifier import simplify_text
from app.services.cognitive_load import calculate_cognitive_load
from gtts import gTTS
import uuid
import os
from app.services.user_profile import update_user_profile
from app.services.accessibility import (
    apply_dyslexia_formatting,
    generate_audio_payload
)

router = APIRouter()


class SimplifyRequest(BaseModel):
    text: str
    level: int | None = None
    user_id: str | None = None
    profile: str | None = "default"
    enable_dyslexia_support: bool = True
    enable_audio: bool = True


@router.post("/simplify")

def simplify(request: SimplifyRequest):

    # 1️⃣ Analyze original
    original_analysis = calculate_cognitive_load(request.text)
    original_score = original_analysis["cognitive_load_score"]

    # 2️⃣ Auto level
    if request.level is None:
        if original_score < 30:
            level = 3
        elif original_score < 60:
            level = 2
        else:
            level = 1
    else:
        level = request.level

    # Profile override
    if request.profile == "focus":
        level = 1
    elif request.profile == "easy_read":
        level = 1
    elif request.profile == "academic":
        level = 3

    # 3️⃣ Simplify
    simplified_output = simplify_text(request.text, level)

    if isinstance(simplified_output, dict):
        simplified_text = simplified_output.get("simplified_text", "")
    else:
        simplified_text = simplified_output

    # 4️⃣ Analyze simplified
    simplified_analysis = calculate_cognitive_load(simplified_text)
    simplified_score = simplified_analysis["cognitive_load_score"]

    reduction = original_score - simplified_score

    # 5️⃣ Overload detection
    overload_warning = None
    isolation_mode = False

    if original_score >= 70:
        overload_warning = "This text may cause cognitive overload."
        isolation_mode = True

    # 6️⃣ Dyslexia Formatting
    dyslexia_view = None
    if request.enable_dyslexia_support:
        dyslexia_view = apply_dyslexia_formatting(simplified_text)

    # 7️⃣ Adaptive Audio Mode
    audio_payload = None
    if request.enable_audio:
        audio_payload = generate_audio_payload(simplified_text)

    # 8️⃣ Save progress
    if request.user_id:
        update_user_profile(
            user_id=request.user_id,
            level=level,
            score=simplified_score
        )

    impact_percentage = 0
    if original_score > 0:
        impact_percentage = round((reduction / original_score) * 100, 1)



    # Generate TTS automatically for simplified text
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join("static", "audio", filename)

    tts = gTTS(text=simplified_text, lang="en", slow=False)
    tts.save(filepath)

    audio_url = f"/static/audio/{filename}"

    return {
        "auto_selected_level": level,
        "profile_used": request.profile,
        "overload_warning": overload_warning,
        "isolation_mode": isolation_mode,
        "original_analysis": original_analysis,
        "simplified_text": simplified_text,
        "dyslexia_optimized_text": dyslexia_view,
        "audio_mode": audio_payload,
        "simplified_analysis": simplified_analysis,
        "cognitive_load_reduction": round(reduction, 2),
        "impact_summary": f"Cognitive load reduced by {round(reduction, 2)} points ({impact_percentage}% improvement)",
        "audio_file": audio_url
    }
