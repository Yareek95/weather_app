import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

FIRST_API_BASE_URL = "https://api.weatherapi.com/v1/current.json"   #base weather
SECOND_API_BASE_URL = "https://www.amdoren.com/api/weather.php"     #forecast weather
CURRENCY_API_BASE_URL = "https://www.amdoren.com/api/currency.php"  #currency

FIRST_API_KEY = "489b3e24494946a89ca63057231911"
# SECOND and CURRENCY have the same KEY:
SECOND_API_KEY = "RSHPS94EemhCEY7QNBfQundpqnUtVk"

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input_weather = None
    first_api = None
    second_api_data = None
    currency_data = None
    error_message = None

    if request.method == 'POST':
        user_input_weather = request.form.get('user_input')
        user_input_currency_1 = request.form.get('user_input_currency_1')
        user_input_currency_2 = request.form.get('user_input_currency_2')
        amount = request.form.get('user_input_amount', 1)  # default amount is 1

        if user_input_weather:
            # Weather API Call
            params_first_api = {
                'key': FIRST_API_KEY,
                'q': user_input_weather,
                'lang': 'en',
            }
            response_first_api = requests.get(FIRST_API_BASE_URL, params=params_first_api)

            if response_first_api.status_code == 200:
                first_api = response_first_api.json()
                # Extract latitude and longitude
                lat = first_api['location']['lat']
                lon = first_api['location']['lon']
                # Second API Call
                params_second_api = {
                    'api_key': SECOND_API_KEY,
                    'lat': lat,
                    'lon': lon,
                }
                response_second_api = requests.get(SECOND_API_BASE_URL, params=params_second_api)
                if response_second_api.status_code == 200:
                    second_api_data = response_second_api.json()
                else:
                    error_message = f"Error: {response_second_api.json().get('error_message', 'Unknown error')}"
            else:
                error_message = f"Error: {response_first_api.status_code}"

        elif user_input_currency_1 and user_input_currency_2:
            # Currency API Call
            params_currency_api = {
                'api_key': SECOND_API_KEY,
                'from': user_input_currency_1,
                'to': user_input_currency_2,
                'amount': amount,
            }
            response_currency_api = requests.get(CURRENCY_API_BASE_URL, params=params_currency_api)

            if response_currency_api.status_code == 200:
                currency_data = response_currency_api.json()
            else:
                error_message = f"Error: {response_currency_api.json().get('error_message', 'Unknown error')}"

    return render_template('index.html', user_input=user_input_weather, weather_data=first_api,
                           second_api_data=second_api_data, currency_data=currency_data, error_message=error_message)

if __name__ == '__main__':
    # Use the environment variable PORT if available, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
