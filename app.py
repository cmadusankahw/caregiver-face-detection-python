from PyQt5 import QtWidgets, uic, QtCore
import sys
from PyQt5.QtGui import *
from create_classifier import *
from create_dataset import *
from firebase_auth import *
from firebase_db import *
from ElderTModel import *

def center(self):
    frameGm = self.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    self.move(frameGm.topLeft())


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        uic.loadUi('gui/home.ui', self)

        # Find the button
        self.addNew = self.findChild(QtWidgets.QPushButton, 'addNewButton')
        self.addNew.clicked.connect(self.showAddNewUi)

        # Find the button
        self.detectElder = self.findChild(QtWidgets.QPushButton, 'detectButton')
        self.detectElder.clicked.connect(self.showDetectElderUi)

        # find exit menu item
        self.exitMenu = self.findChild(QtWidgets.QAction, "actionExit")
        self.exitMenu.triggered.connect(self.exitApp)

        # set the table model
        self.elderTableWidget = appendElderList() #getElders()
        self.elderTableWidget.resize(1230, 260)
        self.elderTableWidget.move(40,470)
        header = self.elderTableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.layout().addWidget(self.elderTableWidget)

        self.centerWindow()

    def exitApp(self):
        self.destroy()

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
        uic.loadUi('gui/addElder.ui', self)

        # setting gender selection combo box
        self.elderGender = self.findChild(QtWidgets.QComboBox, "elderGender")
        self.elderGender.addItems(["Male", "Female"])

        self.addElderBtn = self.findChild(QtWidgets.QPushButton, 'addNewButton')
        self.addElderBtn.clicked.connect(self.addElderFunc)

        self.updateElderBtn = self.findChild(QtWidgets.QPushButton, 'updateButton')
        self.updateElderBtn.clicked.connect(self.updateElderFunc)

        self.removeElderBtn = self.findChild(QtWidgets.QPushButton, 'removeButton')
        self.removeElderBtn.clicked.connect(self.removeElderFunc)

        self.removeElderBtn = self.findChild(QtWidgets.QPushButton, 'resetButton')
        self.removeElderBtn.clicked.connect(self.resetUpdateFields)

        self.findElderBtn = self.findChild(QtWidgets.QPushButton, 'findButton')
        self.findElderBtn.clicked.connect(self.searchElderFunc)

        self.openCamBtn = self.findChild(QtWidgets.QPushButton, 'camButton')
        self.openCamBtn.clicked.connect(self.trainFace)

        # find the text inputs
        self.elderId = self.findChild(QtWidgets.QLineEdit, "elderId")
        self.elderName = self.findChild(QtWidgets.QLineEdit, "elderName")
        self.elderAge = self.findChild(QtWidgets.QSpinBox, "elderAge")
        self.elderDOB = self.findChild(QtWidgets.QDateEdit, "elderDOB")
        self.elderTablets = self.findChild(QtWidgets.QLineEdit, "elderTablets")
        self.tabletQty = self.findChild(QtWidgets.QSpinBox, "tabletQty")
        self.tabletTimeToTake = self.findChild(QtWidgets.QTimeEdit, "tabletTimeToTake")
        self.infoLabel = self.findChild(QtWidgets.QLabel, "infoLabel")
        self.elderImg = self.findChild(QtWidgets.QLabel, "elderImg")

        # find update inputs
        self.updateElderId = self.findChild(QtWidgets.QLineEdit, "uelderId")
        self.updateElderName = self.findChild(QtWidgets.QLineEdit, "uelderName")
        self.updateElderAge = self.findChild(QtWidgets.QSpinBox, "uelderAge")
        self.updateElderTablets = self.findChild(QtWidgets.QLineEdit, "uelderTablets")
        self.updateTabletQty = self.findChild(QtWidgets.QSpinBox, "utabletQty")
        self.updateTabletTimeToTake = self.findChild(QtWidgets.QTimeEdit, "utabletTimeToTake")
        self.updateInfoLabel = self.findChild(QtWidgets.QLabel, "uinfoLabel")
        self.updateElderImg = self.findChild(QtWidgets.QLabel, "uelderImg")

        self.centerWindow()

    def centerWindow(self):
        center(self)

    def addElderFunc(self):
        # ToDo Run Image Capture and Detector passing elderId as dirname
        self.infoLabel.setProperty("text", "Face Data Uploading.. Please Wait..")
        elder = {
            "id": str(self.elderId.text()),
            "name": str(self.elderName.text()),
            "age": int(self.elderAge.value()),
            "gender": str(self.elderGender.currentText()),
            "dob": str(self.elderDOB.date().toPyDate()),
            "tablets": str(self.elderTablets.text()),
            "quantity": int(self.tabletQty.value()),
            "timeToTake": str(self.tabletTimeToTake.time().hour()) + ":" + str(self.tabletTimeToTake.time().minute())
        }
        # self.storeXMLFile(self.elderId.text() + "_classifier.xml")
        self.infoLabel.setProperty("text", "Elder Record creating.. Please Wait..")
        response = addElder(elder)
        if response == "success":
            self.infoLabel.setProperty("text", "Elder added Successfully!")
            self.resetFields()

    def updateElderFunc(self):
        elder = {
            "id": str(self.updateElderId.text()),
            "name": str(self.updateElderName.text()),
            "age": int(self.updateElderAge.value()),
            "tablets": str(self.updateElderTablets.text()),
            "quantity": int(self.updateTabletQty.value()),
            "timeToTake": str(self.updateTabletTimeToTake.time().hour()) + ":" + str(self.updateTabletTimeToTake.time().minute())
        }
        response = updateElder(elder)
        if response == "success":
            self.resetUpdateFields()
            self.updateInfoLabel.setProperty("text", "Elder details Updated Successfully!")
        else:
            self.updateInfoLabel.setProperty("text", "Error Occurred while Updating. Please Retry!")

    def removeElderFunc(self):
        removed = removeElder(str(self.updateElderId.text()))
        if removed == "success":
            self.destroy()
        else:
            self.updateInfoLabel.setProperty("text", "Error Removing! Please Retry!")


    def searchElderFunc(self):
        elder = getElder(str(self.updateElderId.text()))
        if elder != "failed":
            self.updateElderName.setProperty("text", str(elder["name"]))
            self.updateElderAge.setProperty("value", int(elder["age"]))
            self.updateElderTablets.setProperty("text", str(elder["tablets"]))
            self.updateTabletQty.setProperty("value", int(elder["quantity"]))
            recievedTime = QtCore.QTime(int(str(elder["timeToTake"]).split(":")[0]), int(str(elder["timeToTake"]).split(":")[1]))
            self.updateTabletTimeToTake.setProperty("time", recievedTime)
            pixmap = QPixmap("data/" + elder["id"] + "/100" + elder["id"] + ".jpg")
            self.uelderImg.setPixmap(pixmap)
        else:
            self.updateInfoLabel.setProperty("text", "No Elder Found with given ID!")

    def trainFace(self):
        # ToDo open Face Trainer code
        self.addElderBtn.setProperty("enabled", True)


    def storeXMLFile(self, filename):
        storeResponse = storeXML(filename)
        print(storeResponse)

    def resetFields(self):
        self.elderName.setProperty("text", "")
        self.elderAge.setProperty("value", 0)
        self.elderTablets.setProperty("text", "")
        self.tabletQty.setProperty("value", 0)
        resetTime = QtCore.QTime(0, 0)
        resetDOB = QtCore.QDate(2000,1,1)
        self.tabletTimeToTake.setProperty("time", resetTime)
        self.elderDOB.setProperty("date", resetDOB)

    def resetUpdateFields(self):
        self.updateElderName.setProperty("text", "")
        self.updateElderAge.setProperty("value", 0)
        self.updateElderTablets.setProperty("text", "")
        self.updateTabletQty.setProperty("value", 0)
        resetTime = QtCore.QTime(0, 0)
        self.updateTabletTimeToTake.setProperty("time", resetTime)

    def exitRegister(self):
        self.destroy()

    # ToDo to Edit
    # def capimg(self):
    #     self.numimglabel.config(text=str("Captured Images = 0 "))
    #     # messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
    #     x = start_capture(self.controller.active_name)
    #     self.controller.num_of_images = x
    #     self.numimglabel.config(text=str("Number of images captured = " + str(x)))

    # ToDo to edit
    # def trainmodel(self):
    #     if self.controller.num_of_images < 300:
    #         # messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
    #         return
    #     train_classifer(self.controller.active_name)
    #     # messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
    #     self.controller.show_frame("PageFour")


