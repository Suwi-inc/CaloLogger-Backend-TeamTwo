import datetime
from unittest import TestCase
from unittest.mock import create_autospec, MagicMock

from sqlalchemy.orm import Session

from app.models.WeightModel import Weight
from app.repositories.WeightRepository import WeightRepository
from __tests__.common.DatetimeHelpers import is_time_between


class TestWeightRepository(TestCase):
    session: Session
    weight_repository: WeightRepository

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.weight_repository = WeightRepository(
            self.session
        )

    def test_add(self):
        start_time = datetime.datetime.utcnow()

        returned_weight = self.weight_repository.add_weight(1, 2)

        end_time = datetime.datetime.utcnow()

        for session_func in [self.session.add, self.session.refresh]:
            assert session_func.call_count == 1
            weight = session_func.mock_calls[0].args[0]
            assert is_time_between(start_time, end_time, weight.creationTime)
            assert weight.kg == 2
            assert weight.userId == 1
            assert weight == returned_weight

        self.session.commit.assert_called_once()

    def test_get_all_weights(self):
        return_weight = Weight(kg=98)
        query_mock = MagicMock()
        filtered_query_mock = MagicMock()
        query_mock.filter_by = MagicMock(return_value=filtered_query_mock)
        filtered_query_mock.all = MagicMock(return_value=[return_weight])
        self.session.query = MagicMock(return_value=query_mock)

        results = self.weight_repository.get_all_weights(1)

        assert results == [return_weight]
        self.session.query.assert_called_once_with(Weight)
        query_mock.filter_by.assert_called_once_with(userId=1)
        filtered_query_mock.all.assert_called_once_with()