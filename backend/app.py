from flask import Flask, request         # Flask is a lightweight framework and request is a object given by Flask everytime a user do a request
import sqlite3      # python module to connect into the sqlite db
from flask_cors import CORS  # CORS = plugin ; flask_cors = external python library 

app = Flask(__name__)  # initialise the app and inform Flask about the context of execution
CORS(app)  # function to enable cross origin request

def check_credentials(email, password):
    conn = sqlite3.connect('database_file') # Connect to the sqlite db 
    cursor = conn.cursor()  # Creating a cursors 
    cursor.execute("SELECT * FROM USERS WHERE USER_EMAIL = ? AND USERS_PASSWORD = ?", (email, password)) # SQL request with the execute method to search any users in the db with the same email/password than the ones send by the users in the html page
    user = cursor.fetchone() # stocking the corresponding users inside user 
    conn.close() # close the connection to the db
    return user

@app.route('/login', methods=['POST']) # declaring a route for each POST methods to /login 
def login():
    email = request.form.get('email')  # Variable that contains the value put by the user inside the email input (form = ImmutableMultiDict = dict ; get = method of form)
    password = request.form.get('password')

    if not email or not password:  # Here we check if email or password is empty if yes error 400 hhtp
        return "One of the input are empty", 400

    if check_credentials(email, password):  # If the function return yes (He found a user with the same email and password) than return successfull if no than 401 hht error
        return "Successfull !"
    else:
        return "Wrong ID", 401

if __name__ == '__main__':  # if we execute the app.py file than the debug mode is activated if imported than the debugger is off
    app.run(debug=True)