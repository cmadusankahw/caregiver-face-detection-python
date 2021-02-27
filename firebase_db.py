import os
import time
from PyQt5.QtWidgets import *

from model.ElderTModel import *
from firebase_auth import *
from resources.constants.commonConstants import *
from resources.constants.uriConstants import *

db = firebase.database()
storage = firebase.storage()
db.child(dbElders)

# FaceData Storage Methods ##################################################################
def storeXML(filename):
    time.sleep(2)
    try:
        storage.child(dataDir + filename).put(os.path.abspath(classifierDir + filename))
        print("successfully uploaded xml to FireStore ...")
        return success
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)[errorString][messageString]
        if error:
            print(error)
        return error


def retrieveXML(filename):
    try:
        storage.child(dataDir + filename).download(filename)
        print("successfully downloaded trained data file ...")
        return success
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)[errorString][messageString]
        if error:
            print(error)
        return error


def getXMLURL(filename):
    try:
        storage.child(dataDir + filename).get_url()
        return success
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)[errorString][messageString]
        if error:
            print(error)
        return error


# Elders Database Methods ###################################################################

def getSingleElder(id):
    try:
        elder = db.child(dbElders).child(id).get()
        print('successfully retrieved elders')
        print(elder.val())
        return elder.val()
    except requests.HTTPError as error:
        if error:
            print(error)
        return failed

getSingleElder("chiran")

def getElders():
    try:
        elders = db.child(dbElders).get()
        print('successfully retrieved elders')
        eldersList = []
        if elders.val() is not None:
            for elder in elders.each():
                tablets_string = ''
                for e in elder.val()[tabletsStr]:
                    tablets_string += str(e[quantityStr]) + ' ' + e[tabletStr] + ' tablets at ' + e[timeToTakeStr] + ', '
                eldersList.append([elder.key(),
                                   elder.val()[nameStr],
                                   elder.val()[ageStr],
                                   tablets_string])
            print(eldersList)
            return eldersList
        else:
            return []
    except requests.HTTPError as error:
        if error:
            print(error)
        return []



def getElderNames():
    try:
        elders = db.child(dbElders).get()
        print('successfully retrieved elder names')
        eldersList = []
        if elders.val() is not None:
            for elder in elders.each():
                eldersList.append(elder.key())
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
        elder = db.child(dbElders).child(id).get()
        print('successfully retrieved the elder')
        print(elder.val())
        if elder.val() is None:
            return failed
        else:
            return elder.val()
    except requests.HTTPError as error:
        if error:
            print(error)
        return failed


def addElder(elder):
    try:
        db.child(dbElders).child(elder[idStr]).set({
            idStr: elder[idStr],
            nameStr: elder[nameStr],
            ageStr: elder[ageStr],
            genderStr: elder[genderStr],
            dobStr: elder[dobStr],
            tabletsStr: elder[tabletsStr]
        })
        print('successfully added an elder')
        return success
    except requests.HTTPError as error:
        if error:
            print(error)
        return failed


def updateElder(elder):
    try:
        db.child(dbElders).child(elder[idStr]).update({
            nameStr: elder[nameStr],
            ageStr: elder[ageStr],
            tabletsStr: elder[tabletsStr]
        })
        print('successfully updated the elder')
        return success
    except requests.HTTPError as error:
        if error:
            print(error)
        return failed


def removeElder(id):
    try:
        db.child(dbElders).child(id).remove()
        print('successfully removed the elder')
        return success
    except requests.HTTPError as error:
        if error:
            print(error)
        return failed


def appendElderList(tabledata, header=headerData):
    elderTable = QTableView()
    elderTable.setModel(ElderTableModel(tabledata, header))
    elderTable.model().layoutChanged.emit()
    print('successfully setup elders table data')
    return elderTable
