import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(cv2.CAP_PROP_FPS, 60)
segmentor = SelfiSegmentation()
fpsReader = cvzone.FPS()

listImage = os.listdir("img")
print(listImage)
imgList = []
for imgPath in listImage:
    img = cv2.imread(f'img/{imgPath}')
    imgList.append(img)
print(len(imgList))

indexImg = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgOut = segmentor.removeBG(img, imgList[indexImg], threshold=0.8)

    imgStack =cvzone.stackImages([img, imgOut], 2, 1)
    _, imgStack = fpsReader.update(imgStack, color=(0, 0, 255))
    print(indexImg)
    cv2.imshow("Images", imgStack)
    key = cv2.waitKey(1)
    if key == ord('a'):
        indexImg -= 1
    elif key == ord('d'):
        indexImg += 1
    elif key == ord('q'):
        break
