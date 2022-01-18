# Libraries
import cv2
import numpy as np
import time
import HandTrackingModule as htm
import pyautogui
#import autopy

# Variables
wCam, hCam = 640, 480
frameR = 100 # frame Reduction
smoothening = 7
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7, maxHands=1)
wScr, hScr = pyautogui.size()
#wScr, hScr = autopy.screen.size()
#print(wScr,hScr) 1366  768 by pyautogui

while True:
    #1- Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    #2- Get the tip of index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print(x1, x2, y1, y2)

        #3- Check which finger are up
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        # 4- Only Index fingers : Moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            #5- Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6 - Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocX) / smoothening

            # 7 - Move Mouse
            #autopy.mouse.move(wScr - clocX, clocY)
            #pyautogui.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, ploxY = clocX, clocY

        # 8- Both index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9- Find Distance between the fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            #print(length)
            # 10 - Click mouse if Distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                #autopy.mouse.click()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)