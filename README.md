# AI Travel Itinerary Planner / AI 旅行行程规划器

## Overview / 项目简介

AI Travel Itinerary Planner is a Streamlit app that creates multi-day travel plans from a few inputs: city, trip length, budget, interests and language. It includes a built-in Paris demo itinerary, so the UI can be tested without an API key.

AI Travel Itinerary Planner 是一个 Streamlit 旅行计划工具。用户输入城市、天数、预算、兴趣和语言后，应用可以生成多日行程。项目内置巴黎 demo 行程，所以没有 API key 也可以测试主要界面。

## Why I Built It / 项目背景

I built this to practise LLM application structure in Python: prompt design, schema validation, UI rendering and PDF export. The original use case was planning budget-friendly short trips for students in Europe.

我做这个项目是为了用 Python 练习 LLM 应用结构，包括 prompt 设计、结构化输出校验、页面渲染和 PDF 导出。最初场景是为欧洲学生规划预算友好的短途旅行。

## Features / 功能

- Collect city, trip length, budget, interests and student-mode inputs.
- Run in demo mode without external credentials.
- Call the Anthropic API for live itinerary generation when configured.
- Validate generated itinerary data with Pydantic models.
- Show day-by-day plans, meals, travel notes and rainy-day alternatives.
- Add Google Maps links for places.
- Export the generated itinerary as a PDF.

- 输入城市、旅行天数、预算、兴趣和学生模式。
- 无需外部密钥即可使用 demo 模式。
- 配置 Anthropic API 后可以生成实时行程。
- 使用 Pydantic 校验生成的结构化行程数据。
- 展示每日安排、餐食建议、交通提示和雨天备选。
- 为地点添加 Google Maps 链接。
- 支持将生成行程导出为 PDF。

## Tech Stack / 技术栈

- Python
- Streamlit
- Anthropic SDK
- Pydantic v2
- ReportLab
- python-dotenv

## Current Status / 当前状态

Working Streamlit prototype. Demo mode is ready for local testing. Live generation requires an Anthropic API key and should still be reviewed before travel planning.

当前是可运行的 Streamlit 原型。demo 模式可以直接本地测试；实时生成需要 Anthropic API key，生成内容在真实出行前仍然需要人工核对。

## How to Run / 本地运行

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

运行后打开终端里显示的 Streamlit 本地地址。默认可以使用 demo 模式；如果要生成新行程，可以配置 `.env` 或在侧边栏临时输入 API key。

## Screenshots / 项目截图

![AI Travel Itinerary Planner demo](docs/assets/ai-travel-planner-demo.png)

## Limitations / 当前限制

- This is a planning helper, not a booking engine.
- It does not query live hotel, flight, restaurant or availability data.
- Place suggestions depend on the model response or the built-in demo itinerary.
- Budget numbers are estimates and should be checked before travelling.

- 这是行程规划辅助工具，不是预订系统。
- 不查询实时酒店、航班、餐厅或余票信息。
- 地点建议来自模型输出或内置 demo 行程。
- 预算数字是估算值，出行前需要自行核对。

## Roadmap / 后续计划

- Add tests for Pydantic validation and prompt parsing.
- Add optional live place data if a suitable API is configured.
- Save generated itineraries locally for comparison.
- Improve PDF layout for longer trips.
- Add more demo examples for different cities.

- 为 Pydantic 校验和 prompt 解析补充测试。
- 如果找到合适 API，再考虑接入实时地点数据。
- 支持本地保存多个生成行程用于对比。
- 改进长行程 PDF 排版。
- 增加不同城市的 demo 示例。

## What I Learned / 我的收获

This project helped me practise controlling LLM output with schemas. The most important lesson was to validate model responses before they reach the UI, because even a clear prompt can return an unexpected shape.

这个项目让我练习了如何用数据模型约束 LLM 输出。最大的收获是：即使 prompt 写得比较清楚，也需要在进入 UI 前做结构校验，否则页面很容易被不稳定输出影响。

## License / 许可证

MIT. See [LICENSE](LICENSE).
