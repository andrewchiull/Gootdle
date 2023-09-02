# [Pose landmark detection guide for Python  |  MediaPipe  |  Google for Developers](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python?authuser=2#live-stream)
# [How to implement gesture\_recognizer.task for Live stream · Issue #4448 · google/mediapipe](https://github.com/google/mediapipe/issues/4448#issuecomment-1562674509)

from typing import Optional
from settings import S, create_logger
log = create_logger(__file__, S.LOG_LEVEL)

import datetime
import numpy as np
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarker, PoseLandmarkerOptions, PoseLandmarkerResult
BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode


class PoseDetectionForStream:
    class Output():
        detection_result: PoseLandmarkerResult = None
        image: mp.Image = None
        timestamp_ms: int = None

    def __init__(self, model_path) -> None:
        self.detector = self.create_detector(model_path)
        self.starttime = datetime.datetime.now()
        self.output = self.Output()

    def output_result(self, detection_result: PoseLandmarkerResult, image: mp.Image, timestamp_ms: int):
        self.output.detection_result = detection_result
        self.output.image = image
        self.output.timestamp_ms = timestamp_ms

    def create_detector(self,model_path: str):
        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.output_result,
            num_poses=2 # people
            )
        return PoseLandmarker.create_from_options(options)

    def detect(self, frame: np.ndarray) -> Optional[PoseLandmarkerResult]:
        timestamp_ms = (datetime.datetime.now() - self.starttime) // datetime.timedelta(microseconds=1)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.detector.detect_async(image, timestamp_ms)
        return self.output.detection_result

    @classmethod
    def draw_landmarks_on_image(self, rgb_image, detection_result):
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


if __name__ == "__main__":

    import cv2
    from imutils.video import WebcamVideoStream
    from imutils.video import FPS

    # cap = WebcamVideoStream(src=S.VIDEO_SOURCE).start()
    cap = WebcamVideoStream(src=0).start() # Source
    fps = FPS().start()
    MODEL_PATH = S.ROOT / "src/cv/mp/pose_landmarker_lite.task"
    pose = PoseDetectionForStream(MODEL_PATH)

    while cap.grabbed:
        fps.update()
        frame = cap.read()
        result = pose.detect(frame)
        if result:
            annotated_image = pose.draw_landmarks_on_image(frame, result)
            cv2.imshow("img", cv2.flip(annotated_image, 1))

        if cv2.waitKey(5) & 0xFF == 27:
            break

    # stop the timer and display FPS information
    fps.stop()
    log.info("elasped time: {:.2f}".format(fps.elapsed()))
    log.info("approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    cap.stop()