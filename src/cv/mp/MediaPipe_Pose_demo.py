import cv2
import mediapipe as mp
import numpy as np


import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from src.cv.mp.pose import PoseDetection

from settings import S

# DEBUG = S.DEBUG
DEBUG = True

mp_pose = mp.solutions.pose
if DEBUG:
  mp_drawing = mp.solutions.drawing_utils
  mp_drawing_styles = mp.solutions.drawing_styles

# For webcam input:
cap = WebcamVideoStream(src=S.VIDEO_SOURCE).start()
# cap = WebcamVideoStream(src=S.VIDEO_SOURCE).start()
fps = FPS().start()
pose = PoseDetection().start()
while cap.grabbed:
  fps.update()

  image = cap.read()

  # image = cv2.resize(image, None, fx=0.2, fy=0.2) # Reduce the size
  # image = imutils.resize(image, width=800)

  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  image.flags.writeable = False
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
  pose.read_image(image)
  results = pose.process()

  if not DEBUG: continue

  # Draw the pose annotation on the image.
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  mp_drawing.draw_landmarks(
      image,
      results.pose_landmarks,
      mp_pose.POSE_CONNECTIONS,
      landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
  # Flip the image horizontally for a selfie-view display.
  cv2.imshow('MediaPipe Pose',
              image
            #  cv2.flip(image, 1) # DONT Flip
              )

  if cv2.waitKey(5) & 0xFF == 27:
    break

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
cap.stop()