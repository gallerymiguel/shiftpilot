from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def generate_cover_message(
    store_id: int,
    date: str,
    shift_type: str,
    recommendations: list[dict],
) -> str:
    top_candidate = recommendations[0]["name"] if recommendations else "no one"

    prompt = f"""
You are an assistant for a retail workforce scheduling system.

A manager needs to send a short group message asking for coverage.

Shift details:
- Store ID: {store_id}
- Date: {date}
- Shift type: {shift_type}

Top recommendation:
- {top_candidate}

Other candidates:
{recommendations}

Write a short, professional text message to employees asking for coverage.
Keep it concise and natural.
Do not mention internal priority numbers.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text.strip()