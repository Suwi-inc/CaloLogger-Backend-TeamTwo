import datetime
from pydantic import BaseModel


class WeightSchema(BaseModel):
    time: datetime.datetime
    weight_id: int
    weight_kg: float
