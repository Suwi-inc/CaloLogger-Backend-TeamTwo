from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session, lazyload

from configs.Database import (
    get_db_connection,
)
from models.MealModel import Meal


class MealRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def list(
        self,
        name: Optional[str],
        limit: Optional[int],
        start: Optional[int],
    ) -> List[Meal]:
        query = self.db.query(Meal)

        if name:
            query = query.filter_by(name=name)

        return query.offset(start).limit(limit).all()

    def get(self, author: Meal) -> Meal:
        return self.db.get(
            Meal,
            author.id,
            options=[lazyload(Meal.books)],
        )

    def create(self, meal: Meal) -> Meal:
        self.db.add(meal)
        self.db.commit()
        self.db.refresh(meal)
        return meal

    def update(self, id: int, author: Meal) -> Meal:
        author.id = id
        self.db.merge(author)
        self.db.commit()
        return author

    def delete(self, author: Meal) -> None:
        self.db.delete(author)
        self.db.commit()
        self.db.flush()
