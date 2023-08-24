# [Pose landmark detection guide for Python  |  MediaPipe  |  Google for Developers](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python?authuser=2#live-stream)
# [How to implement gesture\_recognizer.task for Live stream · Issue #4448 · google/mediapipe](https://github.com/google/mediapipe/issues/4448#issuecomment-1562674509)

from settings import S, create_logger
log = create_logger(__file__, "DEBUG")

import datetime
import cv2
import numpy as np

from imutils.video import WebcamVideoStream
from imutils.video import FPS

import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarker, PoseLandmarkerOptions, PoseLandmarkerResult
BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
        annotated_image,
        pose_landmarks_proto,
        solutions.pose.POSE_CONNECTIONS,
        solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image

class Output():
    detection_result: PoseLandmarkerResult = None
    image: mp.Image = None
    timestamp_ms: int = None

output = Output()

# Create a pose landmarker instance with the live stream mode:
def print_result(detection_result: PoseLandmarkerResult, image: mp.Image, timestamp_ms: int):
    output.detection_result = detection_result
    output.image = image
    output.timestamp_ms = timestamp_ms

def create_detector(model_path: str):
    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)
    return PoseLandmarker.create_from_options(options)

class Detector(): # TODO clean up
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    # cap = WebcamVideoStream(src=S.VIDEO_SOURCE).start()
    cap = WebcamVideoStream(src=0).start()
    fps = FPS().start()
    starttime = datetime.datetime.now()
    MODEL_PATH = S.ROOT / "src/cv/mp" / "pose_landmarker_lite.task"
    with create_detector(MODEL_PATH) as detector:
        # The landmarker is initialized. Use it here.

        while cap.grabbed:
            fps.update()
            frame = cap.read()
            timestamp_ms = (datetime.datetime.now() - starttime) // datetime.timedelta(microseconds=1)


            # STEP 3: Load the input image.
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            
            # STEP 4: Detect pose landmarks from the input image.
            detector.detect_async(image, timestamp_ms)

            result = output.detection_result
            if result:
                # STEP 5: Process the detection result. In this case, visualize it.
                annotated_image = draw_landmarks_on_image(frame, result)
                cv2.imshow("img", cv2.flip(annotated_image, 1))


            if cv2.waitKey(5) & 0xFF == 27:
                break

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    cap.stop()