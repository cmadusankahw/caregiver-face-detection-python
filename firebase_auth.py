import json

import pyrebase
import requests

firebaseConfig = {
    "apiKey": "AIzaSyCjZQ2fJPtXKW-nLI6cnnSbYro3C7S7uLc",
    "authDomain": "caregiver-face-detection.firebaseapp.com",
    "databaseURL": "https://caregiver-face-detection.firebaseio.com",
    "projectId": "caregiver-face-detection",
    "storageBucket": "caregiver-face-detection.appspot.com",
    "messagingSenderId": "467403437176",
    "appId": "1:467403437176:web:36aa18e8bb98d04cf7e98d",
    "measurementId": "G-GQWDH7J1H6"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()


# signup
def signUp(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        print(" successfully created new careGiver Profile ...")
        return "success"
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error:
            print(error)
        return error


# signin
def signIn(email, password):
    try:
        auth.sign_in_with_email_and_password(email, password)
        print(email + " successfully logged in ...")
        return "success"
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error:
            print(error)
        return error

