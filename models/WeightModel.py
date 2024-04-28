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
    userId = Column(Integer)
    creationTime = Column(DateTime(), nullable=False)
    kg = Column(Float)

    PrimaryKeyConstraint(id)
