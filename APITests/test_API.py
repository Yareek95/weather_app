import unittest
import requests

class TestWeatherAPI(unittest.TestCase):
    BASE_URL = "https://api.weatherapi.com/v1/current.json"
    API_KEY = "489b3e24494946a89ca63057231911"  # Replace with your API key

    def test_successful_request(self):
        params = {
            'key': self.API_KEY,
            'q': 'London',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('current' in response.json())

    def test_invalid_location(self):
        params = {
            'key': self.API_KEY,
            'q': 'InvalidLocation123',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 400)  # Assuming a 400 status code for an invalid location
        self.assertTrue('error' in response.json())

    def test_missing_api_key(self):
        params = {
            'q': 'London',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 401)  # Assuming a 401 status code for a missing API key
        self.assertTrue('error' in response.json())

if __name__ == '__main__':
    unittest.main()
