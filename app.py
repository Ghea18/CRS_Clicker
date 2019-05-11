import os
import sys
import requests
import time

from flask import Flask, session, render_template, request, redirect, url_for, jsonify, make_response
from flask_session import Session
from flask_socketio import SocketIO, emit
from flask_hashing import Hashing as Hashing
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from database import db_session


# Setting APP
app = Flask(__name__)

# Configure app to use in filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["HASHING_METHOD"] = "sha256"
app.config["SECRET_KEY"] = "lkkajdghdadkglajkgah" # a secret key for login

# Init some fungtion needed in app
Session(app)
socketio = SocketIO(app, manage_session=False)
hash = Hashing(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index' # the login view of your application
login_manager.login_message = 'Silahkan login utuk dapat mengakses halaman.'
login_manager.login_message_category = "warning"

# Prepare Global Variable
data_response = [{"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}]
responden = []
response_done = False

class User(UserMixin):
  def __init__(self,id):
    self.id = id

# Route to login
@app.route("/")
@app.route("/index")
def index():  
    return render_template("index.html")

# Route to response
@app.route("/answer")
@login_required
def answer():
    # Display Instrument Page
    return render_template("answer.html", data_response=session['data_response'], username=session['user_name'], number=session['number'], session_code=session['session_code'])

# Route to response
@app.route("/result")
@login_required
def result():
    # Display Instrument Page
    return render_template("result.html", username=session['user_name'], session_code=session['session_code'])

# Route for reset
@app.route('/reset', methods=["POST", "GET"])
def reset():
    data_response.clear()
    data_response.append({"A": 0, "B": 0, "C": 0, "D": 0, "E": 0})
    responden.clear()
    print(data_response)
    return redirect(url_for('logout'))

# Route for login
@app.route('/login', methods=["POST"])
def login():
    # Cek if user request via POST
    if request.method == 'POST':
        # clear user data in session
        session.clear()

        # Cek if user request via POST
        user = request.form['username']
        code = "Pemrograman_WEB"

        # Save login data into sessions
        login_user(User(1))
        session['logged_in'] = True
        session['user_id'] = 1
        session['user_name'] = user
        session['session_code'] = code
        session['number'] = 1
        session['number_cek'] = [0]
        session['data_response'] = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
        responden.append(user)
        # Welcome user and redirected to book page
        sys.stdout.flush()
        if user == 'admin':
            return redirect(url_for('result'))
        else:
            return redirect(url_for('answer'))

# ROute for logout
@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    # remove the username from the session if it's there
    logout_user()
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.clear()
    return redirect(url_for('index'))

#=============================================
# SocketIO Route
#=============================================
# SocketIO to catch response
@socketio.on("submit response")
@login_required
def response(data):
    session['logged_in'] = True
    session['user_id'] = 1

    # Catch selection data that emitted from client
    selection = data["selection"]
    number = session['number']
    # Increase counter of selection
    lib = set(session['number_cek'])
    if number not in lib:
        data_response[number-1][selection] += 1
        session['number_cek'].append(session['number'])
    emit("response number", f"{session['number']} (done)")
    # Emits data_response to display to client
    emit("response admin_people", responden, broadcast=True)
    emit("response admin_totals", data_response, broadcast=True)

# Route to next
@socketio.on("next response")
@login_required
def next():
    # Increase counter of number
    session['number'] += 1
    if len(data_response) < session['number']:
        data_response.append({"A": 0, "B": 0, "C": 0, "D": 0, "E": 0})
    # Emits data_response to display to client
    emit("response number", session['number'])

# Route to next
@socketio.on("back response")
@login_required
def back():
    # Increase counter of number
    if session['number'] > 1:
        session['number'] -= 1
    print(session['number'])
    # Emits data_response to display to client
    emit("response number", session['number'])

# Route to next
@socketio.on("done response")
@login_required
def done(data):
    # Emits data_response to display to client
    emit("response people", responden, broadcast=True)
    emit("response totals", data_response, broadcast=True)

# Route to next
@socketio.on("reset response")
@login_required
def reset(data):
    data_response.clear()
    data_response.append({"A": 0, "B": 0, "C": 0, "D": 0, "E": 0})
    responden.clear()
    emit("response admin_people", responden, broadcast=True)
    emit("response admin_totals", data_response, broadcast=True)

#=============================================
# LOGIN SETTUP 
#=============================================
# Route to manage user
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Route to rejected user handler
@login_manager.unauthorized_handler
def unauthorized():
    # Redirect to home
    response = make_response(redirect(url_for('index'), code=302))
    response.headers['url'] = 'parachutes are cool'
    return response

# Route to after logout
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
	# Runing SocketIO
	socketio.run(app)
