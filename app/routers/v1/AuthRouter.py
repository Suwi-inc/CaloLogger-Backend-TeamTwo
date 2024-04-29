import logging
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from auth import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)
from db import get_db
from models import User

from schemas.pydantic.UserSchema import (
    UserSchema,
    UserInfo,
    TokenPayload, 
    TokenSchema,
)

load_dotenv(".env")

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter()

# engine = get_engine()
# session = Session(engine)

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login", scheme_name="JWT")

@router.post("/signup", summary="Create a new user", response_model=UserSchema)
async def create_user(data: UserSchema, session=Depends(get_db)):
    user = session.query(User).filter(User.username == data.username).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    user = User(
        username=data.username,
        password=get_hashed_password(data.password),
        first_name=data.first_name,
        second_name=data.second_name,
        factory=data.factory,
    )

    session.add(user)
    session.commit()

    new_user = session.query(User).filter(User.username == data.username).first()
    return {
        "username": new_user.username,
        "password": new_user.password,
        "first_name": new_user.first_name,
        "second_name": new_user.second_name,
        "factory": new_user.factory,
    }


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_db)):
    logging.info(f"Data received: {data}")
    user = session.query(User).filter(User.username == data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credentials"
        )

    hashed_pass = user.password
    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credentials"
        )

    return {
        "access_token": create_access_token(user.username, JWT_SECRET_KEY),
        "refresh_token": create_refresh_token(user.username, JWT_REFRESH_SECRET_KEY),
        "user_id": user.id,
    }


async def get_current_user(
    token: str = Depends(reuseable_oauth), session=Depends(get_db)
) -> UserInfo:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.query(User).filter(User.username == token_data.sub).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserInfo(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        second_name=user.second_name,
        factory=user.factory,
    )


def get_current_user_id(user: user = Depends(get_current_user)):
    return user.id

@router.get(
    "/me", summary="Get details of currently logged in user", response_model=UserInfo
)
async def get_me(user: UserInfo = Depends(get_current_user)):
    return user