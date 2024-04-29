import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from app.configs.Database import get_db_connection
from app.configs.Environment import get_environment_variables
from app.models.UserModel import User
from app.routers.v1.auth import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)
from app.schemas.pydantic.UserSchema import (
    UserSchema,
    UserInfo,
    TokenPayload,
    TokenSchema,
)

env = get_environment_variables()

router = APIRouter(
    prefix="/v1/auth", tags=["auth"]
)

# engine = get_engine()
# session = Session(engine)

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/v1/auth/login",
                                       scheme_name="JWT")


@router.post("/signup", summary="Create a new user",
             response_model=UserSchema)
async def create_user(data: UserSchema, session=Depends(get_db_connection)):
    user = session.query(User).filter(User.username == data.username).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    user = User(
        username=data.username,
        password=get_hashed_password(data.password),
    )

    session.add(user)
    session.commit()

    new_user = session.query(User).filter(
        User.username == data.username).first()
    return UserSchema(
        username=new_user.username,
        password=new_user.password
    )


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(data: OAuth2PasswordRequestForm = Depends(),
                session=Depends(get_db_connection)):
    logging.info(f"Data received: {data}")
    user = session.query(User).filter(User.username == data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect credentials"
        )

    hashed_pass = user.password
    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect credentials"
        )

    return {
        "access_token": create_access_token(user.username,
                                            env.JWT_SECRET_KEY),
        "refresh_token": create_refresh_token(user.username,
                                              env.JWT_REFRESH_SECRET_KEY),
        "user_id": user.userId,
    }


async def get_current_user(
        token: str = Depends(reuseable_oauth),
        session=Depends(get_db_connection)
) -> UserInfo:
    try:
        print(token)
        print(env.JWT_SECRET_KEY)
        payload = jwt.decode(token, env.JWT_SECRET_KEY,
                             algorithms=[env.ALGORITHM])
        print(payload)
        token_data = TokenPayload(**payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.JWTError as er:
        print(er)
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
        userId=user.userId,
        username=user.username
    )


def get_current_user_id(user: UserInfo = Depends(get_current_user)):
    return user.userId


@router.get(
    "/me", summary="Get details of currently logged in user",
    response_model=UserInfo
)
async def get_me(user: UserInfo = Depends(get_current_user)):
    return user
