from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.pydantic.WeightSchema import (
    WeightSchema,
)
from app.services.WeightService import WeightService

from app.routers.v1.AuthRouter import get_current_user_id

WeightRouter = APIRouter(
    prefix="/v1/weight", tags=["weight"]
)

@WeightRouter.get(
    "/",
    response_model=List[WeightSchema],
    status_code=status.HTTP_200_OK)
def gel_all(
        current_user_id: int = Depends(get_current_user_id),
        weightService: WeightService = Depends()):
    return weightService.get_all_weights(current_user_id)


@WeightRouter.post(
    "/",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
)
def create(
        weight: float,
        current_user_id: int = Depends(get_current_user_id),
        weightService: WeightService = Depends()):
    weightService.add_weight(current_user_id, weight)
    return "ok"
