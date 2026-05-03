# AI Travel Itinerary Planner

> Generate personalized multi-day travel itineraries with budget estimates, restaurant picks, rainy-day alternatives, and downloadable PDFs — powered by Claude.

A Streamlit web app that turns four inputs (city, days, budget, interests) into a structured day-by-day plan: morning/afternoon/evening attractions grouped by neighborhood, lunch and dinner picks, transit notes, a budget breakdown, and a one-click PDF export. Includes a **Student Mode** that biases toward free attractions, hostels, and cheap eats — built originally as a *Europe Weekend Trip Planner for Students*.

---

## Features

- **Structured day plans** — morning / lunch / afternoon / dinner / evening, grouped by neighborhood to avoid zig-zagging
- **Budget breakdown** — accommodation, food, transport, attractions, misc — with delta vs. user budget
- **Google Maps links** for every attraction
- **Rainy-day alternatives** for outdoor stops
- **Restaurant picks** with cuisine, price, and a one-line "why this place" note
- **Student Mode** — toggles a low-budget bias (free museums, hostels, street food)
- **PDF export** via ReportLab — recruiter-ready trip plan
- **Multi-language** — UI and itinerary content in English or Simplified Chinese
- **Demo Mode** — full UI works without an API key (pre-built Paris weekend itinerary), so you can try the app instantly

---

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend + backend | **Streamlit** | Single-file UI, free hosting on Streamlit Cloud, fastest path to a working demo |
| LLM | **Anthropic Claude** (`claude-sonnet-4-6` default, `opus-4-7` / `haiku-4-5` selectable) | Strong structured output, follows JSON schema reliably |
| Validation | **Pydantic v2** | Type-safe parse of LLM JSON; catches malformed outputs before they hit the UI |
| PDF | **ReportLab** | Pure-Python, no system dependencies |
| Config | **python-dotenv** | Standard `.env` pattern for the API key |

---

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/ai-travel-planner.git
cd ai-travel-planner
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 — the app launches in **Demo mode** (no API key required) showing a Paris 2-day student itinerary. Toggle Demo mode off in the sidebar to plan any city.

### Using the Claude API

To generate live itineraries, you need an Anthropic API key:

1. Get a key at [console.anthropic.com](https://console.anthropic.com)
2. Either:
   - paste it into the sidebar (kept in session memory only), or
   - copy `.env.example` to `.env` and add the key there

Cost per itinerary is roughly **$0.01–0.05** depending on the model — Sonnet 4.6 is the default sweet spot.

---

## Architecture

```
ai-travel-planner/
├── app.py                  # Streamlit UI — form inputs, day tabs, PDF download
├── planner/
│   ├── models.py           # Pydantic schema: Itinerary, DayPlan, Place, Meal, BudgetBreakdown
│   ├── prompts.py          # System + user prompt templates
│   ├── llm.py              # Claude API call + JSON parsing + schema validation
│   ├── mock_data.py        # Pre-built Paris itinerary for Demo mode
│   ├── pdf_export.py       # ReportLab PDF generation
│   └── i18n.py             # English / Chinese UI strings
├── requirements.txt
├── .env.example
└── README.md
```

The pipeline:

1. User fills the form (city, days, budget, interests, student toggle, language)
2. `prompts.build_user_prompt()` renders the request as a strict JSON-shape spec
3. `llm.generate_itinerary()` calls Claude, strips any markdown fences, parses JSON
4. `Itinerary.model_validate()` enforces the schema (raises `GenerationError` on mismatch)
5. The Streamlit UI renders day tabs, a budget breakdown, Google Maps links, and a PDF download button

Schema validation matters: LLMs occasionally drop a field or wrap output in markdown fences. Pydantic catches both at the boundary, so the UI never has to defend against malformed AI output.

---

## Example Output

For *Paris, 2 days, €250, art + history + cafes, student mode*:

```
Day 1 — Classic Paris: Louvre & Latin Quarter
  Morning:    Louvre Museum (€22, 3h, free for under-26 EU)
  Lunch:      L'As du Fallafel (€10, Marais)
  Afternoon:  Notre-Dame exterior + Shakespeare and Co + Latin Quarter walk
  Dinner:     Le Petit Vendôme (€18, French bistro)
  Transport:  All walking — central Paris is compact

Day 2 — Montmartre & the Seine
  Morning:    Sacré-Cœur + Montmartre (€8 dome ticket)
  Lunch:      Le Relais Gascon (€15, giant goat-cheese salads)
  Afternoon:  Musée d'Orsay + Seine sunset walk
  Dinner:     Bouillon Pigalle (€20, traditional French)
  Evening:    Eiffel Tower from Trocadéro (free, hourly sparkle)

Budget: €250 (Accom €120 · Food €63 · Transit €17 · Attractions €46 · Misc €4)

Tips:
  - Under 26 EU resident? Most national museums are free. Bring ID.
  - Buy a Navigo Easy card (€2 + €8.45/day) — way cheaper than singles.
  - Skip Bateaux Mouches — the free Seine walk gives you the same view.
```

---

## Design Notes

- **Demo mode is first-class**, not an afterthought. Recruiters can see the full UI, exports, and structure without me paying for their API calls.
- **Schema-validated LLM output**. Every Claude response is parsed with Pydantic. Garbage in → clean error out, never a half-broken UI.
- **Budget transparency**. The breakdown is shown vs. the user's stated budget with a colored delta — if Claude over-budgets, you see it immediately.
- **Honest about limitations**. The app is a *plan generator*, not a booking engine. It uses Claude's training-data knowledge of restaurants and attractions; it does not query Google Places or live availability. Famous spots that closed last week may still appear. README ships with this disclaimer rather than hiding it.

---

## Future Improvements

- Live restaurant data via Google Places API (would replace the "famous spots that closed" caveat)
- Real-time hotel/hostel pricing via Booking.com or Hostelworld API
- Save itineraries to a database so users can revisit / share
- Stripe-protected hosted version with API key abstracted away
- Unit tests for the schema validator + a few golden-output tests for the prompt
- Streaming generation so users see the itinerary build day-by-day

---

## License

MIT — see [LICENSE](LICENSE).

---

## CV one-liner

> Built an AI travel itinerary planner (Python / Streamlit / Claude API) that generates personalized multi-day routes, budget breakdowns, and downloadable trip plans from four user inputs. Pydantic-validated LLM output, multi-language UI, PDF export, runnable demo without an API key.
