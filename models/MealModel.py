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
    userId = Column(Integer)
    creationTime = Column(DateTime(), nullable=False)
    apiData = Column(String(999), nullable=False)

    PrimaryKeyConstraint(id)
