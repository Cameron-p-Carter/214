from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'key'

class User:
    def __init__(self, user_name, user_password, flight_booked_ids=None):
        self._user_name = user_name
        self._user_password = user_password
        self._flight_booked_ids = flight_booked_ids or []

    def getUserName(self):
        return self._user_name

    def getUserPassword(self):
        return self._user_password

    def addFlightBooking(self, x):
        self._flight_booked_ids.append(x)

    def getFlightBookingIds(self):
        return self._flight_booked_ids

    def getFlightBookingId(self, x):
        return self._flight_booked_ids[x]

class Flight:
    def __init__(self, flight_id, flight_gate_number, flight_time, flight_departing_location, flight_destination_location, flight_price, flight_available_seats):
        self._flight_id = flight_id
        self._flight_gate_number = flight_gate_number
        self._flight_time = flight_time
        self._flight_departing_location = flight_departing_location
        self._flight_destination_location = flight_destination_location
        self._flight_price = flight_price
        self._flight_available_seats = flight_available_seats

    def getFlightId(self):
        return self._flight_id

    def getFlightGateNumber(self):
        return self._flight_gate_number

    def getFlightTime(self):
        return self._flight_time

    def getFlightDepartingLocation(self):
        return self._flight_departing_location

    def getFlightDestinationLocation(self):
        return self._flight_destination_location

    def getFlightPrice(self):
        return self._flight_price

    def getFlightAvailableSeats(self):
        return self._flight_available_seats

class Manager:
    def __init__(self):
        self._all_users = []
        self._all_flights = {}

    def createUser(self, user_name, user_password):
        new_user = User(user_name, user_password)
        self._all_users.append(new_user)
        self.saveUsers('userdata.json')

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

    def addFlightForUser(self, user, flight_id):
        user.addFlightBooking(flight_id)

    def loadUsers(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for user_data in data['users']:
                user = User(user_data['username'], user_data['password'], user_data.get('flight_booked_ids', []))
                self._all_users.append(user)

    def saveUsers(self, file_path):
        with open(file_path, 'w') as file:
            data = {'users': []}
            for user in self._all_users:
                data['users'].append({
                    'username': user.getUserName(),
                    'password': user.getUserPassword(),
                    'flight_booked_ids': user.getFlightBookingIds()
                })
            json.dump(data, file, indent=4)

    def loadFlights(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for flight_data in data:
                flight = Flight(
                    flight_data['flight_id'],
                    flight_data['flight_gate_number'],
                    flight_data['flight_time'],
                    flight_data['flight_departing_location'],
                    flight_data['flight_destination_location'],
                    flight_data['flight_price'],
                    flight_data['flight_available_seats']
                )
                self._all_flights[flight_data['flight_id']] = flight

manager = Manager()
manager.loadUsers('userdata.json')
manager.loadFlights('flightdata.json')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = manager.authenticateUser(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error_message='Invalid username or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if manager.findUserByUsername(username) is None:
            manager.createUser(username, password)
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('register.html', error_message='Username already exists.')
    return render_template('register.html')

# Add additional routes for userFlights if necessary

if __name__ == '__main__':
    app.run(debug=True)
