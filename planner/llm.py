import json
import os
import re
from typing import Optional

import anthropic
from pydantic import ValidationError

from planner.models import Itinerary
from planner.prompts import SYSTEM_PROMPT, build_user_prompt

DEFAULT_MODEL = "claude-opus-4-7"


class GenerationError(Exception):
    pass


def _strip_json_fences(text: str) -> str:
    fenced = re.match(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", text, re.DOTALL)
    if fenced:
        return fenced.group(1)
    return text.strip()


def generate_itinerary(
    city: str,
    days: int,
    budget_eur: float,
    interests: list[str],
    student_mode: bool = False,
    language: str = "en",
    api_key: Optional[str] = None,
    model: str = DEFAULT_MODEL,
) -> Itinerary:
    """Generate a travel itinerary via the Claude API.

    The Anthropic API key is read from the `api_key` argument or the
    ANTHROPIC_API_KEY environment variable. Raises GenerationError if no key
    is set, the API call fails, or the response can't be parsed into the
    Itinerary schema.
    """
    key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise GenerationError(
            "No Anthropic API key found. Set ANTHROPIC_API_KEY or pass api_key."
        )

    client = anthropic.Anthropic(api_key=key)

    user_prompt = build_user_prompt(
        city=city,
        days=days,
        budget_eur=budget_eur,
        interests=interests,
        student_mode=student_mode,
        language=language,
    )

    try:
        response = client.messages.create(
            model=model,
            max_tokens=8192,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
    except anthropic.APIError as exc:
        raise GenerationError(f"Claude API error: {exc}") from exc

    raw_text = next(
        (block.text for block in response.content if block.type == "text"), ""
    )
    if not raw_text:
        raise GenerationError("Claude returned an empty response.")

    cleaned = _strip_json_fences(raw_text)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise GenerationError(
            f"Claude did not return valid JSON: {exc}\n\nRaw response:\n{raw_text[:500]}"
        ) from exc

    try:
        return Itinerary.model_validate(data)
    except ValidationError as exc:
        raise GenerationError(
            f"Response did not match the Itinerary schema:\n{exc}"
        ) from exc
