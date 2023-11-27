import unittest
import requests

class TestWeatherAPI(unittest.TestCase):
    BASE_URL = "https://api.weatherapi.com/v1/current.json"
    API_KEY = "489b3e24494946a89ca63057231911"

    def test_successful_request(self):
        params = {
            'key': self.API_KEY,
            'q': 'London',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('current' in response.json())

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

    def test_invalid_location(self):
        params = {
            'key': self.API_KEY,
            'q': 'InvalidLocation123',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_missing_api_key(self):
        params = {
            'q': 'London',
            'lang': 'en',
        }
        response = requests.get(self.BASE_URL, params=params)

        self.assertEqual(response.status_code, 401)
        self.assertTrue('error' in response.json())

    def test_response_data(self):
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
        # Add more assertions for other response data fields

if __name__ == '__main__':
    unittest.main()
