# AI Travel Itinerary Planner

AI Travel Itinerary Planner is a Streamlit app that creates multi-day travel plans from a few inputs: city, trip length, budget, interests and language. It includes a built-in Paris demo itinerary, so the UI can be tested without an API key.

## Why I Built It

I built this to practise LLM application structure in Python: prompt design, schema validation, UI rendering and PDF export. The original use case was planning budget-friendly short trips for students in Europe.

## What It Does

- Collects city, trip length, budget, interests and student-mode inputs.
- Runs in demo mode without external credentials.
- Calls the Anthropic API for live itinerary generation when configured.
- Validates generated itinerary data with Pydantic models.
- Shows day-by-day plans, meals, travel notes and rainy-day alternatives.
- Adds Google Maps links for places.
- Exports the generated itinerary as a PDF.

## Tech Stack

- Python
- Streamlit
- Anthropic SDK
- Pydantic v2
- ReportLab
- python-dotenv

## Current Status

Working Streamlit prototype. Demo mode is ready for local testing. Live generation requires an Anthropic API key and should still be reviewed before travel planning.

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal. Demo mode is enabled by default.

Optional `.env`:

```bash
ANTHROPIC_API_KEY=
```

You can also paste the key in the sidebar for the current session only.

## Screenshot

![AI Travel Itinerary Planner demo](docs/assets/ai-travel-planner-demo.png)

## Limitations

- This is a planning helper, not a booking engine.
- It does not query live hotel, flight, restaurant or availability data.
- Place suggestions depend on the model response or the built-in demo itinerary.
- Budget numbers are estimates and should be checked before travelling.

## Future Improvements

- Add tests for Pydantic validation and prompt parsing.
- Add optional live place data if a suitable API is configured.
- Save generated itineraries locally for comparison.
- Improve PDF layout for longer trips.
- Add more demo examples for different cities.

## What I Learned

This project helped me practise controlling LLM output with schemas. The most important lesson was to validate model responses before they reach the UI, because even a clear prompt can return an unexpected shape.

## 中文简介

AI Travel Itinerary Planner 是一个 Streamlit 旅行计划工具。它可以根据城市、天数、预算和兴趣生成行程，并支持 demo 模式和 PDF 导出。当前版本适合做本地演示和 LLM 工作流练习，不会查询实时机票、酒店或餐厅库存。

作者：Shiyun Ni

## License

MIT. See [LICENSE](LICENSE).
