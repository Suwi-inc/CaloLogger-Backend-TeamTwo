from datetime import datetime
from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import get_db_connection
from models.WeightModel import Weight


class WeightRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def get_all_weights(self, user_id: int) -> list[Type[Weight]]:
        return self.db.query(Weight).filter_by(userId=user_id).all()

    def add_weight(self, user_id: int, kg: float) -> Weight:
        weight = Weight(
            userId=user_id,
            creationTime=datetime.now(),
            kg=kg
        )
        self.db.add(weight)
        self.db.commit()
        self.db.refresh(weight)
        return weight