# Detect an Elder with trained face recognition data ##########################################
class DetectElderUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(DetectElderUi, self).__init__()
        uic.loadUi('gui/detectElder.ui', self)

        # Find the Face detector button
        self.detectFace = self.findChild(QtWidgets.QPushButton, 'detectButton')
        self.detectFace.clicked.connect(self.detectElder)

        # find the window exit button
        self.exitWindow = self.findChild(QtWidgets.QPushButton, 'exitButton')
        self.exitWindow.clicked.connect(self.exitDetector)

        # find the image
        self.elderImg = self.findChild(QtWidgets.QLabel, "elderImg")

        # find the text inputs
        self.elderId = self.findChild(QtWidgets.QLabel, "elderId")
        self.elderName = self.findChild(QtWidgets.QLabel, "elderName")
        self.elderAge = self.findChild(QtWidgets.QLabel, "elderAge")
        self.elderGender = self.findChild(QtWidgets.QLabel, "elderGender")
        self.elderDOB = self.findChild(QtWidgets.QLabel, "elderName")
        self.elderTablets = self.findChild(QtWidgets.QLabel, "elderTablets")
        self.tabletQty = self.findChild(QtWidgets.QLabel, "tabletQty")
        self.tabletTimeToTake = self.findChild(QtWidgets.QLabel, "tabletTimeToTake")

        self.centerWindow()

    def centerWindow(self):
        center(self)

    def detectElder(self):
        print("running face recognition cam window")

        # ToDo detector will return elder_name so elder data can be retrieved
        # ToDo pass returned elder ID here

        elder = getElder("chiran")

        if elder != "failed":
            pixmap = QPixmap("data/"+elder["id"] + "/100"+elder["id"]+".jpg")
            self.elderImg.setPixmap(pixmap)
            self.elderId.setProperty("text", elder["id"])
            self.elderName.setProperty("text", elder["name"])
            self.elderAge.setProperty("text", elder["age"])
            self.elderDOB.setProperty("text", elder["dob"])
            self.elderTablets.setProperty("text", elder["tablets"])
            self.tabletQty.setProperty("text", elder["quantity"])
            self.tabletTimeToTake.setProperty("text", elder["timeToTake"])


    def exitDetector(self):
        self.destroy()


# Login and Signup - CareGiver ################################################################
class SignUpUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignUpUi, self).__init__()
        uic.loadUi('gui/signup.ui', self)

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
        # self.show()

    def centerWindow(self):
        center(self)

    def signupUser(self):
        result = signUp(self.emailInput.text(), self.passwordInput.text())
        if result == "success":
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
        uic.loadUi('gui/login.ui', self)

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
        if result == "success":
            LoginUi.hide(self)
            self.home = MainUi()
            self.home.showFullScreen()
        else:
            self.hint.setProperty("text", result)

    def showSignUpUi(self):
        LoginUi.hide(self)
        self.signup = SignUpUi()
        self.signup.show()


app = QtWidgets.QApplication(sys.argv)
window = LoginUi()
sys.exit(app.exec_())
