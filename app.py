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

rooms = {}


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/chat", methods=["POST", "GET"])
def chat():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("chat.html", error="Please enter a name", code=code, name=name)

        if join != False and not code:
            return render_template("chat.html", error="Please enter a room code", code=code, name=name)
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("chat.html", error="Room does not exist", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("chat.html")


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("chat"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    # Send the message to the room
    send(content, to=room)

    # Append the message to the room's messages
    rooms[room]["messages"].append(content)
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
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    user_input_weather = None
    first_api = None
    second_api_data = None
    error_message = None

    if request.method == 'POST':
        user_input_weather = request.form.get('user_input')

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

    return render_template('weather.html', user_input=user_input_weather, weather_data=first_api,
                           second_api_data=second_api_data, error_message=error_message)


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
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the password and confirm password match
        if password != confirm_password:
            return render_template('register.html', error_message='Password and confirm password do not match.')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if the username already exists
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            return render_template('register.html', error_message='Username already exists. Choose another.')

        # Insert new user into MongoDB
        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        return redirect(url_for('login'))

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user and bcrypt.check_password_hash(existing_user['password'], password):
            session['username'] = username
            return redirect(url_for('dashboard'))

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

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Guest')
    message = {'username': username, 'message': data['message']}
    mongo.db.chat_messages.insert_one(message)
    emit('message', message, broadcast=True)



'''

    
    *** test ***

    if __name__ == '__main__':
    app.run(debug=True)
    *** test ***
if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False)
  '''

if __name__ == '__main__':
    # Use the environment variable PORT if available, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
