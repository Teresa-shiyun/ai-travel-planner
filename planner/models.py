from typing import List, Optional
from pydantic import BaseModel, Field


class Place(BaseModel):
    name: str
    category: str = Field(description="museum | landmark | park | viewpoint | shopping | nightlife | other")
    description: str
    duration_minutes: int
    cost_eur: float = Field(ge=0)
    rainy_day_alternative: Optional[str] = None


class Meal(BaseModel):
    name: str
    cuisine: str
    cost_eur: float = Field(ge=0)
    note: str = Field(description="Why this place — e.g. 'student-friendly', 'local favorite', 'vegetarian options'")


class DayPlan(BaseModel):
    day: int
    title: str = Field(description="Short theme for the day, e.g. 'Classic Paris'")
    morning: List[Place]
    lunch: Meal
    afternoon: List[Place]
    dinner: Meal
    evening: Optional[List[Place]] = None
    transport_note: str = Field(description="How to get around today, e.g. 'Day metro pass — €8.45'")
    daily_total_eur: float = Field(ge=0)


class BudgetBreakdown(BaseModel):
    accommodation_eur: float = Field(ge=0)
    food_eur: float = Field(ge=0)
    transport_eur: float = Field(ge=0)
    attractions_eur: float = Field(ge=0)
    misc_eur: float = Field(ge=0)

    @property
    def total(self) -> float:
        return (
            self.accommodation_eur
            + self.food_eur
            + self.transport_eur
            + self.attractions_eur
            + self.misc_eur
        )


class Itinerary(BaseModel):
    city: str
    country: str
    days: int
    budget_eur: float
    interests: List[str]
    student_mode: bool
    summary: str = Field(description="2-3 sentence overview of the trip")
    days_plan: List[DayPlan]
    budget_breakdown: BudgetBreakdown
    total_estimated_eur: float
    tips: List[str] = Field(description="3-5 practical tips: best transport pass, scams to avoid, dress code, etc.")

    def maps_query(self, place_name: str) -> str:
        from urllib.parse import quote_plus

        return f"https://www.google.com/maps/search/?api=1&query={quote_plus(place_name + ' ' + self.city)}"
