import json

import pyrebase
import requests

from resources.configs.firebaseConfigs import fbConfig
from resources.constants.commonConstants import *

firebaseConfig = fbConfig

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

# signup
def signUp(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        print("successfully created new careGiver Profile ...")
        return success
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)[errorString][messageString]
        if error == "INVALID_PASSWORD" | error == "INVALID_EMAIL":
            print("Invalid Username or Password")
        else :
            print("Error Occurred: Error Code(" + error + ")")
        return error


# signin
def signIn(email, password):
    try:
        global user
        user = auth.sign_in_with_email_and_password(email, password)
        print(email + " successfully logged in ...")
        return success
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)[errorString][messageString]
        if error:
            print("And Error Occurred: Error Code(" + error + ")")
        return error

