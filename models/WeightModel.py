from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    DateTime, Float
)

from models.BaseModel import EntityMeta


class Weight(EntityMeta):
    __tablename__ = "weights"

    id = Column(Integer)
    kg = Column(Float)
    userId = Column(Integer)
    creationTime = Column(DateTime(), nullable=False)

    PrimaryKeyConstraint(id)
