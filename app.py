from PyQt5 import QtWidgets, uic, QtCore
import sys
from PyQt5.QtGui import *

from create_classifier import train_classifer
from create_dataset import *
from detector import faceDetector
from firebase_db import *
from model.ElderTModel import *
from resources.constants.commonConstants import *
from resources.constants.uriConstants import *


def center(self):
    frameGm = self.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    self.move(frameGm.topLeft())


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        uic.loadUi(homeGUI, self)

        # Find add new button
        self.addNew = self.findChild(QtWidgets.QPushButton, 'addNewButton')
        self.addNew.clicked.connect(self.showAddNewUi)

        # Find careGive button
        self.detectElder = self.findChild(QtWidgets.QPushButton, 'detectButton')
        self.detectElder.clicked.connect(self.showDetectElderUi)

        self.refreshTable = self.findChild(QtWidgets.QPushButton, 'refreshButton')
        self.refreshTable.clicked.connect(self.refreshElderTable)

        # find exit menu item
        self.exitMenu = self.findChild(QtWidgets.QAction, "actionExit")
        self.exitMenu.triggered.connect(self.exitApp)

        # set the table model
        self.elderTableWidget = appendElderList(getElders())
        self.elderTableWidget.resize(1230, 260)
        self.elderTableWidget.move(40, 440)
        header = self.elderTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        custom_font = QFont()
        custom_font.setPointSize(12)
        custom_font.setBold(True)
        self.elderTableWidget.setFont(custom_font)
        self.layout().addWidget(self.elderTableWidget)

        self.elderCount = self.findChild(QtWidgets.QLCDNumber, "lcdNumber")

        self.mainImg = self.findChild(QtWidgets.QLabel, 'mainImg')
        pixmap = QPixmap(mainPNG)
        self.mainImg.setPixmap(pixmap)

        self.elderCount.setProperty("value", self.elderTableWidget.model().rowCount(self))

        self.centerWindow()

    def exitApp(self):
        self.destroy()

    def refreshElderTable(self):
        self.elderTableWidget.setModel(ElderTableModel(getElders(), headerData))
        self.elderTableWidget.model().layoutChanged.emit()

    def centerWindow(self):
        center(self)

    def showAddNewUi(self):
        self.registerElder = RegisterElderUi()
        self.registerElder.show()

    def showDetectElderUi(self):
        self.detectElder = DetectElderUi()
        self.detectElder.show()


