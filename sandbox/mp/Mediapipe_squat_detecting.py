# [[累累累] Google Mediapipe 深蹲偵測，結合 Arduino 首次接觸就上手 - CAVEDU教育團隊技術部落格](https://blog.cavedu.com/2022/05/12/mediapipe-squat-detection/)

import cv2
import mediapipe as mp
import numpy as np
import time
import json
#import serial

from pathlib import Path
ROOT = Path(__file__).parent

cam = cv2.VideoCapture(0)
mppose = mp.solutions.pose
mpdraw = mp.solutions.drawing_utils
poses = mppose.Pose()
h = 0
w = 0
#ser = serial.Serial("COM3", 9600)

start_time = 0
status = False

sport = {
    "name": "Squat",
    "count": 0,
    "calories": 0
}


def logger(count, cals):
    f = open(ROOT / "log.txt", 'a')
    fs = f"{time.ctime()} count: {count} cals: {cals}\n"
    f.write(fs)
    f.close()


def calc_angles(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
              np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


def get_landmark(landmarks, part_name):
    return [
        landmarks[mppose.PoseLandmark[part_name].value].x,
        landmarks[mppose.PoseLandmark[part_name].value].y,
        landmarks[mppose.PoseLandmark[part_name].value].z,
    ]


def get_visibility(landmarks):
    if landmarks[mppose.PoseLandmark["RIGHT_HIP"].value].visibility < 0.8 or \
            landmarks[mppose.PoseLandmark["LEFT_HIP"].value].visibility < 0.8:
        return False
    else:
        return True


def get_body_ratio(landmarks):
    r_body = abs(landmarks[mppose.PoseLandmark["RIGHT_SHOULDER"].value].y
                 - landmarks[mppose.PoseLandmark["RIGHT_HIP"].value].y)
    l_body = abs(landmarks[mppose.PoseLandmark["LEFT_SHOULDER"].value].y
                 - landmarks[mppose.PoseLandmark["LEFT_HIP"].value].y)
    avg_body = (r_body + l_body) / 2
    r_leg = abs(landmarks[mppose.PoseLandmark["RIGHT_HIP"].value].y
                - landmarks[mppose.PoseLandmark["RIGHT_ANKLE"].value].y)
    l_leg = abs(landmarks[mppose.PoseLandmark["LEFT_HIP"].value].y
                - landmarks[mppose.PoseLandmark["LEFT_ANKLE"].value].y)
    if r_leg > l_leg:
        return r_leg / avg_body
    else:
        return l_leg / avg_body


def get_knee_angle(landmarks):
    r_hip = get_landmark(landmarks, "RIGHT_HIP")
    l_hip = get_landmark(landmarks, "LEFT_HIP")

    r_knee = get_landmark(landmarks, "RIGHT_KNEE")
    l_knee = get_landmark(landmarks, "LEFT_KNEE")

    r_ankle = get_landmark(landmarks, "RIGHT_ANKLE")
    l_ankle = get_landmark(landmarks, "LEFT_ANKLE")

    r_angle = calc_angles(r_hip, r_knee, r_ankle)
    l_angle = calc_angles(l_hip, l_knee, l_ankle)

    m_hip = (r_hip + l_hip)
    m_hip = [x / 2 for x in m_hip]
    m_knee = (r_knee + l_knee)
    m_knee = [x / 2 for x in m_knee]
    m_ankle = (r_ankle + l_ankle)
    m_ankle = [x / 2 for x in m_ankle]

    mid_angle = calc_angles(m_hip, m_knee, m_ankle)

    return [r_angle, l_angle, mid_angle]


def main():
    global h, w, start_time, status
    flag = False
    if not cam.isOpened():
        print("Camera not open")
        exit()

    try:
        f = open(ROOT / "sport_recorder.json", "r")
        prevdata = json.load(f)
        if sport['name'] == prevdata['name']:
            sport['count'] = prevdata['count']
            sport['calories'] = prevdata['calories']
            print("Read Success!")
        f.close()
    except:
        print("Read Error...")
        pass

    tmp = f"a{sport['count']}\n"
    #ser.write(str.encode(tmp))
    tmp = f"b{sport['calories']}\n"
    #ser.write(str.encode(tmp))

    cv2.namedWindow('frame', cv2.WINDOW_FREERATIO)

    while not flag:
        ret, frame = cam.read()
        if not ret:
            print("Read Error")
            break
        frame = cv2.flip(frame, 1)
        rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        poseoutput = poses.process(rgbframe)
        h, w, _ = frame.shape
        preview = frame.copy()

        if poseoutput.pose_landmarks:
            mpdraw.draw_landmarks(preview, poseoutput.pose_landmarks, mppose.POSE_CONNECTIONS)
            knee_angles = get_knee_angle(poseoutput.pose_landmarks.landmark)
            body_ratio = get_body_ratio(poseoutput.pose_landmarks.landmark)
            if knee_angles[0] < 120:
                cv2.putText(preview, "Left: Down {:.1f}".format(knee_angles[0]), (10, 40)
                            , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
            elif knee_angles[0] < 130:
                cv2.putText(preview, "Left: ??? {:.1f}".format(knee_angles[0]), (10, 40)
                            , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA
                            )
            else:
                cv2.putText(preview, "Left: Up {:.1f}".format(knee_angles[0]), (10, 40)
                            , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                            )

            if knee_angles[1] < 120:
                cv2.putText(preview, "Right: Down {:.1f}".format(knee_angles[1]), (10, 80)
                            , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
            elif knee_angles[1] < 130:
                cv2.putText(preview, "Right: ??? {:.1f}".format(knee_angles[1]), (10, 80)
                            , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA
                            )
            else:
                cv2.putText(preview, "Right: Up {:.1f}".format(knee_angles[1]), (10, 80)
                            , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                            )

            avg_angle = (knee_angles[0] + knee_angles[1]) // 2

            # determine the status
            if status:
                if avg_angle > 160:
                    status = False
                    pass_time = time.time() - start_time
                    start_time = 0
                    if 3000 > pass_time > 3:
                        sport['count'] = sport['count'] + 1
                        sport['calories'] = sport['calories'] + int(0.66 * pass_time)
                        logger(sport['count'], sport['calories'])
                        tmp = f"a{sport['count']}\n"
                        #ser.write(str.encode(tmp))
                        tmp = f"b{sport['calories']}\n"
                        #ser.write(str.encode(tmp))

            else:
                if avg_angle < 120 and body_ratio < 1.2:
                    start_time = time.time()
                    status = True

            # print(f"status:{status} {start_time}")
            if status:
                cv2.putText(preview, f"{status} : {avg_angle:.1f} {body_ratio:.3f}", (10, 120)
                            , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
                #if time.time() - start_time > 3:
                    #ser.write(b'command_2\n')
                #else:
                    #ser.write(b'command_1\n')
            else:
                cv2.putText(preview, f"{status} : {avg_angle:.1f} {body_ratio:.3f}", (10, 120)
                            , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                            )
                #ser.write(b'command_4\n')
        else:
            #ser.write(b'command_4\n')
            start_time = 0

        cv2.imshow('frame', preview)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            flag = True

    f = open(ROOT / "sport_recorder.json", "w+")
    f.write(json.dumps(sport))
    f.close()

    # release camera
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()