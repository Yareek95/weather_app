import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://api.weatherapi.com/v1/current.json"
SECOND_API_BASE_URL = "https://www.amdoren.com/api/weather.php"
API_KEY = "489b3e24494946a89ca63057231911"

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = None
    weather_data = None
    second_api_data = None

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            # First API Call
            params_first_api = {
                'key': API_KEY,
                'q': user_input,
                'lang': 'en',
            }
            response_first_api = requests.get(BASE_URL, params=params_first_api)

            if response_first_api.status_code == 200:
                weather_data = response_first_api.json()

                # Extract latitude and longitude
                lat = weather_data['location']['lat']
                lon = weather_data['location']['lon']

                # Second API Call
                params_second_api = {
                    'api_key': '489b3e24494946a89ca63057231911',  # Replace with your second API key
                    'lat': lat,
                    'lon': lon,
                }
                response_second_api = requests.get(SECOND_API_BASE_URL, params=params_second_api)

                if response_second_api.status_code == 200:
                    second_api_data = response_second_api.json()

    return render_template('index.html', user_input=user_input, weather_data=weather_data, second_api_data=second_api_data)

if __name__ == '__main__':
    # Use the environment variable PORT if available, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
