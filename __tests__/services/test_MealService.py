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
    MealRepository: MealRepository
    CalorieNinjasClient: CalorieNinjasClient
    MealService: MealService

    def setUp(self):
        super().setUp()
        self.MealRepository = create_autospec(
            MealRepository
        )
        self.CalorieNinjasClient = create_autospec(
            CalorieNinjasClient
        )
        self.MealService = MealService(
            self.MealRepository,
            self.CalorieNinjasClient
        )

    def test_create(self):
        self.CalorieNinjasClient.get_meal_descriptions = MagicMock()
        self.MealRepository.create = MagicMock()
        self.CalorieNinjasClient.get_meal_descriptions.return_value = ["{some json 1}", "{some json2}"]
        start_time = datetime.datetime.utcnow()

        self.MealService.create(current_user_id=1, name="Meal name")

        end_time = datetime.datetime.utcnow()
        mock_calls = self.MealRepository.create.mock_calls
        assert len(mock_calls) == 1
        mock_call = self.MealRepository.create.mock_calls[0]
        meals = mock_call.args[0]
        assert len(meals) == 2
        for meal, calorie_ninjas_response in zip(meals, self.CalorieNinjasClient.get_meal_descriptions.return_value):
            assert meal.apiData == calorie_ninjas_response
            assert meal.userId == 1
            assert is_time_between(start_time, end_time, meal.creationTime)
        print(mock_calls)

        self.CalorieNinjasClient.get_meal_descriptions.assert_called_once_with("Meal name")

    def test_get_all(self):
        const_creation_time = datetime.datetime.utcnow()
        self.MealRepository.list_by_user_id = MagicMock()
        self.MealRepository.list_by_user_id.return_value = [
            Meal(id=1, userId=1, apiData="data 1", creationTime=const_creation_time),
            Meal(id=2, userId=1, apiData="data 2", creationTime=const_creation_time)]

        response = self.MealService.list_by_user_id(user_id=1)

        self.MealRepository.list_by_user_id.assert_called_once_with(1)
        assert response == [
            MealSchema(meal_id=1, calorie_ninjas_response="data 1", time=const_creation_time),
            MealSchema(meal_id=2, calorie_ninjas_response="data 2", time=const_creation_time)]

    def test_delete_success(self):
        const_creation_time = datetime.datetime.utcnow()
        self.MealRepository.get = MagicMock()
        self.MealRepository.get.return_value = Meal(id=12, userId=1, apiData="data 1", creationTime=const_creation_time)

        self.MealService.delete(meal_id=12, user_id=1)

        self.MealRepository.get.assert_called_once_with(12)

    def test_delete_not_found(self):
        self.MealRepository.get = MagicMock()
        self.MealRepository.get.return_value = None

        with pytest.raises(HTTPException) as ex:
            self.MealService.delete(meal_id=12, user_id=1)

        self.MealRepository.get.assert_called_once_with(12)
        assert ex.value.status_code == 404
        assert ex.value.detail == 'Meal not found'

    def test_delete_forbidden(self):
        const_creation_time = datetime.datetime.utcnow()
        self.MealRepository.get = MagicMock()
        self.MealRepository.get.return_value = Meal(id=12, userId=2, apiData="data 1", creationTime=const_creation_time)

        with pytest.raises(HTTPException) as ex:
            self.MealService.delete(meal_id=12, user_id=1)

        self.MealRepository.get.assert_called_once_with(12)
        assert ex.value.status_code == 403
        assert ex.value.detail == "No access to this meal"
