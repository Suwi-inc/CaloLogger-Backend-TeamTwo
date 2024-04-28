from typing import List, Optional

from fastapi import APIRouter, Depends, status

from schemas.pydantic.MealSchema import (
    MealSchema,
)
from services.MealService import MealService

MealRouter = APIRouter(
    prefix="/v1/meal", tags=["meal"]
)

# TODO
def get_current_user_id():
    return 1

@MealRouter.get("/", response_model=List[MealSchema])
def gelAll(
        current_user_id: int = Depends(get_current_user_id),
        mealService: MealService = Depends()):
    return []


@MealRouter.delete("/{id}", response_model=str)
def delete(
        meal_id: int,
        current_user_id: int = Depends(get_current_user_id),
        mealService: MealService = Depends()):
    return mealService.delete(current_user_id, meal_id)


@MealRouter.post(
    "/",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
)
def create(
        name: str,
        current_user_id: int = Depends(get_current_user_id),
        mealService: MealService = Depends(),
):
    mealService.create(current_user_id, name)
    return "ok"


