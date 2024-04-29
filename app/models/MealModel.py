from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    DateTime
)

from app.models.BaseModel import EntityMeta


class Meal(EntityMeta):
    __tablename__ = "meals"

    id = Column(Integer)
    userId = Column(Integer)
    creationTime = Column(DateTime(), nullable=False)
    apiData = Column(String(999), nullable=False)

    # noinspection PyTypeChecker
    PrimaryKeyConstraint(id)
