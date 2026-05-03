"""Hard-coded demo itinerary so the app runs without an Anthropic API key.

Used by Streamlit's "Demo mode" toggle — recruiters/visitors can try the full
UI (PDF export, maps links, budget breakdown) before investing in a key.
"""

from planner.models import BudgetBreakdown, DayPlan, Itinerary, Meal, Place


def demo_itinerary() -> Itinerary:
    return Itinerary(
        city="Paris",
        country="France",
        days=2,
        budget_eur=250.0,
        interests=["art", "history", "cafes"],
        student_mode=True,
        summary=(
            "Two days of classic Paris on a student budget — Louvre + Latin Quarter on "
            "day one, Montmartre + Seine on day two. Walking-heavy, with a single day "
            "metro pass on day two. No tourist traps."
        ),
        days_plan=[
            DayPlan(
                day=1,
                title="Classic Paris: Louvre & Latin Quarter",
                morning=[
                    Place(
                        name="Louvre Museum",
                        category="museum",
                        description="World's largest art museum. Free for under-26 EU residents; €22 otherwise. Skip the Mona Lisa queue and head to the Italian Renaissance wing.",
                        duration_minutes=180,
                        cost_eur=22.0,
                        rainy_day_alternative="Stay inside — the Louvre is already indoor.",
                    ),
                ],
                lunch=Meal(
                    name="L'As du Fallafel",
                    cuisine="Middle Eastern",
                    cost_eur=10.0,
                    note="Iconic falafel in the Marais. Order to-go and eat in Place des Vosges.",
                ),
                afternoon=[
                    Place(
                        name="Notre-Dame Cathedral exterior + Île de la Cité",
                        category="landmark",
                        description="Cathedral is closed for restoration but worth seeing from outside. Walk across to Île Saint-Louis for ice cream.",
                        duration_minutes=60,
                        cost_eur=0.0,
                        rainy_day_alternative="Sainte-Chapelle (€11.50, stunning stained glass, indoor).",
                    ),
                    Place(
                        name="Shakespeare and Company bookstore",
                        category="other",
                        description="Legendary English-language bookstore opposite Notre-Dame. Free to browse.",
                        duration_minutes=45,
                        cost_eur=0.0,
                        rainy_day_alternative=None,
                    ),
                    Place(
                        name="Latin Quarter walk",
                        category="other",
                        description="Wander Rue Mouffetard and Place de la Contrescarpe. Stop for an espresso (€2-3).",
                        duration_minutes=90,
                        cost_eur=3.0,
                        rainy_day_alternative="Panthéon (€11.50, free under 26 EU).",
                    ),
                ],
                dinner=Meal(
                    name="Le Petit Vendôme",
                    cuisine="French bistro",
                    cost_eur=18.0,
                    note="Plat du jour around €15-18. Order the jambon-beurre or steak frites.",
                ),
                evening=None,
                transport_note="Walk everything today — central Paris is compact. No transit needed.",
                daily_total_eur=53.0,
            ),
            DayPlan(
                day=2,
                title="Montmartre & the Seine",
                morning=[
                    Place(
                        name="Sacré-Cœur Basilica + Montmartre",
                        category="viewpoint",
                        description="Free entry to the basilica; €8 for the dome (worth it, panoramic view). Wander Place du Tertre after.",
                        duration_minutes=120,
                        cost_eur=8.0,
                        rainy_day_alternative="Musée de Montmartre (€15) — Renoir's old studio.",
                    ),
                ],
                lunch=Meal(
                    name="Le Relais Gascon",
                    cuisine="French (Gascon)",
                    cost_eur=15.0,
                    note="Famous for giant warm goat-cheese salads (~€14). 5 min walk from Sacré-Cœur.",
                ),
                afternoon=[
                    Place(
                        name="Musée d'Orsay",
                        category="museum",
                        description="Impressionist masterpieces in a converted railway station. Free under 26 EU; €16 otherwise.",
                        duration_minutes=150,
                        cost_eur=16.0,
                        rainy_day_alternative="Stay inside — fully indoor.",
                    ),
                    Place(
                        name="Seine walk: Pont des Arts → Pont Alexandre III",
                        category="other",
                        description="Sunset walk along the river. Grab a baguette + cheese (~€6) for a picnic.",
                        duration_minutes=90,
                        cost_eur=6.0,
                        rainy_day_alternative="Galeries Lafayette rooftop (free, covered).",
                    ),
                ],
                dinner=Meal(
                    name="Bouillon Pigalle",
                    cuisine="French (traditional)",
                    cost_eur=20.0,
                    note="Classic French at near-cafeteria prices. Mains €8-12. No reservations — go before 7pm.",
                ),
                evening=[
                    Place(
                        name="Eiffel Tower at night (from Trocadéro)",
                        category="landmark",
                        description="Best free view of the tower lit up. Hourly sparkle on the hour after sunset.",
                        duration_minutes=45,
                        cost_eur=0.0,
                        rainy_day_alternative="Skip — tower is less impressive in heavy rain.",
                    ),
                ],
                transport_note="Day metro pass: €8.45 (Navigo Easy). Covers all metro + buses.",
                daily_total_eur=73.45,
            ),
        ],
        budget_breakdown=BudgetBreakdown(
            accommodation_eur=120.0,
            food_eur=63.0,
            transport_eur=17.0,
            attractions_eur=46.0,
            misc_eur=4.0,
        ),
        total_estimated_eur=250.0,
        tips=[
            "Under 26 and EU resident? Most national museums (Louvre, d'Orsay, Pompidou, Panthéon) are free. Bring ID.",
            "Buy a Navigo Easy card (€2 one-time) and load day passes (€8.45) — way cheaper than single tickets (€2.15 each).",
            "Skip the Bateaux Mouches river cruise (€16) — the free Seine walk gives you the same view.",
            "Tap water is fine and free at all restaurants — ask for 'une carafe d'eau'. Bottled water is €5+.",
            "Bouillon restaurants (Pigalle, Chartier, République) serve full traditional French meals for under €20. Best cheap eats in the city.",
        ],
    )
