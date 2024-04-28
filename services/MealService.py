import datetime
from typing import List, Optional

from fastapi import Depends
from models.MealModel import Meal

from repositories.MealRepository import MealRepository
from schemas.pydantic.MealSchema import MealSchema


class MealService:
    # TODO
    mealRepository: MealRepository

    def __init__(
        self, authorRepository: MealRepository = Depends()
    ) -> None:
        self.mealRepository = authorRepository

    def create(self, current_user_id: int, name: str):
        return self.mealRepository.create(
            Meal(
                creationTime=datetime.datetime.now(),
                apiData=f"TODO, user - {current_user_id}"
            )
        )

    def delete(self, author_id: int) -> None:
        return self.mealRepository.delete(
            Meal(id=author_id)
        )

    def get(self, author_id: int) -> Meal:
        return self.mealRepository.get(
            Meal(id=author_id)
        )

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Meal]:
        return self.mealRepository.list(
            name, pageSize, startIndex
        )

    def update(
        self, author_id: int, author_body: MealSchema
    ) -> Meal:
        return self.mealRepository.update(
            author_id, Meal(name=author_body.name)
        )

    def get_books(self, author_id: int) -> List[Meal]:
        return self.mealRepository.get(
            Meal(id=author_id)
        ).books
