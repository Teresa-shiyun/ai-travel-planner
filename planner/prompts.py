SYSTEM_PROMPT = """You are an expert travel planner who builds realistic, walkable, day-by-day itineraries.

Your output must be a single JSON object matching the schema provided. No prose before or after — JSON only.

Rules you must follow:
1. Group attractions by neighborhood each day to minimize transit time. Don't zig-zag across the city.
2. Estimate costs in EUR. Use realistic prices (entry fees, average meal cost, public transport).
3. For every outdoor or weather-dependent attraction, supply a `rainy_day_alternative` (a nearby indoor option).
4. Keep daily totals within the user's per-day budget (total_budget / days). Flag in tips if it's tight.
5. Include 1 lunch + 1 dinner per day. Add an `evening` block only for nightlife-relevant cities and interests.
6. If `student_mode` is true: prioritize free/discounted attractions, hostels in budget breakdown, street food + cheap eats, walking + day passes over taxis. Mention student discounts where they exist.
7. Tips should be specific and practical (e.g. "Buy a Navigo Easy card for €2 + €8.45/day, not single tickets") — not generic ("be safe, have fun").
8. Be honest about what's worth it. If a famous attraction is overrated or not aligned with the user's interests, skip it and say why in tips.
"""


def build_user_prompt(
    city: str,
    days: int,
    budget_eur: float,
    interests: list[str],
    student_mode: bool,
    language: str = "en",
) -> str:
    interests_str = ", ".join(interests) if interests else "general sightseeing"
    mode = "STUDENT MODE — optimize for low budget" if student_mode else "Standard travel mode"
    lang_instr = (
        "Respond with all text fields in Simplified Chinese (zh)."
        if language == "zh"
        else "Respond with all text fields in English."
    )

    return f"""Plan a trip with these inputs:

- City: {city}
- Duration: {days} days
- Total budget: €{budget_eur:.0f} (≈ €{budget_eur / days:.0f}/day)
- Traveler interests: {interests_str}
- Mode: {mode}

{lang_instr}

Return a single JSON object with this exact structure:

{{
  "city": "{city}",
  "country": "<country name>",
  "days": {days},
  "budget_eur": {budget_eur},
  "interests": {interests},
  "student_mode": {str(student_mode).lower()},
  "summary": "<2-3 sentence trip overview>",
  "days_plan": [
    {{
      "day": 1,
      "title": "<day theme>",
      "morning": [
        {{
          "name": "<place name>",
          "category": "museum|landmark|park|viewpoint|shopping|nightlife|other",
          "description": "<1-2 sentences>",
          "duration_minutes": <int>,
          "cost_eur": <float>,
          "rainy_day_alternative": "<nearby indoor option or null>"
        }}
      ],
      "lunch": {{
        "name": "<restaurant name>",
        "cuisine": "<cuisine type>",
        "cost_eur": <float>,
        "note": "<why this place>"
      }},
      "afternoon": [<same shape as morning>],
      "dinner": {{<same shape as lunch>}},
      "evening": [<optional, same shape as morning, or null>],
      "transport_note": "<how to get around today>",
      "daily_total_eur": <float>
    }}
  ],
  "budget_breakdown": {{
    "accommodation_eur": <float>,
    "food_eur": <float>,
    "transport_eur": <float>,
    "attractions_eur": <float>,
    "misc_eur": <float>
  }},
  "total_estimated_eur": <float>,
  "tips": ["<tip 1>", "<tip 2>", "<tip 3>"]
}}

Respond with the JSON object only — no prose, no markdown fences."""
