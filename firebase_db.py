import os
import time
from PyQt5.QtWidgets import *

from model.ElderTModel import *
from firebase_auth import *

db = firebase.database()
storage = firebase.storage()
db.child("elders")

# FaceData Storage Methods ##################################################################
def storeXML(filename):
    time.sleep(2)
    try:
        storage.child("data/" + filename).put(os.path.abspath("data/classifiers/" + filename))
        print("successfully uploaded xml to FireStore ...")
        return "success"
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error:
            print(error)
        return error


def retrieveXML(filename):
    try:
        storage.child("data/" + filename).download(filename)
        print("successfully downloaded trained data file ...")
        return "success"
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error:
            print(error)
        return error


def getXMLURL(filename):
    try:
        storage.child("data/" + filename).get_url()
        return "success"
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error:
            print(error)
        return error


# Elders Database Methods ###################################################################

def getSingleElder(id):
    try:
        elder = db.child("elders").child(id).get()
        print('successfully retrieved elders')
        print(elder.val())
        return elder.val()
    except requests.HTTPError as error:
        if error:
            print(error)
        return "failed"

getSingleElder("chiran")

def getElders():
    try:
        elders = db.child("elders").get()
        print('successfully retrieved elders')
        eldersList = []
        if elders.val() is not None:
            for elder in elders.each():
                eldersList.append([elder.key(),
                                   elder.val()["name"],
                                   elder.val()["age"],
                                   elder.val()["tablets"],
                                   elder.val()["quantity"],
                                   elder.val()["timeToTake"]])
            print(eldersList)
            return eldersList
        else:
            return []
    except requests.HTTPError as error:
        if error:
            print(error)
        return []


def getElder(id):
    try:
        elder = db.child("elders").child(id).get()
        print('successfully retrieved the elder')
        print(elder.val())
        if elder.val() is None:
            return "failed"
        else:
            return elder.val()
    except requests.HTTPError as error:
        if error:
            print(error)
        return "failed"


def addElder(elder):
    try:
        db.child("elders").child(elder["id"]).set({
            "id": elder["id"],
            "name": elder["name"],
            "age": elder["age"],
            "gender": elder["gender"],
            "dob": elder["dob"],
            "tablets": elder["tablets"],
            "quantity": elder["quantity"],
            "timeToTake": elder["timeToTake"]
        })
        print('successfully added an elder')
        return "success"
    except requests.HTTPError as error:
        if error:
            print(error)
        return "failed"

# addElder({
#     "id": "kamal",
#     "name": "Kamal M",
#     "age": 24,
#     "gender": "Male",
#     "dob": "1995-4-6",
#     "tablets": "panadol",
#     "quantity": 2,
#     "timeToTake": "11:00"
# })

def updateElder(elder):
    try:
        db.child("elders").child(elder["id"]).update({
            "name": elder["name"],
            "age": elder["age"],
            "tablets": elder["tablets"],
            "quantity": elder["quantity"],
            "timeToTake": elder["timeToTake"]
        })
        print('successfully updated the elder')
        return "success"
    except requests.HTTPError as error:
        if error:
            print(error)
        return "failed"


def removeElder(id):
    try:
        db.child("elders").child(id).remove()
        print('successfully removed the elder')
        return "success"
    except requests.HTTPError as error:
        if error:
            print(error)
        return "failed"

def appendElderList(tabledata, header=headerData):
    elderTable = QTableView()
    elderTable.setModel(ElderTableModel(tabledata, header))
    elderTable.model().layoutChanged.emit()
    print('successfully setup elders table data')
    return elderTable
