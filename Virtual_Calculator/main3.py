import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
#cap.set(3,1280)
#cap.set(4,720)
#cap.set(10,150)
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #detection of hand
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        length,  _, img = detector.findDistance(lmList[8], lmList[12], img)
        print(length)

    # Display Image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        myEquation = ''