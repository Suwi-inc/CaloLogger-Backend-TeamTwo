from pydantic import BaseModel


class UserSchema(BaseModel):  # also can be used for creation
    username: str
    password: str


class UserInfo(BaseModel):
    userId: int
    username: str


class UserUpdate(UserSchema):
    userId: int


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
    exp: int
