from typing import Iterable

import requests

from app.configs.Environment import get_environment_variables

# Runtime Environment Configuration
env = get_environment_variables()


class CalorieNinjasClient:
    def get_meal_descriptions(
        self,
        meals_string: str
    ) -> Iterable[str]:
        items = requests.get(
            url="https://api.calorieninjas.com/v1/nutrition",
            params={'query': meals_string},
            headers={"X-Api-Key": env.CALORIE_NINJAS_API_KEY}
        ).json()['items']
        return [str(item) for item in items]
