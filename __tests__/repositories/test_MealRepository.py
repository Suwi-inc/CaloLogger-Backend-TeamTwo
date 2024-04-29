from unittest import TestCase
from unittest.mock import create_autospec, MagicMock

from sqlalchemy.orm import Session

from app.models.MealModel import Meal
from app.repositories.MealRepository import MealRepository


class TestMealRepository(TestCase):
    session: Session
    meal_repository: MealRepository

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.meal_repository = MealRepository(
            self.session
        )

    def test_create(self):
        meals = [Meal(apiData="data 1"), Meal(apiData="data 2")]
        self.meal_repository.create(meals)

        self.session.add_all.assert_called_once_with(meals)
        self.session.commit.assert_called_once()

    def test_get(self):
        return_meal = Meal(apiData="data 1")
        self.session.get = MagicMock(return_value=return_meal)

        response = self.meal_repository.get(1)

        assert response == return_meal

        self.session.get.assert_called_once_with(Meal, 1)


    def test_delete(self):
        meal = Meal(apiData="data 1")

        self.meal_repository.delete(meal)

        self.session.delete.assert_called_once_with(meal)
        self.session.commit.assert_called_once()
        self.session.flush.assert_called_once()

    def test_list_by_user_id(self):
        return_meal = Meal(apiData="data 1")
        query_mock = MagicMock()
        filtered_query_mock = MagicMock()
        query_mock.filter_by = MagicMock(return_value=filtered_query_mock)
        filtered_query_mock.all = MagicMock(return_value=[return_meal])
        self.session.query = MagicMock(return_value=query_mock)

        results = self.meal_repository.list_by_user_id(1)

        assert results == [return_meal]
        self.session.query.assert_called_once_with(Meal)
        query_mock.filter_by.assert_called_once_with(userId=1)
        filtered_query_mock.all.assert_called_once_with()