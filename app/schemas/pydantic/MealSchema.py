import datetime

from pydantic import BaseModel


class MealSchema(BaseModel):
    time: datetime.datetime
    meal_id: int
    calorie_ninjas_response: str
