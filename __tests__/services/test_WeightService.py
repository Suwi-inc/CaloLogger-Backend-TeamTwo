import datetime
from unittest import TestCase
from unittest.mock import create_autospec, MagicMock

from app.models.WeightModel import Weight
from app.repositories.WeightRepository import WeightRepository
from app.schemas.pydantic.WeightSchema import WeightSchema
from app.services.WeightService import WeightService


class TestWeightService(TestCase):
    weight_repository: WeightRepository
    weight_service: WeightService

    def setUp(self):
        super().setUp()
        self.weight_repository = create_autospec(
            WeightRepository
        )
        self.weight_service = WeightService(
            self.weight_repository
        )

    def test_add_weight(self):
        self.weight_repository.add_weight = MagicMock()

        self.weight_service.add_weight(user_id=1, kg=69)

        self.weight_repository.add_weight.assert_called_once_with(1, 69)

    def test_get_all_weights(self):
        const_creation_time = datetime.datetime.utcnow()
        self.weight_repository.get_all_weights = MagicMock()
        self.weight_repository.get_all_weights.return_value = [
            Weight(id=1, userId=1, kg=61, creationTime=const_creation_time),
            Weight(id=2, userId=1, kg=62, creationTime=const_creation_time)]

        response = self.weight_service.get_all_weights(user_id=1)

        self.weight_repository.get_all_weights.assert_called_once_with(1)
        assert response == [
            WeightSchema(weight=61, time=const_creation_time),
            WeightSchema(weight=62, time=const_creation_time)]
