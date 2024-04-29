import datetime
import sqlite3
from unittest import TestCase
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from httpx import QueryParams

from __tests__.common.DatetimeHelpers import is_time_between
from app.clients.CaloriteNinjasClient import CalorieNinjasClient
from app.main import app


class TestMealRouter(TestCase):
    calorie_ninjas_client: CalorieNinjasClient
    client: TestClient

    def setUp(self):
        super().setUp()
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        cur.execute("DELETE FROM meals")
        con.commit()
        con.close()

        self.calorie_ninjas_client = MagicMock()
        app.dependency_overrides[CalorieNinjasClient] = lambda _: self.calorie_ninjas_client
        self.client = TestClient(app)

    def tearDown(self):
        super().tearDown()
        app.dependency_overrides[CalorieNinjasClient] = None

    def test_create(self):
        self.calorie_ninjas_client.get_meal_descriptions = \
            MagicMock(return_value=["{some json 1}", "{some json2}"])
        start_time = datetime.datetime.utcnow()

        resp = self.client.post(
            "/v1/meal/",
            params=QueryParams({'args': '...', "_": "...", "kwargs": "...", 'name': 'Omelet'}),
            headers={'accept': 'application/json'}, )

        assert resp.status_code == 201
        print(resp.text)
        self.calorie_ninjas_client.get_meal_descriptions.assert_called_once()

        end_time = datetime.datetime.utcnow()

        con = sqlite3.connect("test.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM meals").fetchall()
        assert len(res) == 2
        for meal, api_json in zip(res, ["{some json 1}", "{some json2}"]):
            assert meal[1] == 1  # TODO: user id from auth
            assert is_time_between(start_time, end_time,
                                   datetime.datetime.strptime(meal[2], "%Y-%m-%d %H:%M:%S.%f"))
