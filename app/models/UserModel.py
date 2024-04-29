from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    DateTime
)

from app.models.BaseModel import EntityMeta


class User(EntityMeta):
    __tablename__ = "user"
    userId = Column(Integer)
    username = Column(String)
    password = Column(String)

    # noinspection PyTypeChecker
    PrimaryKeyConstraint(userId)