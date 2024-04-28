from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    DateTime
)
from sqlalchemy.orm import relationship

from models.BaseModel import EntityMeta


class Meal(EntityMeta):
    __tablename__ = "meals"

    id = Column(Integer)
    user_id = Column(Integer)
    creationTime = Column(DateTime(), nullable=False)
    apiData = Column(String(999), nullable=False)

    PrimaryKeyConstraint(id)

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
        }
