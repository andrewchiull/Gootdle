# [Pose landmark detection guide for Python  |  MediaPipe  |  Google for Developers](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/python?authuser=2#live-stream)

from settings import S, create_logger
import cv2
import numpy as np

from imutils.video import WebcamVideoStream
from imutils.video import FPS
model_path = S.ROOT / "src/cv/mp" / "pose_landmarker_lite.task"


import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarker, PoseLandmarkerOptions, PoseLandmarkerResult

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


BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the live stream mode:
def print_result(detection_result: PoseLandmarkerResult, image: mp.Image, timestamp_ms: int):
    # TODO imshow
    # print('pose landmarker result: {}'.format(detection_result))

    # STEP 5: Process the detection result. In this case, visualize it.
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    cv2.imshow("img", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

    # segmentation_mask = detection_result.segmentation_masks[0].numpy_view()
    # visualized_mask = np.repeat(segmentation_mask[:, :, np.newaxis], 3, axis=2) * 255
    # cv2.imshow("img",visualized_mask)


options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

# cap = WebcamVideoStream(src=S.VIDEO_SOURCE).start()
cap = WebcamVideoStream(src=0).start()
fps = FPS().start()
timestamp = 0
with PoseLandmarker.create_from_options(options) as detector:
    # The landmarker is initialized. Use it here.

    while cap.grabbed:
        fps.update()
        frame = cap.read()
        timestamp += 1
        # cv2.imshow('MediaPipe Pose',
        #         #    frame,
        #            cv2.flip(frame, 1)
        # )

        # STEP 3: Load the input image.
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        
        # STEP 4: Detect pose landmarks from the input image.
        detector.detect_async(image, timestamp)
        # detection_result = detector.detect_async(image, timestamp)

        if cv2.waitKey(5) & 0xFF == 27:
            break