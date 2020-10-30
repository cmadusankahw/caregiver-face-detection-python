import json
import os
import requests
from PyQt5.QtWidgets import *

from ElderModel import *
from firebase_auth import firebase

db = firebase.database()
storage = firebase.storage()


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

def appendElderList(tabledata = tableData, header=headerData):
    elderTable = QTableView()
    elderTable.setModel(ElderTableModel(tabledata, header))
    elderTable.model().layoutChanged.emit()
    print('successfully setup elders table data')
    return elderTable
