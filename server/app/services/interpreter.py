import json

from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def interpret_message(message: str) -> dict:
    prompt = f"""
You are an assistant for a workforce scheduling system.

Interpret the employee message and classify its operational meaning.

Possible intents:
- call_out
- late
- shift_swap
- availability_change
- other

Return only valid JSON with this exact shape:
{{
  "intent": "call_out",
  "urgency": "high",
  "notes": "short explanation"
}}

Message:
{message}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    text = response.output_text.strip()
    print("RAW INTERPRETER OUTPUT:", text)

    # Remove markdown code fences if the model added them
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "intent": "other",
            "urgency": "unknown",
            "notes": f"Interpreter returned non-JSON output: {text}",
        }