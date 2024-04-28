from typing import List

from fastapi import Depends

from repositories.WeightRepository import WeightRepository
from schemas.pydantic.WeightSchema import WeightSchema


class WeightService:
    weight_repository: WeightRepository

    def __init__(
            self, weight_repository: WeightRepository = Depends()
    ) -> None:
        self.weight_repository = weight_repository

    def add_weight(self, user_id: int, kg: float) -> WeightSchema:
        weight = self.weight_repository.add_weight(user_id, kg)
        return WeightSchema(
            weight_id=weight.id,
            weight_kg=weight.kg,
            time=weight.creationTime
        )

    def get_all_weights(self, user_id: int) -> List[WeightSchema]:
        weights = self.weight_repository.get_all_weights(user_id)
        return [
            WeightSchema(
                weight_id=weight.id,
                weight_kg=weight.kg,
                time=weight.creationTime
            )
            for weight in weights
        ]
