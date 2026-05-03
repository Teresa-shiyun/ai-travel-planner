"""Streamlit UI for the AI Travel Itinerary Planner."""

import os

import streamlit as st
from dotenv import load_dotenv

from planner import demo_itinerary, generate_itinerary
from planner.i18n import STRINGS, t
from planner.llm import GenerationError
from planner.models import DayPlan, Itinerary, Meal, Place
from planner.pdf_export import itinerary_to_pdf

load_dotenv()

st.set_page_config(
    page_title="AI Travel Itinerary Planner",
    page_icon=":earth_africa:",
    layout="wide",
)


def render_meal(meal: Meal, label: str, lang: str) -> None:
    st.markdown(
        f"**{label}: {meal.name}** &nbsp; · &nbsp; *{meal.cuisine}* &nbsp; · &nbsp; €{meal.cost_eur:.0f}"
    )
    st.caption(meal.note)


def render_place(place: Place, itinerary: Itinerary, lang: str) -> None:
    cost = f"€{place.cost_eur:.0f}" if place.cost_eur > 0 else "Free"
    maps_url = itinerary.maps_query(place.name)
    cols = st.columns([5, 1])
    with cols[0]:
        st.markdown(
            f"**{place.name}** &nbsp; · &nbsp; {cost} &nbsp; · &nbsp; {place.duration_minutes} min &nbsp; · &nbsp; *{place.category}*"
        )
        st.write(place.description)
        if place.rainy_day_alternative:
            st.caption(f":umbrella: {t(lang, 'rainy_day')}: {place.rainy_day_alternative}")
    with cols[1]:
        st.link_button(t(lang, "open_in_maps"), maps_url, use_container_width=True)


def render_day(day: DayPlan, itinerary: Itinerary, lang: str) -> None:
    st.subheader(f"{t(lang, 'day_label').format(n=day.day)} — {day.title}")
    st.caption(
        f"{t(lang, 'transport_today')}: {day.transport_note} &nbsp; · &nbsp; {t(lang, 'daily_total')}: €{day.daily_total_eur:.2f}"
    )

    if day.morning:
        st.markdown(f"### :sunrise: {t(lang, 'morning')}")
        for place in day.morning:
            render_place(place, itinerary, lang)

    st.markdown(f"### :fork_and_knife: {t(lang, 'lunch')}")
    render_meal(day.lunch, t(lang, "lunch"), lang)

    if day.afternoon:
        st.markdown(f"### :sun_with_face: {t(lang, 'afternoon')}")
        for place in day.afternoon:
            render_place(place, itinerary, lang)

    st.markdown(f"### :wine_glass: {t(lang, 'dinner')}")
    render_meal(day.dinner, t(lang, "dinner"), lang)

    if day.evening:
        st.markdown(f"### :night_with_stars: {t(lang, 'evening')}")
        for place in day.evening:
            render_place(place, itinerary, lang)


def render_budget(itinerary: Itinerary, lang: str) -> None:
    bb = itinerary.budget_breakdown
    cols = st.columns(5)
    cols[0].metric(t(lang, "accommodation"), f"€{bb.accommodation_eur:.0f}")
    cols[1].metric(t(lang, "food"), f"€{bb.food_eur:.0f}")
    cols[2].metric(t(lang, "transport"), f"€{bb.transport_eur:.0f}")
    cols[3].metric(t(lang, "attractions"), f"€{bb.attractions_eur:.0f}")
    cols[4].metric(t(lang, "misc"), f"€{bb.misc_eur:.0f}")

    delta = itinerary.total_estimated_eur - itinerary.budget_eur
    delta_color = "inverse" if delta > 0 else "normal"
    st.metric(
        f"{t(lang, 'estimated')} {t(lang, 'total').lower()}",
        f"€{itinerary.total_estimated_eur:.0f}",
        delta=f"€{delta:+.0f} {t(lang, 'vs_budget').format(budget=itinerary.budget_eur)}",
        delta_color=delta_color,
    )


def render_itinerary(itinerary: Itinerary, lang: str) -> None:
    st.header(f"{itinerary.city}, {itinerary.country} — {itinerary.days} days")
    st.write(itinerary.summary)

    st.markdown("---")
    st.subheader(t(lang, "budget_breakdown"))
    render_budget(itinerary, lang)

    st.markdown("---")
    tabs = st.tabs([t(lang, "day_label").format(n=d.day) for d in itinerary.days_plan])
    for tab, day in zip(tabs, itinerary.days_plan):
        with tab:
            render_day(day, itinerary, lang)

    if itinerary.tips:
        st.markdown("---")
        st.subheader(f":bulb: {t(lang, 'tips')}")
        for tip in itinerary.tips:
            st.markdown(f"- {tip}")

    st.markdown("---")
    pdf_bytes = itinerary_to_pdf(itinerary)
    st.download_button(
        label=f":page_facing_up: {t(lang, 'download_pdf')}",
        data=pdf_bytes,
        file_name=f"{itinerary.city.lower().replace(' ', '_')}_{itinerary.days}d.pdf",
        mime="application/pdf",
    )


