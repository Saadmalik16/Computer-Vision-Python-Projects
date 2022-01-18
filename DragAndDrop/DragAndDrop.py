import cv2
import cvzone
import numpy
#from cvzone.HandTrackingModule import HandDetector
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
#detector = HandDetector(detectionCon=0.8)
detector = htm.HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)
cx, cy, w, h = 50, 50, 100, 100

class DragRect():
    def __init__(self, posCenter, size=[100, 100]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        #If the index finger in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and \
            cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor

rectList = []
for x in range(5):
    #rectList.append(DragRect([x * 100 + 50, 100]))
    rectList.append(DragRect([x * 120 + 70, 120]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img) # _ means ignore the argument

    if lmList:
        length, _, _ = detector.findDistance(8, 12, img)
        print(length)
        if length < 20:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)

    #Draw Solid
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    #Draw Traspency
    #imgNew = np.zeros_like(img, np.uint8)
    #for rect in rectList:
        #cx, cy = rect.posCenter
        #w, h = rect.size
        #cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        #cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    #out = img.copy()
    #alpha = 0.5
    #mask = imgNew.astype(bool)
    #out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", img)
    cv2.waitKey(1)