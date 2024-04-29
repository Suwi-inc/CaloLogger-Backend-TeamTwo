from typing import List

from fastapi import APIRouter, Depends, status

from schemas.pydantic.MealSchema import (
    MealSchema,
)
from services.MealService import MealService

from AuthRouter import get_current_user_id

MealRouter = APIRouter(
    prefix="/v1/meal", tags=["meal"]
)


@MealRouter.get(
    "/",
    response_model=List[MealSchema],
    status_code=status.HTTP_200_OK)
def gel_all(
        current_user_id: int = Depends(get_current_user_id),
        mealService: MealService = Depends()):
    return mealService.list_by_user_id(current_user_id)


@MealRouter.delete(
    "/",
    response_model=str,
    status_code=status.HTTP_200_OK,
    responses={
        403: {
            "description": "No access to this meal",
            "content": {
                "application/json": {
                    "example": {"detail": "No access to this meal"}
                }
            }
        },
        404: {
            "description": "Meal not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Meal not found"}
                }
            }
        }})
def delete(
        meal_id: int,
        current_user_id: int = Depends(get_current_user_id),
        mealService: MealService = Depends()):
    mealService.delete(meal_id, current_user_id)
    return 'ok'


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
