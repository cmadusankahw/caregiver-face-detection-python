import json
import os
import requests
from PyQt5.QtWidgets import *

from ElderTModel import *
from firebase_auth import firebase

db = firebase.database()
storage = firebase.storage()


# FaceData Storage Methods ##################################################################
def storeXML(filename):
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

# ToDo
# Elders Database Methods ###################################################################
def getElder(id):
    try:
        print('successfully retrieved elder')
        return {
            "id": id,
            "name": "Chiran",
            "age": 24,
            "gender": "Male",
            "dob": "1996-7-8",
            "tablets": "panadol",
            "quantity": 2,
            "timeToTake": "12.30"
        }
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        if error:
            print(error)
        return "failed"


def getElders():
    print('successfully retrieved elders')
    return [[1234567890, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20]]  # temp


def addElder(elder):
    print('successfully added an elder')


def updateElder(elder):
    print('successfully updated the elder')


def removeElder(id):
    print('successfully removed elder')


def appendElderList(tabledata=tableData, header=headerData):
    elderTable = QTableView()
    elderTable.setModel(ElderTableModel(tabledata, header))
    elderTable.model().layoutChanged.emit()
    print('successfully setup elders table data')
    return elderTable
