import math
import random
import cvzone
import numpy as np
import cv2
import HandTrackingModule as htm
#from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = htm.HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGame:
    def __init__(self, pathFood):
        self.points = [] # All points of the snake
        self.lengths = [] # Distance between each points
        self.currentLength = 0 # Total Length of Snake
        self.allowedLength = 120 # Total allowed Length
        self.previousHead = 0, 0 # Previous Head Points

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(80, 500), random.randint(80, 350)

    def update(self, imgMain, currentHead):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [100, 200], offset=5, thickness=3, scale=4)
            cvzone.putTextRect(imgMain, f'Your Score {self.score}', [100, 300], offset=5, thickness=3, scale=4)

        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Check if Snake eat the Fries
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 40
                self.score += 1
                print(self.score)

            #Draw Snake
            if self.points:
                for i, points in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 15)
                cv2.circle(imgMain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

            #Draw Food
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))
            cvzone.putTextRect(imgMain, f'Your Score {self.score}', [30, 50], offset=3, thickness=2, scale=2)

            #Check for Collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 200, 0), 2)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            if -1 <= minDist <= 1:
                print("Hit")
                self.gameOver = True
                self.points = []  # All points of the snake
                self.lengths = []  # Distance between each points
                self.currentLength = 0  # Total Length of Snake
                self.allowedLength = 120  # Total allowed Length
                self.previousHead = 0, 0  # Previous Head Points
                self.randomFoodLocation()
                self.score = 0

        return imgMain

game = SnakeGame("fries.png")
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