# Add New Elder with Face Data Training ######################################################
class RegisterElderUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterElderUi, self).__init__()
        uic.loadUi(addElderGUI, self)

        # no of captured images
        self.x = 0

        # setting gender selection combo box
        self.elderGender = self.findChild(QtWidgets.QComboBox, "elderGender")
        self.elderGender.addItems([male, female])

        self.addElderBtn = self.findChild(QtWidgets.QPushButton, 'addNewButton')
        self.addElderBtn.clicked.connect(self.addElderFunc)

        self.updateElderBtn = self.findChild(QtWidgets.QPushButton, 'updateButton')
        self.updateElderBtn.clicked.connect(self.updateElderFunc)

        self.removeElderBtn = self.findChild(QtWidgets.QPushButton, 'removeButton')
        self.removeElderBtn.clicked.connect(self.removeElderFunc)

        self.resetElderBtn = self.findChild(QtWidgets.QPushButton, 'resetButton')
        self.resetElderBtn.clicked.connect(self.resetUpdateFields)

        self.findElderBtn = self.findChild(QtWidgets.QPushButton, 'findButton')
        self.findElderBtn.clicked.connect(self.searchElderFunc)

        self.openCamBtn = self.findChild(QtWidgets.QPushButton, 'camButton')
        self.openCamBtn.clicked.connect(self.trainFace)

        # find the text inputs
        self.elderId = self.findChild(QtWidgets.QLineEdit, "elderId")
        self.elderName = self.findChild(QtWidgets.QLineEdit, "elderName")
        self.elderAge = self.findChild(QtWidgets.QSpinBox, "elderAge")
        self.elderDOB = self.findChild(QtWidgets.QDateEdit, "elderDOB")
        self.elderImg = self.findChild(QtWidgets.QLabel, "elderImg")
        self.infoLabel = self.findChild(QtWidgets.QLabel, "infoLabel")

        # find tablet details
        self.tablet1Select = self.findChild(QtWidgets.QComboBox, "tablet1Select")
        self.tablet1Select.addItems(tablet_items)
        self.tablet1Select.currentTextChanged.connect(self.tablet1Enable)
        self.tablet1Qty = self.findChild(QtWidgets.QSpinBox, "tablet1Qty")
        self.tablet1TimeToTake = self.findChild(QtWidgets.QTimeEdit, "tablet1TimeToTake")

        self.tablet2Select = self.findChild(QtWidgets.QComboBox, "tablet2Select")
        self.tablet2Select.addItems(tablet_items)
        self.tablet2Select.currentTextChanged.connect(self.tablet2Enable)
        self.tablet2Qty = self.findChild(QtWidgets.QSpinBox, "tablet2Qty")
        self.tablet2TimeToTake = self.findChild(QtWidgets.QTimeEdit, "tablet2TimeToTake")

        self.tablet3Select = self.findChild(QtWidgets.QComboBox, "tablet3Select")
        self.tablet3Select.addItems(tablet_items)
        self.tablet3Select.currentTextChanged.connect(self.tablet3Enable)
        self.tablet3Qty = self.findChild(QtWidgets.QSpinBox, "tablet3Qty")
        self.tablet3TimeToTake = self.findChild(QtWidgets.QTimeEdit, "tablet3TimeToTake")

        self.tablet4Select = self.findChild(QtWidgets.QComboBox, "tablet4Select")
        self.tablet4Select.addItems(tablet_items)
        self.tablet4Select.currentTextChanged.connect(self.tablet4Enable)
        self.tablet4Qty = self.findChild(QtWidgets.QSpinBox, "tablet4Qty")
        self.tablet4TimeToTake = self.findChild(QtWidgets.QTimeEdit, "tablet4TimeToTake")

        # find update inputs
        self.updateElderId = self.findChild(QtWidgets.QLineEdit, "uelderId")
        self.updateElderName = self.findChild(QtWidgets.QLineEdit, "uelderName")
        self.updateElderAge = self.findChild(QtWidgets.QSpinBox, "uelderAge")
        self.updateInfoLabel = self.findChild(QtWidgets.QLabel, "uinfoLabel")
        self.updateElderImg = self.findChild(QtWidgets.QLabel, "uelderImg")

        # find table details update inputs
        self.updateTablet1Select = self.findChild(QtWidgets.QComboBox, "utablet1Select")
        self.updateTablet1Select.addItems(tablet_items)
        self.updateTablet1Select.currentTextChanged.connect(self.utablet1Enable)
        self.updateTablet1Qty = self.findChild(QtWidgets.QSpinBox, "utablet1Qty")
        self.updateTablet1TimeToTake = self.findChild(QtWidgets.QTimeEdit, "utablet1TimeToTake")

        self.updateTablet2Select = self.findChild(QtWidgets.QComboBox, "utablet2Select")
        self.updateTablet2Select.addItems(tablet_items)
        self.updateTablet2Select.currentTextChanged.connect(self.utablet2Enable)
        self.updateTablet2Qty = self.findChild(QtWidgets.QSpinBox, "utablet2Qty")
        self.updateTablet2TimeToTake = self.findChild(QtWidgets.QTimeEdit, "utablet2TimeToTake")

        self.updateTablet3Select = self.findChild(QtWidgets.QComboBox, "utablet3Select")
        self.updateTablet3Select.addItems(tablet_items)
        self.updateTablet3Select.currentTextChanged.connect(self.utablet3Enable)
        self.updateTablet3Qty = self.findChild(QtWidgets.QSpinBox, "utablet3Qty")
        self.updateTablet3TimeToTake = self.findChild(QtWidgets.QTimeEdit, "utablet3TimeToTake")

        self.updateTablet4Select = self.findChild(QtWidgets.QComboBox, "utablet4Select")
        self.updateTablet4Select.addItems(tablet_items)
        self.updateTablet4Select.currentTextChanged.connect(self.utablet4Enable)
        self.updateTablet4Qty = self.findChild(QtWidgets.QSpinBox, "utablet4Qty")
        self.updateTablet4TimeToTake = self.findChild(QtWidgets.QTimeEdit, "utablet4TimeToTake")

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle(messageBoxTitle)
        self.msg.setStandardButtons(QMessageBox.Ok)

        pixmap = QPixmap(imageHolderPNG)
        self.elderImg.setPixmap(pixmap)
        self.updateElderImg.setPixmap(pixmap)

        self.centerWindow()

    def tablet1Enable(self):
        if self.tablet1Select.currentText() != 'None':
            self.tablet1Qty.setProperty('enabled', True)
            self.tablet1TimeToTake.setProperty('enabled', True)
        else:
            self.tablet1Qty.setProperty('enabled', False)
            self.tablet1TimeToTake.setProperty('enabled', False)

    def tablet2Enable(self):
        if self.tablet2Select.currentText() != 'None':
            self.tablet2Qty.setProperty('enabled', True)
            self.tablet2TimeToTake.setProperty('enabled', True)
        else:
            self.tablet2Qty.setProperty('enabled', False)
            self.tablet2TimeToTake.setProperty('enabled', False)

    def tablet3Enable(self):
        if self.tablet3Select.currentText() != 'None':
            self.tablet3Qty.setProperty('enabled', True)
            self.tablet3TimeToTake.setProperty('enabled', True)
        else:
            self.tablet3Qty.setProperty('enabled', False)
            self.tablet3TimeToTake.setProperty('enabled', False)

    def tablet4Enable(self):
        if self.tablet4Select.currentText() != 'None':
            self.tablet4Qty.setProperty('enabled', True)
            self.tablet4TimeToTake.setProperty('enabled', True)
        else:
            self.tablet4Qty.setProperty('enabled', False)
            self.tablet4TimeToTake.setProperty('enabled', False)

    # elder details updating
    def utablet1Enable(self):
        if self.updateTablet1Select.currentText() != 'None':
            self.updateTablet1Qty.setProperty('enabled', True)
            self.updateTablet1TimeToTake.setProperty('enabled', True)
        else:
            self.updateTablet1Qty.setProperty('enabled', False)
            self.updateTablet1TimeToTake.setProperty('enabled', False)

    def utablet2Enable(self):
        if self.updateTablet2Select.currentText() != 'None':
            self.updateTablet2Qty.setProperty('enabled', True)
            self.updateTablet2TimeToTake.setProperty('enabled', True)
        else:
            self.updateTablet2Qty.setProperty('enabled', False)
            self.updateTablet2TimeToTake.setProperty('enabled', False)

    def utablet3Enable(self):
        if self.updateTablet3Select.currentText() != 'None':
            self.updateTablet3Qty.setProperty('enabled', True)
            self.updateTablet3TimeToTake.setProperty('enabled', True)
        else:
            self.updateTablet3Qty.setProperty('enabled', False)
            self.updateTablet3TimeToTake.setProperty('enabled', False)

    def utablet4Enable(self):
        if self.updateTablet4Select.currentText() != 'None':
            self.updateTablet4Qty.setProperty('enabled', True)
            self.updateTablet4TimeToTake.setProperty('enabled', True)
        else:
            self.updateTablet4Qty.setProperty('enabled', False)
            self.updateTablet4TimeToTake.setProperty('enabled', False)

    def centerWindow(self):
        center(self)

    def updateTime(self, t):
        if t < 10:
            updated_time = '0' + str(t)
        else:
            updated_time = str(t)
        return updated_time

    def getAddElderTablets(self):
        tablets = []
        if self.tablet1Select.currentText() != 'None':
            hour_time = self.updateTime(int(self.tablet1TimeToTake.time().hour()))
            min_time = self.updateTime(int(self.tablet1TimeToTake.time().minute()))

            tablets.append({
                tabletStr: str(self.tablet1Select.currentText()),
                quantityStr: int(self.tablet1Qty.value()),
                timeToTakeStr: hour_time + ":" + min_time
            })

        if self.tablet2Select.currentText() != 'None':
            hour_time = self.updateTime(int(self.tablet2TimeToTake.time().hour()))
            min_time = self.updateTime(int(self.tablet2TimeToTake.time().minute()))

            tablets.append({
                tabletStr: str(self.tablet2Select.currentText()),
                quantityStr: int(self.tablet2Qty.value()),
                timeToTakeStr: hour_time + ":" + min_time
            })

        if self.tablet3Select.currentText() != 'None':
            hour_time = self.updateTime(int(self.tablet3TimeToTake.time().hour()))
            min_time = self.updateTime(int(self.tablet3TimeToTake.time().minute()))

            tablets.append({
                tabletStr: str(self.tablet3Select.currentText()),
                quantityStr: int(self.tablet3Qty.value()),
                timeToTakeStr: hour_time + ":" + min_time
            })

        if self.tablet4Select.currentText() != 'None':
            hour_time = self.updateTime(int(self.tablet4TimeToTake.time().hour()))
            min_time = self.updateTime(int(self.tablet4TimeToTake.time().minute()))

            tablets.append({
                tabletStr: str(self.tablet4Select.currentText()),
                quantityStr: int(self.tablet4Qty.value()),
                timeToTakeStr: hour_time + ":" + min_time
            })
        return tablets

    def getUpdateElderTablets(self):
        tablets = []
        if self.updateTablet1Select.currentText() != 'None':
            hour_time = self.updateTime(int(self.updateTablet1TimeToTake.time().hour()))
            min_time = self.updateTime(int(self.updateTablet1TimeToTake.time().minute()))

            tablets.append({
                tabletStr: str(self.updateTablet1Select.currentText()),
                quantityStr: int(self.updateTablet1Qty.value()),
                timeToTakeStr: hour_time + ":" + min_time
            })

        if self.updateTablet2Select.currentText() != 'None':
            hour_time = self.updateTime(int(self.updateTablet2TimeToTake.time().hour()))
            min_time = self.updateTime(int(self.updateTablet2TimeToTake.time().minute()))

            tablets.append({
                tabletStr: str(self.updateTablet2Select.currentText()),
                quantityStr: int(self.updateTablet2Qty.value()),
                timeToTakeStr: hour_time + ":" + min_time
            })

        if self.updateTablet3Select.currentText() != 'None':
            hour_time = self.updateTime(int(self.updateTablet3TimeToTake.time().hour()))
            min_time = self.updateTime(int(self.updateTablet3TimeToTake.time().minute()))

            tablets.append({
                tabletStr: str(self.updateTablet3Select.currentText()),
                quantityStr: int(self.updateTablet3Qty.value()),
                timeToTakeStr: hour_time + ":" + min_time
            })

        if self.updateTablet4Select.currentText() != 'None':
            hour_time = self.updateTime(int(self.updateTablet4TimeToTake.time().hour()))
            min_time = self.updateTime(int(self.updateTablet4TimeToTake.time().minute()))

            tablets.append({
                tabletStr: str(self.updateTablet4Select.currentText()),
                quantityStr: int(self.updateTablet4Qty.value()),
                timeToTakeStr: hour_time + ":" + min_time
            })
        return tablets

    def addElderFunc(self):
        self.infoLabel.setProperty("text", "Face Data Uploading.. Please Wait..")
        self.msg.setText("Please wait while Image Data uploads to firebase...")
        self.msg.show()
        elder = {
            idStr: str(self.elderId.text()),
            nameStr: str(self.elderName.text()),
            ageStr: int(self.elderAge.value()),
            genderStr: str(self.elderGender.currentText()),
            dobStr: str(self.elderDOB.date().toPyDate()),
            tabletsStr: self.getAddElderTablets(),
        }

        """ @note: Uncomment below line to enable fireStore dataset upload """
        # self.storeXMLFile(self.elderId.text() + classifierPostfix)

        self.msg.hide()
        self.infoLabel.setProperty("text", "Elder Record creating.. Please Wait..")
        response = addElder(elder)
        if response == success:
            self.infoLabel.setProperty("text", "")
            self.msg.setText("Elder added Successfully!")
            self.msg.show()
            self.resetFields()

    def updateElderFunc(self):
        elder = {
            idStr: str(self.updateElderId.text()),
            nameStr: str(self.updateElderName.text()),
            ageStr: int(self.updateElderAge.value()),
            tabletsStr: self.getUpdateElderTablets(),
        }
        response = updateElder(elder)
        if response == success:
            self.resetUpdateFields()
            self.msg.setText("Elder updated Successfully!")
            self.msg.show()
        else:
            self.msg.setText("Error Occurred while Updating Elder Details. Please Retry!")
            self.msg.show()

    def removeElderFunc(self):
        removed = removeElder(str(self.updateElderId.text()))
        if removed == success:
            self.msg.setText("Elder Removed!")
            self.msg.show()
            self.resetUpdateFields()
        else:
            self.msg.setText("Error Removing Elder! Please Retry!")
            self.msg.show()

    def retriveElderTablets(self, elderTablets):
        if 0 < len(elderTablets):
            recievedTime1 = QtCore.QTime(int(str(elderTablets[0][timeToTakeStr]).split(":")[0]),
                                         int(str(elderTablets[0][timeToTakeStr]).split(":")[1]))
            self.updateTablet1Select.setCurrentText(elderTablets[0][tabletStr])
            self.updateTablet1TimeToTake.setProperty("time", recievedTime1)
            self.updateTablet1Qty.setProperty("value", elderTablets[0][quantityStr])

        if 1 < len(elderTablets):
            recievedTime2 = QtCore.QTime(int(str(elderTablets[1][timeToTakeStr]).split(":")[0]),
                                         int(str(elderTablets[1][timeToTakeStr]).split(":")[1]))
            self.updateTablet2Select.setCurrentText(elderTablets[1][tabletStr])
            self.updateTablet2TimeToTake.setProperty("time", recievedTime2)
            self.updateTablet2Qty.setProperty("value", elderTablets[1][quantityStr])

        if 2 < len(elderTablets):
            recievedTime3 = QtCore.QTime(int(str(elderTablets[2][timeToTakeStr]).split(":")[0]),
                                         int(str(elderTablets[2][timeToTakeStr]).split(":")[1]))
            self.updateTablet3Select.setCurrentText(elderTablets[2][tabletStr])
            self.updateTablet3TimeToTake.setProperty("time", recievedTime3)
            self.updateTablet3Qty.setProperty("value", elderTablets[2][quantityStr])

        if 3 < len(elderTablets):
            recievedTime4 = QtCore.QTime(int(str(elderTablets[3][timeToTakeStr]).split(":")[0]),
                                         int(str(elderTablets[3][timeToTakeStr]).split(":")[1]))
            self.updateTablet4Select.setCurrentText(elderTablets[3][tabletStr])
            self.updateTablet4TimeToTake.setProperty("time", recievedTime4)
            self.updateTablet4Qty.setProperty("value", elderTablets[3][quantityStr])

    def searchElderFunc(self):
        self.updateInfoLabel.setProperty("text", "")
        elder = getElder(str(self.updateElderId.text()))
        self.removeElderBtn.setProperty("enabled", True)
        self.updateElderBtn.setProperty("enabled", True)
        if elder != failed:
            self.updateElderName.setProperty("text", str(elder[nameStr]))
            self.updateElderAge.setProperty("value", int(elder[ageStr]))

            # update tablet details
            self.retriveElderTablets(elder[tabletsStr])

            pixmap = QPixmap(dataDir + elder[idStr] + image100 + elder[idStr] + jpgType)
            self.uelderImg.setPixmap(pixmap)
            self.updateInfoLabel.setProperty("text", "")
        else:
            self.msg.setText("No Elder Found with given ID!")
            self.msg.show()
            self.resetUpdateFields()

    def trainFace(self):
        self.infoLabel.setProperty("text", "")
        self.msg.setText("Image Capture will start now. Please do not terminate the capture.")
        self.msg.setWindowTitle(messageBoxTitle)
        retVal = self.msg.exec_()
        if retVal == QMessageBox.Ok:
            self.capimg()

    def storeXMLFile(self, filename):
        storeResponse = storeXML(filename)
        print(storeResponse)

    def resetFields(self):
        self.addElderBtn.setProperty("enabled", False)
        self.elderName.setProperty("text", "")
        self.elderAge.setProperty("value", 0)

        self.tablet1Select.setCurrentText("None")
        self.tablet2Select.setCurrentText("None")
        self.tablet3Select.setCurrentText("None")
        self.tablet4Select.setCurrentText("None")

        resetTime = QtCore.QTime(0, 0)
        self.tablet1TimeToTake.setProperty("time", resetTime)
        self.tablet1Qty.setProperty("value", 0)
        self.tablet2TimeToTake.setProperty("time", resetTime)
        self.tablet2Qty.setProperty("value", 0)
        self.tablet3TimeToTake.setProperty("time", resetTime)
        self.tablet3Qty.setProperty("value", 0)
        self.tablet4TimeToTake.setProperty("time", resetTime)
        self.tablet4Qty.setProperty("value", 0)

        self.updateInfoLabel.setProperty("text", "")
        pixmap = QPixmap(imageHolderPNG)
        self.updateElderImg.setPixmap(pixmap)

        resetDOB = QtCore.QDate(2000, 1, 1)
        self.elderDOB.setProperty("date", resetDOB)

    def resetUpdateFields(self):
        self.removeElderBtn.setProperty("enabled", False)
        self.updateElderBtn.setProperty("enabled", False)
        self.updateElderName.setProperty("text", "")
        self.updateElderAge.setProperty("value", 0)

        self.updateTablet1Select.setCurrentText("None")
        self.updateTablet2Select.setCurrentText("None")
        self.updateTablet3Select.setCurrentText("None")
        self.updateTablet4Select.setCurrentText("None")

        self.updateInfoLabel.setProperty("text", "")
        pixmap = QPixmap(imageHolderPNG)
        self.updateElderImg.setPixmap(pixmap)

        resetTime = QtCore.QTime(0, 0)
        self.updateTablet1TimeToTake.setProperty("time", resetTime)
        self.updateTablet1Qty.setProperty("value", 0)
        self.updateTablet2TimeToTake.setProperty("time", resetTime)
        self.updateTablet2Qty.setProperty("value", 0)
        self.updateTablet3TimeToTake.setProperty("time", resetTime)
        self.updateTablet3Qty.setProperty("value", 0)
        self.updateTablet4TimeToTake.setProperty("time", resetTime)
        self.updateTablet4Qty.setProperty("value", 0)

    def exitRegister(self):
        self.destroy()

    def capimg(self):
        self.x = start_capture(self.elderId.text())
        self.infoLabel.setProperty("text", str("Number of images captured = " + str(self.x)))
        self.msg.setText("Create the Classifier DataSet for captured Face?")
        self.msg.show()
        retVal = self.msg.exec_()
        if retVal == QMessageBox.Ok:
            self.addElderBtn.setProperty("enabled", True)
            self.trainmodel()

    def trainmodel(self):
        if self.x < 500:
            self.msg.setText("No of Captured Images aren't enough! Please retry!")
            self.msg.setWindowTitle(messageBoxTitle)
            self.msg.show()
            retVal = self.msg.exec_()
            if retVal == QMessageBox.Ok:
                return
        train_classifer(self.elderId.text())
        self.msg.setText("Face Data Extracting and Training Successful!")
        self.msg.setWindowTitle(messageBoxTitle)
        self.msg.show()
        self.infoLabel.setProperty("text", "")
        successVal = self.msg.exec_()
        if successVal == QMessageBox.Ok:
            return


