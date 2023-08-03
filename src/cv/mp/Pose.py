# import the necessary packages
from threading import Thread
import numpy as np
import cv2
import mediapipe as mp


import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose




class PoseDetection:

    def __init__(self, name="WebcamVideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream

        self.pose = mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        
        
        H, W = 1, 1
        self.image = np.ndarray((H, W, 3), np.uint8) # empty image
        self.result = self.pose.process(self.image)

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            self.result = self.pose.process(self.image)

    def read_image(self, image):
        self.image = image

    def process(self):
        # return the frame most recently read
        return self.result

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
