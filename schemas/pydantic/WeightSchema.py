import datetime
from pydantic import BaseModel


class WeightSchema(BaseModel):
    time: datetime.datetime
    weight: float
