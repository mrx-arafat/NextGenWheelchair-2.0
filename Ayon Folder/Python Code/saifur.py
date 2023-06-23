import cv2
import dlib
import websocket
import json
 
# Set up the WebSocket connection
ws = websocket.WebSocket()
ws.connect("ws://192.168.1.204:81")  # Replace with your WebSocket server URL
print("Connected to WebSocket server")

 
cap = cv2.VideoCapture(0)
 
hog_face_detector = dlib.get_frontal_face_detector()
 
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
 
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    faces = hog_face_detector(gray)
 
    for face in faces:
        face_landmarks = dlib_facelandmark(gray, face)
 
        left1st = (face_landmarks.part(0).x, face_landmarks.part(0).y)
        left2nd = (face_landmarks.part(36).x, face_landmarks.part(36).y)
        dis1 = (left1st[0]-left2nd[0])*(left1st[0]-left2nd[0]) + (left1st[1]-left2nd[1])*(left1st[1]-left2nd[1])
 
        right1st = (face_landmarks.part(16).x, face_landmarks.part(17).y)
        right2nd = (face_landmarks.part(45).x, face_landmarks.part(45).y)
        dis2 = (right1st[0]-right2nd[0])*(right1st[0]-right2nd[0]) + (right1st[1]-right2nd[1])*(right1st[1]-right2nd[1])
 
        lefteye = (face_landmarks.part(21).x, face_landmarks.part(21).y)
        lefteye1 = (face_landmarks.part(39).x, face_landmarks.part(39).y)
 
        dis31 = (lefteye[0]-lefteye1[0])*(lefteye[0]-lefteye1[0]) + (lefteye[1]-lefteye1[1])*(lefteye[1]-lefteye1[1])
 
        righteye = (face_landmarks.part(22).x, face_landmarks.part(22).y)
        righteye1 = (face_landmarks.part(42).x, face_landmarks.part(42).y)
 
        dis32 = (righteye[0]-righteye1[0])*(righteye[0]-righteye1[0]) + (righteye[1]-righteye1[1])*(righteye[1]-righteye1[1])
 
        dis3 = (dis31 + dis32) / 2
 
        middle1st = (face_landmarks.part(33).x, face_landmarks.part(33).y)
        middle2nd = (face_landmarks.part(8).x, face_landmarks.part(8).y)
        dis4 = (middle1st[0]-middle2nd[0])*(middle1st[0]-middle2nd[0]) + (middle1st[1]-middle2nd[1])*(middle1st[1]-middle2nd[1])

        data = {"status":"normal"}

        if(dis1 > 4500):
            data = {"status":"left"}
        elif dis2 > 4500:
            data = {"status":"right"}
        elif dis3 > 1250:
            data = {"status":"up"}
        elif dis4 < 7000:
            data = {"status":"down"}
        # else:
        #     data = {"status": "normal"}
 
        # Send the data as JSON to the WebSocket server
        # ws.send(json.dumps(data))
        # print(f"{data}")
        ws.send(json.dumps(data))
 
        for n in range(0, 68):
 
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
 
            cv2.circle(frame, (x,y), 1, (0, 255, 255), 1)
    cv2.imshow("face landmarks", frame)
 
    key = cv2.waitKey(1)
    if key == 27:
        break
 
cap.release()