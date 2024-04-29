from fastapi import FastAPI

from app.configs.Environment import get_environment_variables
from app.metadata.Tags import Tags
from app.models.BaseModel import init
from app.routers.v1.WeightRouter import WeightRouter
from app.routers.v1.MealRouter import MealRouter
from fastapi.middleware.cors import CORSMiddleware

# Application Environment Configuration
env = get_environment_variables()

# Core Application Instance
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

origins = ["*"]

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Routers
app.include_router(MealRouter)
app.include_router(WeightRouter)
#app.include_router(UserRouter)

# Initialise Data Model Attributes
init()
