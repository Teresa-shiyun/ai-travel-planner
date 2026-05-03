"""PDF export for an Itinerary using ReportLab.

Returns the PDF as bytes so Streamlit can offer it as a download without
touching the filesystem.
"""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from planner.models import DayPlan, Itinerary, Meal


def itinerary_to_pdf(itinerary: Itinerary) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    h1 = styles["Heading1"]
    h2 = styles["Heading2"]
    h3 = styles["Heading3"]
    body = styles["BodyText"]

    small = ParagraphStyle(
        "small", parent=body, fontSize=9, textColor=colors.grey, spaceAfter=4
    )

    story = []

    story.append(Paragraph(f"{itinerary.city} — {itinerary.days} days", h1))
    mode = " · Student mode" if itinerary.student_mode else ""
    story.append(
        Paragraph(
            f"{itinerary.country} · €{itinerary.budget_eur:.0f} budget{mode}", small
        )
    )
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(itinerary.summary, body))
    story.append(Spacer(1, 0.5 * cm))

    bb = itinerary.budget_breakdown
    budget_table = Table(
        [
            ["Accommodation", f"€{bb.accommodation_eur:.0f}"],
            ["Food", f"€{bb.food_eur:.0f}"],
            ["Transport", f"€{bb.transport_eur:.0f}"],
            ["Attractions", f"€{bb.attractions_eur:.0f}"],
            ["Misc", f"€{bb.misc_eur:.0f}"],
            ["Total", f"€{itinerary.total_estimated_eur:.0f}"],
        ],
        colWidths=[5 * cm, 3 * cm],
    )
    budget_table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
                ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 10),
                ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(Paragraph("Budget breakdown", h2))
    story.append(budget_table)
    story.append(Spacer(1, 0.5 * cm))

    for day in itinerary.days_plan:
        story.append(Paragraph(f"Day {day.day} — {day.title}", h2))
        story.append(
            Paragraph(
                f"Daily total: €{day.daily_total_eur:.2f} · {day.transport_note}", small
            )
        )

        if day.morning:
            story.append(Paragraph("Morning", h3))
            for place in day.morning:
                story.extend(_place_block(place, body, small))

        story.append(Paragraph("Lunch", h3))
        story.extend(_meal_block(day.lunch, body, small))

        if day.afternoon:
            story.append(Paragraph("Afternoon", h3))
            for place in day.afternoon:
                story.extend(_place_block(place, body, small))

        story.append(Paragraph("Dinner", h3))
        story.extend(_meal_block(day.dinner, body, small))

        if day.evening:
            story.append(Paragraph("Evening", h3))
            for place in day.evening:
                story.extend(_place_block(place, body, small))

        story.append(Spacer(1, 0.4 * cm))

    if itinerary.tips:
        story.append(Paragraph("Tips", h2))
        for tip in itinerary.tips:
            story.append(Paragraph(f"• {tip}", body))

    doc.build(story)
    return buffer.getvalue()


def _place_block(place, body, small):
    cost = f"€{place.cost_eur:.0f}" if place.cost_eur > 0 else "Free"
    blocks = [
        Paragraph(
            f"<b>{place.name}</b> — {cost} · {place.duration_minutes} min", body
        ),
        Paragraph(place.description, body),
    ]
    if place.rainy_day_alternative:
        blocks.append(Paragraph(f"Rainy day: {place.rainy_day_alternative}", small))
    blocks.append(Spacer(1, 0.15 * cm))
    return blocks


def _meal_block(meal: Meal, body, small):
    return [
        Paragraph(
            f"<b>{meal.name}</b> ({meal.cuisine}) — €{meal.cost_eur:.0f}", body
        ),
        Paragraph(meal.note, small),
        Spacer(1, 0.15 * cm),
    ]
