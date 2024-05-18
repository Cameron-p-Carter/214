from flask import Flask, render_template, request, redirect, url_for, session
import json


class User():
    def __init__(self, user_name, user_password):
        self._user_name = user_name
        self._user_password = user_password
        self._flights = []
   
    def getUserName(self):
        return self._user_name
   
    def getUserPassword(self):
        return self._user_password
   
    def addFlight(self, x):
        self._flights.append(x)

    def getFlights(self):
        return self._flights

    def getFlight(self, x):
        return self._flight[x]


class Flight():
    def __init__(self, flight_name, flight_seat_number, flight_time):
        self._flight_name = flight_name
        self._flight_seat_number = flight_seat_number
        self._flight_time = flight_time

    def getFlightName(self):
        return self._flight_name
   
    def getFlightSeatNumber(self):
        return self._flight_seat_number
   
    def getFlightTime(self):
        return self._flight_time


   
   
class Manager:
    def __init__(self):
        self._all_users = []

    def createUser(self, user_name, user_password):
        new_user = User(user_name, user_password)
        self._all_users.append(new_user)

    def findUserByUsername(self, user_name):
        for user in self._all_users:
            if user.getUserName() == user_name:
                return user
        return None
   
    def authenticateUser(self, user_name, user_password):
        for user in self._all_users:
            if user.getUserName() == user_name and user.getUserPassword() == user_password:
                return user
        return None
   
    def addFlightForUser(self, user, flight_name, flight_seat_number, flight_time):
        new_flight = Flight(flight_name, flight_seat_number, flight_time)
        user.addFlight(new_flight)

    def loadDataFromJsonFile(self):
        try:
            with open('password_data.json', 'r') as file:
                data = json.load(file)
                for user_data in data.get('users', []):
                    user = User(user_data['username'], user_data['password'])
                    for flight_data in user_data.get('flights', []):
                        flight = Flight(flight_data['flight_name'], flight_data['username'], flight_data['password'])
                        user.addFlight(flight)
                    self._all_users.append(user)
        except FileNotFoundError:
            pass

    def saveDataToJsonFile(self):
        data = {"users": []}
        for user in self._all_users:
            user_data = {"username": user.getUserName(), "password": user.getUserPassword(), "flights": []}
            for flight in user.getFlights():
                flight_data = {"flight_name": flight.getFlightName(), "username": flight.getFlightSeatNumber(), "password": flight.getFlightTime()}
                user_data["flights"].append(flight_data)
            data["users"].append(user_data)

        with open('password_data.json', 'w') as file:
            json.dump(data, file)






app = Flask(__name__)
manager = Manager()
manager.loadDataFromJsonFile()



@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = manager.authenticateUser(username, password)

    if user:
        session['user'] = {
            'user_name': user.getUserName(),
            'user_password': user.getUserPassword(),
            'flights': [{'flight_name': flight.getFlightName(), 'username': flight.getFlightSeatNumber(), 'password': flight.getFlightTime()} for flight in user.getFlights()]
        }
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error_message="Incorrect username or password")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        manager.createUser(username, password)
        manager.saveDataToJsonFile()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_data = session.get('user')
    if not user_data:
        return redirect(url_for('login'))

    user = User(user_data['user_name'], user_data['user_password'])
    for flight_data in user_data['flights']:
        flight = Flight(flight_data['flight_name'], flight_data['username'], flight_data['password'])
        user.addFlight(flight)

    if request.method == 'POST':
        flight_name = request.form['flight_name']
        flight_seat_number = request.form['flight_seat_number']
        flight_time = request.form['flight_time']

        user.addFlight(Flight(flight_name, flight_seat_number, flight_time))

        existing_user = manager.findUserByUsername(user.getUserName())
        existing_user.getFlights().append(Flight(flight_name, flight_seat_number, flight_time))

        manager.saveDataToJsonFile()

    return render_template('dashboard.html', user=user)


app.secret_key = 'key'

if __name__ == '__main__':
    app.run(debug=True)