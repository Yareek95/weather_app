import os
from flask import Flask, render_template, request, jsonify
import requests



app = Flask(__name__)

BASE_URL = "https://api.weatherapi.com/v1/current.json"
API_KEY = "489b3e24494946a89ca63057231911"

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = None
    weather_data = None

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            params = {
                'key': API_KEY,
                'q': user_input,
                'lang': 'en',  # Replace with your preferred language
            }
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                weather_data = response.json()
            

    return render_template('index.html', user_input=user_input, weather_data=weather_data)



if __name__ == '__main__':
    # Use the environment variable PORT if available, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=port)
