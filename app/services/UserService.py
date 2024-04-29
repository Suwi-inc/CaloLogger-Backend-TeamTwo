import datetime
from typing import List

import requests
from fastapi import Depends, HTTPException

from configs.Environment import get_environment_variables
from models.UserModel import User
from repositories.UserRepository import UserRepository
from schemas.pydantic.UserSchema import UserSchema

# Runtime Environment Configuration
env = get_environment_variables()

class UserService :
    def __init__(self, userRepository: UserRepository) -> None:
        self.userRepository = userRepository

    def create_user(self, data: UserSchema) -> User:
        user = self.userRepository.get_by_username(data.username)
        if user is not None:
            raise HTTPException(
                status_code=400, detail="User already exists"
            )

        user = User(
            username=data.username,
            password=data.password,
            factory=data.factory,
        )

        self.userRepository.create(user)
        return user

    def get_user(self, user_id: int) -> User:
        user = self.userRepository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found"
            )
        return user

    def get_all_users(self) -> List[User]:
        return self.userRepository.list()

    def delete_user(self, user_id: int) -> None:
        user = self.userRepository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found"
            )
        self.userRepository.delete(user)

    def update_user(self, user_id: int, data: UserSchema) -> User:
        user = self.userRepository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found"
            )

        user.username = data.username
        user.password = data.password
        user.factory = data.factory

        self.userRepository.update(user)
        return user

    def get_user_by_username(self, username: str) -> User:
        user = self.userRepository.get_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found"
            )
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.userRepository.get_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found"
            )
        return user

    def get_user_by_phone(self, phone: str) -> User:
        user = self.userRepository.get_by_phone(phone)
        if user is None:
            raise HTTPException(
                status_code=404, detail="User not found"
            )
        return user
    