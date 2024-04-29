import datetime
from typing import List

from fastapi import Depends, HTTPException

from app.clients.CaloriteNinjasClient import CalorieNinjasClient
from app.models.MealModel import Meal
from app.repositories.MealRepository import MealRepository
from app.schemas.pydantic.MealSchema import MealSchema


class MealService:
    mealRepository: MealRepository
    calorieNinjasClient: CalorieNinjasClient

    def __init__(
            self,
            meal_repository: MealRepository = Depends(),
            calorie_ninjas_client: CalorieNinjasClient = Depends(CalorieNinjasClient)
    ) -> None:
        self.mealRepository = meal_repository
        self.calorieNinjasClient = calorie_ninjas_client

    def create(self, current_user_id: int, name: str):
        api_data = self.calorieNinjasClient.get_meal_descriptions(name)

        creation_time = datetime.datetime.utcnow()
        meals = [Meal(apiData=meal_response, creationTime=creation_time,
                      userId=current_user_id) for meal_response in api_data]
        print(meals)
        return self.mealRepository.create(meals)

    def delete(self, meal_id: int, user_id: int):
        meal_by_id = self.mealRepository.get(meal_id)
        if meal_by_id is None:
            raise HTTPException(status_code=404, detail="Meal not found")
        if meal_by_id.userId != user_id:
            raise HTTPException(status_code=403, detail="No access to this "
                                                        "meal")
        self.mealRepository.delete(
            meal_by_id
        )

    def list_by_user_id(
            self,
            user_id: int
    ) -> List[MealSchema]:
        return list([MealSchema(meal_id=meal_model.id,
                                calorie_ninjas_response=meal_model.apiData,
                                time=meal_model.creationTime) for meal_model
                     in self.mealRepository.list_by_user_id(
                user_id
            )])
