from PyQt5 import QtWidgets, uic
import sys


class LoginUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginUi, self).__init__()
        uic.loadUi('login.ui', self)

        # Find the button
        self.button = self.findChild(QtWidgets.QPushButton, 'loginButton')

        # Remember to pass the definition/method, not the return value!
        self.button.clicked.connect(self.loginUser)

        self.center()
        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def loginUser(self):
        # This is executed when the button is pressed
        print('logged in')


app = QtWidgets.QApplication(sys.argv)
window = LoginUi()
sys.exit(app.exec_())
