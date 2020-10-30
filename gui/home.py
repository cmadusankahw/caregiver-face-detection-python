from PyQt5 import QtWidgets, uic
import sys

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
        

app = QtWidgets.QApplication(sys.argv)
window = MainUi()
sys.exit(app.exec_())
