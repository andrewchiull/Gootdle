from PyQt5.QtCore import QObject
from PyQt5 import QtCore, QtGui
import numpy as np
import cv2
import time
from Color.Color import ColorDetection
class Camera(QObject):


    picdone = QtCore.pyqtSignal(np.ndarray)
    fail = QtCore.pyqtSignal(bool)
    is_paused = False
    def img2pyqt(self,img,label):
        '''
        convert the opencv format to pyqt format color
        '''
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        temp = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1]*3, QtGui.QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(temp).scaled(label.width(), label.height())

    def run(self):

        self.vid = cv2.VideoCapture(0)

        while True:
            if self.is_paused:
                ret, frame = self.vid.read()
                frame = cv2.rotate(frame, cv2.ROTATE_180)
                cd = ColorDetection(img=frame, detect=40, resize=50)
                cd.main()
                self.is_paused = False
                continue
            ret, frame = self.vid.read()
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            # time.sleep(1/20)
            if ret:
                self.screen.setPixmap(self.img2pyqt(frame,self.screen))
            else:
                self.fail.emit(False)
                break
