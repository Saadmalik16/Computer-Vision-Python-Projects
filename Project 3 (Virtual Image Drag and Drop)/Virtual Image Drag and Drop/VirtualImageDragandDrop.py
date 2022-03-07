import cv2
import cvzone
import os
import HandTrackingModule as htm
#from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = htm.HandDetector(detectionCon=0.8)

class DragImg():
    def __init__(self, path, posOrigion, imgType):
        self.path = path
        self.posOrigion = posOrigion
        self.imgType = imgType

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigion
        h, w = self.size

        #check if in rigion
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigion = cursor[0] - w // 2, cursor[1] - h // 2


#img1 = cv2.imread("ImageJPG/1.jpg")
#img1 = cv2.imread("ImagePNG/1.png", cv2.IMREAD_UNCHANGED)
#ox, oy = 200, 200

path = "ImageJPG"
myList = os.listdir(path)
print(myList)

listImg = []
for x, pathImg in enumerate(myList):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{path}/{pathImg}', [30 + x * 300, 60], imgType))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        lmList = hands[0]['lmList']
        #Check if Clicked
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)
        #print(length)
        if length < 30:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)

    try:
        for imgObject in listImg:
            h, w = imgObject.size
            ox, oy = imgObject.posOrigion
            if imgObject.imgType == "png":
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img
    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)