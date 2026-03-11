from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def generate_cover_explanation(
    shift_id: int,
    store_id: int,
    date: str,
    shift_type: str,
    recommendations: list
):

    if not recommendations:
        return "No replacement candidates were found for this shift."

    prompt = f"""
You are an operations assistant for a retail workforce scheduling system.

A shift needs coverage because an employee called out.

Shift info:
Shift ID: {shift_id}
Store ID: {store_id}
Date: {date}
Shift type: {shift_type}

Ranked candidates:
{recommendations}

Explain to a store manager who should cover the shift and why.
Keep the explanation short and professional.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text