from typing import List, Optional, Iterable, Type

from fastapi import Depends
from sqlalchemy.orm import Session, lazyload, Query

from configs.Database import (
    get_db_connection,
)
from models.UserModel import User


class UserRepository:
    db: Session

    def __init__(
        self, db: Session = Depends(get_db_connection)
    ) -> None:
        self.db = db

    def list_by_user_id(
        self,
        user_id: int
    ) -> List[User]:
        query: Query[User] = self.db.query(User)

        query = query.filter_by(userId=user_id)

        return query.all()

    def get(self, user_id: int) -> User | None:
        return self.db.get(
            User,
            user_id
        )

    def create(self, user: Iterable[User]):
        self.db.add_all(user)
        self.db.commit()
        # self.db.refresh(user)

    def delete(self, author: User) -> None:
        self.db.delete(author)
        self.db.commit()
        self.db.flush()