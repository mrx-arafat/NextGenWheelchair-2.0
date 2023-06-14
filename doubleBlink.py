import cv2
import cvzone
import time
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [20, 50], invert=True)

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)
blinkCounter = 0
timer = 0
lastOpen = 0
doubleBlink = 0
blinkList = []
blink1 = 0
blink2 = 0

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img = cv2.flip(img, 1)
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5,color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)

        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35:# and counter == 0:
            blinkCounter += 1
            blinkList.append(time.time())
            
            if len(blinkList) < 2:
                continue
            if len(blinkList) > 2:
                blinkList.pop(0)
                
            blink1 = blinkList[0]
            blink2 = blinkList[1]
            # print(blink1)
            # print(lastOpen)
            
            if (blink1 < lastOpen) and (lastOpen<blink2) and (blink2-blink1 < 0.8):
                print('Double blink detcted')
                doubleBlink += 1
                # color = (255)
                # cvzone.putTextRect(img, 'Double blink detcted', (50, 100), colorR=color)
                # cv2.imshow("Image", img)
                # cv2.waitKey(1000)
                
            color = (0,200,0)
            counter = 1
            
        else:
            lastOpen = time.time()
        
        print('lastopen = ', lastOpen)
        print('blink2 = ', blink2)
        
        if len(blinkList)>1 and (blink2 - lastOpen) > 10:
            print('Alart please!!!')
            cvzone.putTextRect(img, 'Alarm!!!', (50, 100), colorR=(255, 0, 0))
            # cv2.imshow("Image", imgStack)
            # cv2.waitKey(50)
            
        # if counter != 0:
        #     counter += 1
        #     if counter > 10:
        #         counter = 0
        #         color = (255,0, 255)

        cvzone.putTextRect(img, f'Blink Count: {doubleBlink}', (50, 100), colorR=color)

        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)

    cv2.imshow("Image", imgStack)
    # cv2.imshow("Image", img)
    cv2.waitKey(10)
    
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
