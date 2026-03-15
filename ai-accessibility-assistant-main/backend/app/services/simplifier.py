import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def simplify_text(text: str, level: int):

    system_prompt = """
You are an AI accessibility assistant for neurodiverse learners.

Simplify the given text based on the level:

Level 1 = very simple, short sentences.
Level 2 = moderately simplified.
Level 3 = lightly simplified.

Return ONLY valid JSON in this format:

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
        model="moonshotai/kimi-k2-instruct-0905",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "simplified_text": content,
            "bullet_points": [],
            "definitions": {}
        }