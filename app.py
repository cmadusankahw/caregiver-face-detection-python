from PyQt5 import QtWidgets, uic
import sys

from create_classifier import *
from create_dataset import *
from firebase_auth import *


def center(self):
    frameGm = self.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    self.move(frameGm.topLeft())


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        uic.loadUi('home.ui', self)

        # Find the button
        self.addNew = self.findChild(QtWidgets.QPushButton, 'addNewButton')
        self.addNew.clicked.connect(self.showAddNewUi)

        self.centerWindow()

    def centerWindow(self):
        center(self)

    def showLoginUi(self):
        self.registerElder = RegisterElderUi()
        self.registerElder.show()


# Add New Elder with Face Data Training ######################################################

class RegisterElderUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterElderUi, self).__init__()
        uic.loadUi('addElder.ui', self)

        # Find the button
        self.addElder = self.findChild(QtWidgets.QPushButton, 'addNewButton')
        self.addElder.clicked.connect(self.addNewElder)

        self.centerWindow()

    def centerWindow(self):
        center(self)

    def addNewElder(self):
        # add new elder
        print('add new elder')

    # ToDo to Edit
    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        # messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = " + str(x)))

    # ToDo to edit
    def trainmodel(self):
        if self.controller.num_of_images < 300:
            # messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        # messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.show_frame("PageFour")


# Login and Signup - CareGiver ################################################################

class SignUpUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignUpUi, self).__init__()
        uic.loadUi('signup.ui', self)

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
        uic.loadUi('login.ui', self)

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
