import random
import time
from typing import List
from unittest import TestCase

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By


class MealInfo:

    def __init__(self, name: str, time: str, stats: List[str]):
        self.name = name
        self.time = time
        self.stats = stats

    def as_tuple(self, no_time: bool = False):
        if no_time:
            return self.name, self.stats
        return self.name, self.time, self.stats


class TestUi(TestCase):

    def get_meal_info_by_index(self, driver: webdriver.Firefox, index: int) -> MealInfo:
        print(index)
        name = driver.find_element(By.CSS_SELECTOR,
                                   f'div.MuiGrid-root:nth-child({index + 1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)').text
        time = driver.find_element(By.CSS_SELECTOR,
                                   f'div.MuiGrid-root:nth-child({index + 1}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > p:nth-child(2)').text
        stats = list([driver.find_element(By.CSS_SELECTOR,
                                          f'div.MuiGrid-root:nth-child({index + 1}) > div:nth-child(1) > div:nth-child(1) > p:nth-child({2 + stat_index})').text
                      for stat_index in range(0, 11)])
        meal_info = MealInfo(name, time, stats)
        print(meal_info.name)
        print(meal_info.time)
        print(meal_info.stats)
        return meal_info

    def gradually_delete_all_meals_and_assert_expected_behaviour(self, driver: webdriver.Firefox):
        meals_grid = driver.find_element(By.CSS_SELECTOR, '.MuiGrid-root')
        all_meals = meals_grid.find_elements(By.XPATH, "./*")
        print(f"num of meals is {len(all_meals)}")
        all_meal_infos = list([self.get_meal_info_by_index(driver, i) for i in range(len(all_meals))])

        while len(all_meals) >= 1:
            meal_1 = all_meals[0]
            meal_1.find_elements(By.CLASS_NAME, "MuiButtonBase-root")[0].click()

            # Wait for removal
            time.sleep(1)

            updated_all_meals = meals_grid.find_elements(By.XPATH, "./*")
            updated_meal_infos = list([self.get_meal_info_by_index(driver, i) for i in range(len(updated_all_meals))])
            assert [i.as_tuple() for i in updated_meal_infos] == (list([i.as_tuple() for i in all_meal_infos[1:]]))
            assert len(updated_all_meals) == len(all_meals) - 1

            all_meals = updated_all_meals
            all_meal_infos = updated_meal_infos

        assert all_meals == []

    def test_full_workflow(self):
        options = FirefoxOptions()
        options.add_argument('--headless')  # Comment for visible browser
        driver = webdriver.Firefox(
            options=options)
        driver.get('https://calo.rinri-d.xyz/register')

        time.sleep(2)

        random_gen = random.Random()
        test_name = str(random_gen.randint(1, 1000000))
        test_password = str(random_gen.randint(1, 1000000))

        self.signup(driver, test_name, test_password)

        # Wait for all events
        time.sleep(2)

        self.login(driver, test_name, test_password)

        # Wait for all events
        time.sleep(2)

        self.gradually_delete_all_meals_and_assert_expected_behaviour(driver)

        meal_inputter = driver.find_elements(By.CLASS_NAME, "MuiInputBase-input")[0]
        meal_inputter.send_keys("omelet and eggs")

        meal_send = driver.find_elements(By.CLASS_NAME,
                                         "MuiButtonBase-root")[1]
        meal_send.click()

        # Wait all interactions and update
        time.sleep(8)

        meals_grid = driver.find_element(By.CSS_SELECTOR, '.MuiGrid-root')
        all_meals = meals_grid.find_elements(By.XPATH, "./*")
        assert len(all_meals) == 2

        meal_infos = list([self.get_meal_info_by_index(driver, i) for i in range(2)])
        assert [i.as_tuple(no_time=True) for i in meal_infos] == [
            ('omelet', ['Calories: 176.3',
                        'Serving Size: 100g',
                        'Fat Total: 13.9g',
                        'Fat Saturated: 3.3g',
                        'Protein: 11.7g',
                        'Sodium: 294mg',
                        'Potassium: 189mg',
                        'Cholesterol: 351mg',
                        'Carbohydrates Total: 0.8g',
                        'Fiber: 0g',
                        'Sugar: 0.4g']),
            ('eggs', ['Calories: 144.3',
                      'Serving Size: 100g',
                      'Fat Total: 9.4g',
                      'Fat Saturated: 3.1g',
                      'Protein: 12.6g',
                      'Sodium: 143mg',
                      'Potassium: 200mg',
                      'Cholesterol: 373mg',
                      'Carbohydrates Total: 0.7g',
                      'Fiber: 0g',
                      'Sugar: 0.4g'])
        ]

        self.gradually_delete_all_meals_and_assert_expected_behaviour(driver)

    def login(self, driver, test_name, test_password):
        login_inputter = driver.find_elements(By.CLASS_NAME, "MuiInputBase-input")[0]
        login_inputter.click()
        login_inputter.send_keys(test_name)
        password_inputter = driver.find_elements(By.CLASS_NAME, "MuiInputBase-input")[1]
        password_inputter.click()
        password_inputter.send_keys(test_password)
        login_button = driver.find_elements(By.CLASS_NAME, 'MuiButtonBase-root')[0]
        login_button.click()

    def signup(self, driver, test_name, test_password):
        login_inputter = driver.find_elements(By.CLASS_NAME, "MuiInputBase-input")[0]
        login_inputter.click()
        login_inputter.send_keys(test_name)
        password_inputter = driver.find_elements(By.CLASS_NAME, "MuiInputBase-input")[1]
        password_inputter.click()
        password_inputter.send_keys(test_password)
        register_button = driver.find_elements(By.CLASS_NAME, 'MuiButtonBase-root')[0]
        register_button.click()
