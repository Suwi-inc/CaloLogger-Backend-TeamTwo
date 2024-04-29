import datetime
from unittest import TestCase
from unittest.mock import create_autospec, MagicMock

import pytest
from fastapi import HTTPException

from __tests__.common.DatetimeHelpers import is_time_between
from app.clients.CaloriteNinjasClient import CalorieNinjasClient
from app.repositories.MealRepository import MealRepository
from app.services.MealService import MealService
from app.models.MealModel import Meal
from app.schemas.pydantic.MealSchema import MealSchema


class TestMealService(TestCase):
    meal_repository: MealRepository
    calorie_ninjas_client: CalorieNinjasClient
    meal_service: MealService

    def setUp(self):
        super().setUp()
        self.meal_repository = create_autospec(
            MealRepository
        )
        self.calorie_ninjas_client = create_autospec(
            CalorieNinjasClient
        )
        self.meal_service = MealService(
            self.meal_repository,
            self.calorie_ninjas_client
        )

    def test_create(self):
        self.calorie_ninjas_client.get_meal_descriptions = MagicMock()
        self.meal_repository.create = MagicMock()
        self.calorie_ninjas_client.get_meal_descriptions.return_value = ["{some json 1}", "{some json2}"]
        start_time = datetime.datetime.utcnow()

        self.meal_service.create(current_user_id=1, name="Meal name")

        end_time = datetime.datetime.utcnow()
        mock_calls = self.meal_repository.create.mock_calls
        assert len(mock_calls) == 1
        mock_call = self.meal_repository.create.mock_calls[0]
        meals = mock_call.args[0]
        assert len(meals) == 2
        for meal, calorie_ninjas_response in zip(meals, self.calorie_ninjas_client.get_meal_descriptions.return_value):
            assert meal.apiData == calorie_ninjas_response
            assert meal.userId == 1
            assert is_time_between(start_time, end_time, meal.creationTime)
        print(mock_calls)

        self.calorie_ninjas_client.get_meal_descriptions.assert_called_once_with("Meal name")

    def test_get_all(self):
        const_creation_time = datetime.datetime.utcnow()
        self.meal_repository.list_by_user_id = MagicMock()
        self.meal_repository.list_by_user_id.return_value = [
            Meal(id=1, userId=1, apiData="data 1", creationTime=const_creation_time),
            Meal(id=2, userId=1, apiData="data 2", creationTime=const_creation_time)]

        response = self.meal_service.list_by_user_id(user_id=1)

        self.meal_repository.list_by_user_id.assert_called_once_with(1)
        assert response == [
            MealSchema(meal_id=1, calorie_ninjas_response="data 1", time=const_creation_time),
            MealSchema(meal_id=2, calorie_ninjas_response="data 2", time=const_creation_time)]

    def test_delete_success(self):
        const_creation_time = datetime.datetime.utcnow()
        self.meal_repository.get = MagicMock()
        self.meal_repository.get.return_value = Meal(id=12, userId=1, apiData="data 1", creationTime=const_creation_time)

        self.meal_service.delete(meal_id=12, user_id=1)

        self.meal_repository.get.assert_called_once_with(12)

    def test_delete_not_found(self):
        self.meal_repository.get = MagicMock()
        self.meal_repository.get.return_value = None

        with pytest.raises(HTTPException) as ex:
            self.meal_service.delete(meal_id=12, user_id=1)

        self.meal_repository.get.assert_called_once_with(12)
        assert ex.value.status_code == 404
        assert ex.value.detail == 'Meal not found'

    def test_delete_forbidden(self):
        const_creation_time = datetime.datetime.utcnow()
        self.meal_repository.get = MagicMock()
        self.meal_repository.get.return_value = Meal(id=12, userId=2, apiData="data 1", creationTime=const_creation_time)

        with pytest.raises(HTTPException) as ex:
            self.meal_service.delete(meal_id=12, user_id=1)

        self.meal_repository.get.assert_called_once_with(12)
        assert ex.value.status_code == 403
        assert ex.value.detail == "No access to this meal"
