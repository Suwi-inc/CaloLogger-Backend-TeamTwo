from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.pydantic.MealSchema import (
    MealSchema,
)
from app.services.MealService import MealService

from app.routers.v1.AuthRouter import get_current_user_id

MealRouter = APIRouter(
    prefix="/v1/meal", tags=["meal"]
)


@MealRouter.get(
    "/",
    response_model=List[MealSchema],
    status_code=status.HTTP_200_OK)
def gel_all(
        current_user_id: int = Depends(get_current_user_id),
        meal_service: MealService = Depends()):
    return meal_service.list_by_user_id(current_user_id)


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
        meal_service: MealService = Depends()):
    meal_service.delete(meal_id, current_user_id)
    return 'ok'


@MealRouter.post(
    "/",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
)
def create(
        name: str,
        current_user_id: int = Depends(get_current_user_id),
        meal_service: MealService = Depends(),
):
    meal_service.create(current_user_id, name)
    return "ok"
