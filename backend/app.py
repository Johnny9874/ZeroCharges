from flask import Flask, request         # Flask is a lightweight framework and request is a object given by Flask everytime a user do a request
import sqlite3      # python module to connect into the sqlite db
from flask_cors import CORS  # CORS = plugin ; flask_cors = external python library 

app = Flask(__name__)  # initialise the app and inform Flask about the context of execution
CORS(app, resources={r"/*": {"origins": "*"}})  # function to enable cross origin request from all origin

def check_credentials(email, password):
    conn = sqlite3.connect('database_file') # Connect to the sqlite db 
    cursor = conn.cursor()  # Creating a cursors 
    cursor.execute("SELECT * FROM USERS WHERE USER_EMAIL = ? AND USERS_PASSWORD = ?", (email, password)) # SQL request with the execute method to search any users in the db with the same email/password than the ones send by the users in the html page
    user = cursor.fetchone() # stocking the corresponding users inside user 
    conn.close() # close the connection to the db
    return user

def add_users_function(email, password):
    conn = sqlite3.connect('database_file') # Connect to the sqlite db
    cursor = conn.cursor() # Creating a cursors
    cursor.execute("SELECT * FROM USERS WHERE USER_EMAIL = ? AND USERS_PASSWORD = ?", (email, password)) # SQL request with the execute method to search any users in the db with the same id than the ones put by the users in the html page
    user = cursor.fetchone() # Stocking the one corresponding in user
    if user: # See if one exist if yes than close te connection and return a string if no execute the else
        conn.close()
        return "There are already a account with those id !"
    else:
        try:
            cursor.execute("INSERT INTO USERS (USER_EMAIL, USERS_PASSWORD) VALUES (?, ?)", (email, password)) # SQL request to insert the new user in USERS table
            conn.commit() # Confirm the changes in the sqlite db
            conn.close() # Close the connection
            return "User succesfully added !"
        except sqlite3.OperationalError as e:
            conn.close() # Close the connection if the try doesnt succeed 
            print("Failed to create the user: ", e) # Print the error

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
    
@app.route('/create_account', methods=['POST']) # Declaring a route for each POST methods sent to /create_account
def register():
    email = request.form.get('email') # Variable that contains the value put by the user inside the email input (form = ImmutableMultiDict = dict ; get = method of form)
    password = request.form.get('password')

    if not email or not password: # Check if one of them are empty if yes 400 http error
        return "One of the input are empty", 400
    
    if add_users_function(email, password): # Check if add_users_function is true (the new users has been added) than success if false (the new users has not been added) than 401 http error 
        return "Successful !"
    else:
        return "Error", 401

if __name__ == '__main__':  # if we execute the app.py file than the debug mode is activated if imported than the debugger is off
    app.run(debug=True)