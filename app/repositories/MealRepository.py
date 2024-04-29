from typing import List, Iterable

from fastapi import Depends
from sqlalchemy.orm import Session, Query

from app.configs.Database import (
    get_db_connection,
)
from app.models.MealModel import Meal


class MealRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def list_by_user_id(
        self,
        user_id: int
    ) -> List[Meal]:
        # noinspection PyTypeChecker
        query: Query[Meal] = self.db.query(Meal)

        query = query.filter_by(userId=user_id)

        return query.all()

    def get(self, meal_id: int) -> Meal | None:
        return self.db.get(
            Meal,
            meal_id
        )

    def create(self, meal: Iterable[Meal]):
        self.db.add_all(meal)
        self.db.commit()
        # self.db.refresh(meal)

    def delete(self, author: Meal) -> None:
        self.db.delete(author)
        self.db.commit()
        self.db.flush()
