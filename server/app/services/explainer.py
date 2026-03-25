from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def generate_cover_explanation(
    shift_id: int,
    store_id: int,
    date: str,
    shift_type: str,
    recommendations: list[dict],
    policies: list[str] | None = None,
) -> str:
    if not recommendations:
        return "No replacement candidates were found for this shift."

    policy_text = "\n".join(f"- {policy}" for policy in (policies or []))

    prompt = f"""
You are an operations assistant for a retail workforce scheduling system.

A shift needs coverage because an employee called out.

Shift info:
Shift ID: {shift_id}
Store ID: {store_id}
Date: {date}
Shift type: {shift_type}

Relevant staffing policies:
{policy_text if policy_text else "- No policies retrieved."}

Ranked candidates:
{recommendations}

Explain to a store manager who should cover the shift and why.
Keep the explanation short and professional.
Use the retrieved policy context when relevant.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text.strip()