from ui_remoteCarApp import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QMainWindow
from camera import Camera
from serialControl import SerialControl

import sys
import cv2
import serial
import time
class remoteCar(QMainWindow, Ui_Form):
    def __init__(self,parent = None):
        QMainWindow.__init__(self, parent = parent)
        Ui_Form.__init__(self)
        self.setupUi(self)
        self.setFocus()
        self.startThread()
        self.setupButtons()
        # self.setupSerial()
        self.loggingMessages = ""

    def setupButtons(self):
        self.pushButton_right.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_D))
        self.pushButton_right.clicked.connect(self.right)

        self.pushButton_forward.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_W))
        self.pushButton_forward.clicked.connect(self.forward)

        self.pushButton_backward.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_S))
        self.pushButton_backward.clicked.connect(self.backward)

        self.pushButton_left.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A))
        self.pushButton_left.clicked.connect(self.left)

        self.pushButton_open.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Q))
        self.pushButton_open.clicked.connect(self.open)

        self.pushButton_close.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_E))
        self.pushButton_close.clicked.connect(self.close)

        self.pushButton_detectColor.clicked.connect(self.detectColor)


        self.lineEdit.installEventFilter(self)

        self.pushButton_sendCommand.clicked.connect(self.sendCommand)
        self.pushButton_sendCommand.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return))

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        # return super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_B:
            self.workerSerial.command = "stop"
        elif event.key() == QtCore.Qt.Key_P:
            self.workerSerial.command = "stepForward"
        elif event.key() == QtCore.Qt.Key_Semicolon:
            self.workerSerial.command = "stepBackward"





    def sendCommand(self):
        command = self.lineEdit.text()
        self.workerSerial.command = command
        self.setFocus()

    def detectColor(self):
        self.workerCamera.is_paused = True
        print("(Pause streaming to detect color.)")
        time.sleep(1)
        print("(Resume streaming.)")
        self.workerCamera.is_paused = False

    def open(self):
        self.workerSerial.command = "open"

    def close(self):
        self.workerSerial.command = "close"

    def forward(self):
        self.workerSerial.command = "forward"

    def backward(self):
        self.workerSerial.command = "backward"

    def left(self):
        self.workerSerial.command = "left"


    def right(self):
        self.workerSerial.command = "right"

    def failConnect(self, condition):
        if condition == False:
            bg = cv2.imread('bg.jpg')
            self.screen.setPixmap(self.workerCamera.img2pyqt(bg,self.screen))
            print('Failed to connect to Camera ....')


    def startThread(self):
        self.threadCamera = QtCore.QThread()
        self.workerCamera = Camera()
        self.workerCamera.moveToThread(self.threadCamera)

        self.threadCamera.started.connect(self.workerCamera.run)
        self.workerCamera.fail.connect(self.failConnect)
        self.workerCamera.screen = self.screen
        self.threadCamera.start()



        self.threadSerial = QtCore.QThread()
        self.workerSerial = SerialControl()
        self.workerSerial.moveToThread(self.threadSerial)
        self.threadSerial.started.connect(self.workerSerial.run)
        self.threadSerial.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = remoteCar()
    ui.show()
    sys.exit(app.exec_())

