import datetime
from typing import List

import requests
from fastapi import Depends, HTTPException

from configs.Environment import get_environment_variables
from models.MealModel import Meal
from repositories.MealRepository import MealRepository
from schemas.pydantic.MealSchema import MealSchema

# Runtime Environment Configuration
env = get_environment_variables()


class MealService:
    mealRepository: MealRepository

    def __init__(
            self, authorRepository: MealRepository = Depends()
    ) -> None:
        self.mealRepository = authorRepository

    def create(self, current_user_id: int, name: str):
        api_data = requests.get(
            url="https://api.calorieninjas.com/v1/nutrition",
            params={'query': name},
            headers={"X-Api-Key": env.CALORIE_NINJAS_API_KEY}
        ).json()['items']

        creation_time = datetime.datetime.now()
        meals = [Meal(apiData=str(meal_response), creationTime=creation_time,
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
