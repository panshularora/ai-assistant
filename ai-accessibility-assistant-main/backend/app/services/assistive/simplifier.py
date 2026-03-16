import os
import json
from typing import Any, Dict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# Groq is OpenAI‑compatible; we just point the OpenAI client at Groq.
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def simplify_text(text: str, level: int) -> Dict[str, Any]:
    """Call Groq (OpenAI‑style) to simplify text for neurodiverse learners."""
    system_prompt = """
You are an AI accessibility assistant for neurodiverse learners.

Simplify the given text based on the level:

Level 1 = very simple, short sentences.
Level 2 = moderately simplified.
Level 3 = lightly simplified.

Return ONLY valid JSON in this exact format:

{
  "simplified_text": "...",
  "bullet_points": ["..."],
  "definitions": {"term": "..."},
  "step_by_step_explanation": ["step 1", "step 2"]
}

Do not return anything outside JSON.
"""

    user_prompt = f"""
Simplification level: {level}

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content or ""

    try:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        return json.loads(cleaned)
    except Exception:
        return {
            "simplified_text": content,
            "bullet_points": [],
            "definitions": {},
            "step_by_step_explanation": [],
        }