# Detect an Elder with trained face recognition data ##########################################
class DetectElderUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(DetectElderUi, self).__init__()
        uic.loadUi(detectElderGUI, self)

        # Find the Face detector button
        self.detectFace = self.findChild(QtWidgets.QPushButton, 'detectButton')
        self.detectFace.clicked.connect(self.detectElder)

        # find the window exit button
        self.exitWindow = self.findChild(QtWidgets.QPushButton, 'exitButton')
        self.exitWindow.clicked.connect(self.exitDetector)

        # find the text inputs
        self.elderId = self.findChild(QtWidgets.QLabel, "elderId")
        self.elderName = self.findChild(QtWidgets.QLabel, "elderName")
        self.elderAge = self.findChild(QtWidgets.QLabel, "elderAge")
        self.elderGender = self.findChild(QtWidgets.QLabel, "elderGender")
        self.elderDOB = self.findChild(QtWidgets.QLabel, "elderDOB")

        self.tablet1Title = self.findChild(QtWidgets.QLabel, "tablet1Title")
        self.tablet1Qty = self.findChild(QtWidgets.QLabel, "tablet1Qty")
        self.tablet1TimeToTake = self.findChild(QtWidgets.QLabel, "tablet1TimeToTake")
        self.tablet2Title = self.findChild(QtWidgets.QLabel, "tablet2Title")
        self.tablet2Qty = self.findChild(QtWidgets.QLabel, "tablet2Qty")
        self.tablet2TimeToTake = self.findChild(QtWidgets.QLabel, "tablet2TimeToTake")
        self.tablet3Title = self.findChild(QtWidgets.QLabel, "tablet3Title")
        self.tablet3Qty = self.findChild(QtWidgets.QLabel, "tablet3Qty")
        self.tablet3TimeToTake = self.findChild(QtWidgets.QLabel, "tablet3TimeToTake")
        self.tablet4Title = self.findChild(QtWidgets.QLabel, "tablet4Title")
        self.tablet4Qty = self.findChild(QtWidgets.QLabel, "tablet4Qty")
        self.tablet4TimeToTake = self.findChild(QtWidgets.QLabel, "tablet4TimeToTake")

        self.elderImg = self.findChild(QtWidgets.QLabel, "elderImg")

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle(messageBoxTitle)
        self.msg.setStandardButtons(QMessageBox.Ok)

        pixmap = QPixmap(imageHolderPNG)
        self.elderImg.setPixmap(pixmap)

        self.detectElder()

        self.centerWindow()

    def centerWindow(self):
        center(self)

    def retriveTabletDetails(self, elderTablets):
        if 0 < len(elderTablets):
            self.tablet1Title.setProperty("text", elderTablets[0][tabletStr])
            self.tablet1TimeToTake.setProperty("text", elderTablets[0][timeToTakeStr])
            self.tablet1Qty.setProperty("text", elderTablets[0][quantityStr])

        if 1 < len(elderTablets):
            self.tablet2Title.setProperty("text", elderTablets[1][tabletStr])
            self.tablet2TimeToTake.setProperty("text", elderTablets[1][timeToTakeStr])
            self.tablet2Qty.setProperty("text", elderTablets[1][quantityStr])

        if 2 < len(elderTablets):
            self.tablet3Title.setProperty("text", elderTablets[2][tabletStr])
            self.tablet3TimeToTake.setProperty("text", elderTablets[2][timeToTakeStr])
            self.tablet3Qty.setProperty("text", elderTablets[2][quantityStr])

        if 3 < len(elderTablets):
            self.tablet4Title.setProperty("text", elderTablets[3][tabletStr])
            self.tablet4TimeToTake.setProperty("text", elderTablets[3][timeToTakeStr])
            self.tablet4Qty.setProperty("text", elderTablets[3][quantityStr])

    def detectElder(self):
        print("running face recognition cam window")
        try:
            detectedElderName = faceDetector(getElderNames())
        except:
            self.msg.setText(
                "Some Registered Elders' Datassets are missing! Cannot continue! Please check the Database")
            self.msg.show()
            return

        if detectedElderName == failed:
            self.msg.setText("No Elders found in System!")
            self.msg.show()
            return

        elder = getElder(detectedElderName)

        if elder != failed:
            pixmap = QPixmap(dataDir + elder[idStr] + image100 + elder[idStr] + jpgType)
            self.elderImg.setPixmap(pixmap)
            self.elderId.setProperty("text", elder[idStr])
            self.elderName.setProperty("text", elder[nameStr])
            self.elderAge.setProperty("text", elder[ageStr])
            self.elderGender.setProperty("text", elder[genderStr])
            self.elderDOB.setProperty("text", elder[dobStr])
            self.retriveTabletDetails(elder[tabletsStr])
            tablet_1 = ''
            tablet_2 = ''
            tablet_3 = ''
            if len(elder[tabletsStr]) > 2:
                tablet_1 = elder[tabletsStr][0]
                tablet_2 = elder[tabletsStr][1]
                tablet_3 = elder[tabletsStr][2]
            elif len(elder[tabletsStr]) == 2:
                tablet_1 = elder[tabletsStr][0]
                tablet_2 = elder[tabletsStr][1]
            elif len(elder[tabletsStr]) == 1:
                tablet_1 = elder[tabletsStr][0]

            new_elder = {
                idStr: elder[idStr],
                'tablet1': tablet_1,
                'tablet2': tablet_2,
                'tablet3': tablet_3
            }
            response = addElderToIot(new_elder)


    def exitDetector(self):
        self.destroy()