def sidebar() -> dict:
    with st.sidebar:
        ui_lang = st.selectbox(
            "UI language / 界面语言", options=["en", "zh"], format_func=lambda x: {"en": "English", "zh": "中文"}[x]
        )
        st.header(t(ui_lang, "sidebar_settings"))

        demo = st.toggle(t(ui_lang, "demo_mode"), value=True, help=t(ui_lang, "demo_mode_help"))

        env_key = os.getenv("ANTHROPIC_API_KEY", "")
        api_key = st.text_input(
            t(ui_lang, "api_key"),
            value=env_key,
            type="password",
            help=t(ui_lang, "api_key_help"),
            disabled=demo,
        )

        model = st.selectbox(
            t(ui_lang, "model"),
            options=["claude-opus-4-7", "claude-sonnet-4-6", "claude-haiku-4-5"],
            index=1,
            disabled=demo,
            help="Sonnet 4.6 is the best balance of cost & quality for itinerary generation.",
        )

        return {
            "ui_lang": ui_lang,
            "demo": demo,
            "api_key": api_key,
            "model": model,
        }


def trip_form(ui_lang: str) -> dict | None:
    st.subheader(t(ui_lang, "trip_inputs"))
    with st.form("trip"):
        cols = st.columns([3, 1, 1])
        city = cols[0].text_input(
            t(ui_lang, "city"), placeholder=t(ui_lang, "city_placeholder")
        )
        days = cols[1].number_input(t(ui_lang, "days"), min_value=1, max_value=14, value=3)
        budget = cols[2].number_input(
            t(ui_lang, "budget"), min_value=50, max_value=10000, value=500, step=50
        )

        interests = st.multiselect(
            t(ui_lang, "interests"),
            options=STRINGS[ui_lang]["interests_options"],
            default=STRINGS[ui_lang]["interests_options"][:3],
        )

        cols2 = st.columns(2)
        student = cols2[0].toggle(t(ui_lang, "student_mode"), value=False)
        itin_lang = cols2[1].selectbox(
            t(ui_lang, "itinerary_language"),
            options=["en", "zh"],
            format_func=lambda x: {"en": "English", "zh": "中文"}[x],
        )

        submitted = st.form_submit_button(t(ui_lang, "generate"), type="primary")

        if submitted:
            if not city.strip():
                st.error(t(ui_lang, "city"))
                return None
            return {
                "city": city.strip(),
                "days": int(days),
                "budget": float(budget),
                "interests": interests,
                "student": student,
                "itin_lang": itin_lang,
            }
    return None


def main() -> None:
    settings = sidebar()
    ui_lang = settings["ui_lang"]

    st.title(f":earth_africa: {t(ui_lang, 'page_title')}")
    st.caption(t(ui_lang, "tagline"))

    if settings["demo"]:
        st.info(t(ui_lang, "demo_disclaimer"))
        if "itinerary" not in st.session_state or st.session_state.get("source") != "demo":
            st.session_state["itinerary"] = demo_itinerary()
            st.session_state["source"] = "demo"
        render_itinerary(st.session_state["itinerary"], ui_lang)
        return

    inputs = trip_form(ui_lang)

    if inputs:
        if not settings["api_key"]:
            st.error(t(ui_lang, "no_api_key"))
            return

        with st.spinner(t(ui_lang, "generating")):
            try:
                itinerary = generate_itinerary(
                    city=inputs["city"],
                    days=inputs["days"],
                    budget_eur=inputs["budget"],
                    interests=inputs["interests"],
                    student_mode=inputs["student"],
                    language=inputs["itin_lang"],
                    api_key=settings["api_key"],
                    model=settings["model"],
                )
                st.session_state["itinerary"] = itinerary
                st.session_state["source"] = "live"
            except GenerationError as exc:
                st.error(str(exc))
                return

    if "itinerary" in st.session_state and st.session_state.get("source") == "live":
        render_itinerary(st.session_state["itinerary"], ui_lang)


if __name__ == "__main__":
    main()
