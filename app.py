from PyQt5 import QtWidgets, uic
import sys

from firebase_auth import *

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        uic.loadUi('home.ui', self)

        # Find the button
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')

        # Remember to pass the definition/method, not the return value!
        self.button.clicked.connect(self.printButtonPressed)

        self.center()
        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def printButtonPressed(self):
        # This is executed when the button is pressed
        print('printButtonPressed')

class LoginUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginUi, self).__init__()
        uic.loadUi('login.ui', self)

        # Find the login button
        self.loginButton = self.findChild(QtWidgets.QPushButton, 'loginButton')
        self.loginButton.clicked.connect(self.loginUser)

        # Find the signUp button
        self.signButton = self.findChild(QtWidgets.QPushButton, 'signupButton')
        self.signButton.clicked.connect(self.signupUser)

        # email, password inputs
        self.emailInput = self.findChild(QtWidgets.QLineEdit, 'emailInput')
        self.passwordInput = self.findChild(QtWidgets.QLineEdit, 'passwordInput')


        self.center()
        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def loginUser(self):
        result = signIn(self.emailInput.text(), self.passwordInput.text())
        if result == "success":
            LoginUi.hide(self)
            self.home = MainUi()
            self.home.show()

    def signupUser(self):
        signUp(self.emailInput.text(), self.passwordInput.text())


app = QtWidgets.QApplication(sys.argv)
window = LoginUi()
sys.exit(app.exec_())