# Login and Signup - CareGiver ################################################################
class SignUpUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignUpUi, self).__init__()
        uic.loadUi(signupGUI, self)

        # Find the back to login button
        self.signupButton = self.findChild(QtWidgets.QPushButton, 'loginButton')
        self.signupButton.clicked.connect(self.showLoginUi)

        # Find the signUp button
        self.signButton = self.findChild(QtWidgets.QPushButton, 'signupButton')
        self.signButton.clicked.connect(self.signupUser)

        # email, password inputs
        self.emailInput = self.findChild(QtWidgets.QLineEdit, 'emailInput')
        self.passwordInput = self.findChild(QtWidgets.QLineEdit, 'passwordInput')

        # find hint
        self.hint = self.findChild(QtWidgets.QLabel, 'errorLabel')

        self.centerWindow()

    def centerWindow(self):
        center(self)

    def signupUser(self):
        result = signUp(self.emailInput.text(), self.passwordInput.text())
        if result == success:
            self.showLoginUi()
        else:
            self.hint.setProperty("text", result)

    def showLoginUi(self):
        SignUpUi.hide(self)
        self.login = LoginUi()
        self.login.show()


class LoginUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginUi, self).__init__()
        uic.loadUi(loginGUI, self)

        # Find the login button
        self.loginButton = self.findChild(QtWidgets.QPushButton, 'loginButton')
        self.loginButton.clicked.connect(self.loginUser)

        # Find the oen signUp UI button
        self.signButton = self.findChild(QtWidgets.QPushButton, 'signupButton')
        self.signButton.clicked.connect(self.showSignUpUi)

        # email, password inputs
        self.emailInput = self.findChild(QtWidgets.QLineEdit, 'emailInput')
        self.passwordInput = self.findChild(QtWidgets.QLineEdit, 'passwordInput')

        # find hint
        self.hint = self.findChild(QtWidgets.QLabel, 'errorLabel')

        self.centerWindow()
        self.show()

    def centerWindow(self):
        center(self)

    def loginUser(self):
        result = signIn(self.emailInput.text(), self.passwordInput.text())
        if result == success:
            LoginUi.hide(self)
            self.home = MainUi()
            self.home.show()
        else:
            self.hint.setProperty("text", result)

    def showSignUpUi(self):
        LoginUi.hide(self)
        self.signup = SignUpUi()
        self.signup.show()


app = QtWidgets.QApplication(sys.argv)
window = LoginUi()
sys.exit(app.exec_())
