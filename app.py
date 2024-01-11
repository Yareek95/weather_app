import os
from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import requests
import secrets
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import random
from string import ascii_uppercase
from datetime import datetime
import pytz

# Specify the time zone as Central Time
central_timezone = pytz.timezone('America/Chicago')

load_dotenv()  # Load environment variables from .env file
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

FIRST_API_BASE_URL = "https://api.weatherapi.com/v1/current.json"  # base weather
SECOND_API_BASE_URL = "https://www.amdoren.com/api/weather.php"  # forecast weather
CURRENCY_API_BASE_URL = "https://www.amdoren.com/api/currency.php"  # currency

FIRST_API_KEY = os.environ.get("FIRST_API_KEY")
# SECOND and CURRENCY have the same KEY:
SECOND_API_KEY = os.environ.get("SECOND_API_KEY")
MONGO_DB_PASSWORD = os.environ.get("MONGO_DB_PASSWORD")

app.config['MONGO_URI'] = f"mongodb+srv://Yarik:{MONGO_DB_PASSWORD}@login.wrtuhbw.mongodb.net/weather-app"
socketio = SocketIO(app)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

global_chat_collection = mongo.db.global_chat
rooms = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/chat", methods=["POST", "GET"])
def chat():
    if 'username' in session:
        name = session['username']
        #glob_chat = request.form.get("global_chat")

        room = "Global Chat"
        rooms[room] = {"members": 0, "messages": []}

        # Retrieve message history from MongoDB
        messages = global_chat_collection.find()
        message_history = [{"name": msg["name"], "message": msg["message"], "timestamp": msg["timestamp"]} for msg in messages]
        rooms[room]["messages"] = message_history

        session["room"] = room
        session["name"] = name
        return render_template("room.html", messages=rooms[room]["messages"])

    session.clear()
    return redirect(url_for("login"))


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"],
        "timestamp": datetime.now(central_timezone).strftime("%Y-%m-%d %H:%M:%S")
    }

    # Send the message to the room
    send(content, to=room)

    # Append the message to the room's messages
    rooms[room]["messages"].append(content)
    # If it's the global chat, also store the message in MongoDB
    if room == "Global Chat":
        global_chat_collection.insert_one(content)

    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    send({"name": name, "message": "has left the room"}, to=room)


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    user_input_weather = request.form.get('user_input')
    temperature_unit = request.form.get('temperature_unit')
    # Set default values if not provided
    user_input_weather = user_input_weather if user_input_weather else 'Chicago'
    temperature_unit = temperature_unit if temperature_unit else 'fahrenheit'

    first_api = None
    second_api_data = None
    error_message = None

    if request.method in ['GET', 'POST']:
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
                lat = first_api.get('location', {}).get('lat')
                lon = first_api.get('location', {}).get('lon')

                # Second API Call
                if lat is not None and lon is not None:
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
                    error_message = "Latitude or longitude not available in the first API response."
            else:
                error_message = f"Error: {response_first_api.status_code}"

    return render_template('weather.html', user_input=user_input_weather, temperature_unit=temperature_unit,
                           weather_data=first_api, second_api_data=second_api_data, error_message=error_message,
                           temperature_c=first_api['current']['temp_c'], temperature_f=first_api['current']['temp_f'],
                           forecast_data=second_api_data['forecast'])


@app.route('/currency', methods=['GET', 'POST'])
def currency():
    user_input_currency_1 = None
    user_input_currency_2 = None
    amount = None
    currency_data = None
    error_message = None

    if request.method == 'POST':
        user_input_currency_1 = request.form.get('user_input_currency_1')
        user_input_currency_2 = request.form.get('user_input_currency_2')
        amount = request.form.get('user_input_amount', 100)  # default amount is 1

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

    return render_template('currency.html', user_input_currency_1=user_input_currency_1,
                           user_input_currency_2=user_input_currency_2, user_input_amount=amount,
                           currency_data=currency_data, error_message=error_message)


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    print(mongo.db)  # Add this line to check the value of mongo.db
    if request.method == 'POST':
        username = request.form['username'].lower()     # Convert to lowercase

        if len(username) < 2:
            return render_template('register.html', error_message='Username is too short. (must be >= 2)')
        if len(username) > 8:
            return render_template('register.html', error_message='Username must be less than 9 characters.')
        if not username[:2].isalpha():
            return render_template('register.html', error_message='Username must start with at least 2 letters.')
        if not all(char.isalnum() or char in ('_', '-') for char in username):
            return render_template('register.html', error_message='Username can only contain letters, numbers,'
                                                                  ' underscores, or hyphens.')

        password = request.form['password']

        if len(password) < 4:
            return render_template('register.html', error_message='Password is too short. (must be >= 4)')
        confirm_password = request.form['confirm_password']

        if len(password) > 10:
            return render_template('register.html', error_message='Password must be less than 11 characters.')
        confirm_password = request.form['confirm_password']

        # Check if the password and confirm password match
        if password != confirm_password:
            return render_template('register.html', error_message='Password and confirm password do not match.')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if the username already exists
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            return render_template('register.html', error_message='Username was taken by someone else.')

        # Insert new user into MongoDB
        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        return redirect(url_for('login'))

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()     # Convert to lowercase
        password = request.form['password']
        # Check if the username exists
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user and bcrypt.check_password_hash(existing_user['password'], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        if existing_user and not bcrypt.check_password_hash(existing_user['password'], password):
            return render_template('login.html', error_message='Wrong Password, but not the Username 😉')
        if not existing_user:
            return render_template('login.html', error_message='Wrong Username')

    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/about')
def about():
    username = session.get('username')
    return render_template('about.html', username=username)

'''

    *** test ***
if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
  '''

if __name__ == '__main__':
    # Use the environment variable PORT if available, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)