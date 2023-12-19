import os
import unittest
from dotenv import load_dotenv
import requests

# Load environment variables from the .env file      (.env is in .gitignore)
load_dotenv()


class TestWeatherAPI(unittest.TestCase):
    BASE_URL = "https://api.weatherapi.com/v1/current.json"
    API_KEY = os.environ.get("FIRST_API_KEY")

    def test_successful_request(self):
        params = {
            'key': self.API_KEY,
            'q': 'London',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('current' in response.json())
        print("test_successful_request: 200 success")

    def test_town_displayed(self):
        params = {
            'key': self.API_KEY,
            'q': 'London',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('current' in response.json())
        self.assertTrue('location' in response.json())
        self.assertTrue('name' in response.json()['location'])
        print("test_town_displayed: 200 success")

    def test_invalid_location(self):
        params = {
            'key': self.API_KEY,
            'q': 'InvalidLocation123',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())
        print("test_invalid_location: 400 success")

    def test_missing_api_key(self):
        params = {
            'q': 'London',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 401)
        self.assertTrue('error' in response.json())
        print("test_missing_api_key: 401 success")

    def test_response_data1(self):
        params = {
            'key': self.API_KEY,
            'q': 'Chicago',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('location' in data)
        self.assertTrue('current' in data)
        self.assertTrue('last_updated' in data['current'])
        self.assertTrue('temp_c' in data['current'])
        self.assertTrue('temp_f' in data['current'])
        print("test_response_data1: 200 success")

    def test_response_data2(self):
        params = {
            'key': self.API_KEY,
            'q': 'Chicago',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('location' in data)
        self.assertTrue('current' in data)
        self.assertTrue('last_updated' in data['current'])
        self.assertTrue('wind_mph' in data['current'])
        self.assertTrue('feelslike_c' in data['current'])
        print("test_response_data2: 200 success")


class TestSecondAPI(unittest.TestCase):
    BASE_URL = "https://www.amdoren.com/api/weather.php"
    API_KEY = os.environ.get("SECOND_API_KEY")


    def test_valid_request(self):
        # Test a valid request to the API
        params = {
            'api_key': self.API_KEY,
            "lat": 41.85,
            "lon": -87.65,
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        # Check if the response has the expected keys
        self.assertIn("error", data)
        self.assertIn("error_message", data)
        self.assertIn("forecast", data)

        # Check if the forecast is a list
        self.assertIsInstance(data["forecast"], list)

        # Check if each forecast entry has the expected keys
        for entry in data["forecast"]:
            self.assertIn("date", entry)
            self.assertIn("avg_c", entry)
            self.assertIn("min_c", entry)
            self.assertIn("max_c", entry)
            self.assertIn("avg_f", entry)
            self.assertIn("min_f", entry)
            self.assertIn("max_f", entry)
            self.assertIn("summary", entry)
            self.assertIn("icon", entry)
        print("test_valid_request: success")

    def test_invalid_request(self):
        # Test an invalid request to the API (example: missing lat and lon)
        response = requests.get(self.BASE_URL)
        data = response.json()

        # Check if the response has the expected keys
        self.assertIn("error", data)
        self.assertIn("error_message", data)
        #self.assertNotIn("forecast", data)

        # Check if the error message indicates a validation error
        #self.assertEqual(data["error"], 1)
        self.assertEqual(data["error_message"], "Latitude must be numeric: ")
        print("test_invalid_request: error success")


class TestCurrencyAPI(unittest.TestCase):
    BASE_URL = "https://www.amdoren.com/api/currency.php"
    API_KEY = os.environ.get("SECOND_API_KEY")      #Currency API key same as Second API key

    def test_successful_conversion(self):
        # Test a valid request to the API for currency conversion
        params = {
            "api_key": self.API_KEY,
            "from": "USD",
            "to": "UAH",
            "amount": 100
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        # Check if the response has the expected keys
        self.assertIn("error", data)
        self.assertIn("error_message", data)
        self.assertIn("amount", data)

        # Check if the error is 0, indicating a successful conversion
        self.assertEqual(data["error"], 0)
        self.assertEqual(data["error_message"], "-")

        # Check if the amount is a numeric value
        self.assertIsInstance(data["amount"], (int, float))
        print("test_successful_conversion: success")

    def test_invalid_conversion(self):
        # Test an invalid request to the API (example: missing 'from' currency)
        params = {
            "api_key": self.API_KEY,
            "to": "UAH",
            "amount": 100
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        # Check if the response has the expected keys
        self.assertIn("error", data)
        self.assertIn("error_message", data)
        # Check if the 'amount' key is present but is "inf" when there is an error
        if data["error"] != 0:
            self.assertIn("amount", data)
            self.assertEqual(data["amount"], float('inf'))

            # Check if the 'amount' key is present and its value is "inf" when there is an error
            if data["error"] != 0:
                self.assertIn("amount", data)
                self.assertEqual(data["amount"], float('inf'))
                self.assertEqual(data["error_message"], "-")

            # Check if the error message indicates a validation error
            self.assertEqual(data["error"], 0)
        print("test_invalid_conversion: success")


if __name__ == '__main__':
    unittest.main()
