import cv2
import numpy as np
import face_recognition
from scipy.spatial import distance as dist
import time

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def blink_detector(landmarks):
    rightEye = landmarks['right_eye']
    leftEye = landmarks['left_eye']
    ear = (eye_aspect_ratio(rightEye) + eye_aspect_ratio(leftEye)) / 2.0
    return ear < 0.3

if __name__ =='__main__':
    Camera = cv2.VideoCapture(0)
    _, frame = Camera.read()
    blink_count = 0
    consecutive_blinks = 0
    double_blink_counter = 0
    blink_in_progress = False
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    box = face_recognition.face_locations(frameRGB)
    cx_ = (box[0][3] + box[0][1]) / 2
    cy_ = (box[0][0] + box[0][2]) / 2
    MIN_MOVE = 10

    while True:
        ret, frame = Camera.read()
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # scale down resolution by 50%
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        box = face_recognition.face_locations(frameRGB)
        if box:
            cx = (box[0][3] + box[0][1]) / 2
            cy = (box[0][0] + box[0][2]) / 2
            landmarks = face_recognition.face_landmarks(frameRGB, box)

            if landmarks and blink_detector(landmarks[0]):
                if not blink_in_progress:
                    blink_count += 1
                    blink_in_progress = True
                    if blink_count - consecutive_blinks == 1:
                        double_blink_counter += 1
                    else:
                        double_blink_counter = 0
                    consecutive_blinks = blink_count
            else:
                blink_in_progress = False

            if double_blink_counter == 2:
                print("Double blink detected!")
                double_blink_counter = 0

            if abs(cx - cx_) > abs(cy - cy_):
                if cx - cx_ > MIN_MOVE:
                    print('LEFT')
                elif cx - cx_ < -MIN_MOVE:
                    print('RIHT')
            else:
                if cy - cy_ > MIN_MOVE:
                    print('DOWN')
                elif cy - cy_ < -MIN_MOVE:
                    print('UP')
            print('Blink count: ', blink_count)

            cv2.rectangle(frame, (box[0][3], box[0][0]), (box[0][1], box[0][2]), (0, 0, 255), 2)
            cv2.imshow("unlock Face", frame)
            key = cv2.waitKey(30)
            cx_ = cx
            cy_ = cy
            if key == 27:
                break
