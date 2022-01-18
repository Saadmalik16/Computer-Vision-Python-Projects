import cv2
#from cvzone.HandTrackingModule import HandDetector
import HandTrackingModule as htm

class Button:
    #Constructor
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225,225,225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50),2)
        cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 50),
                      cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width,
                                          self.pos[1] + self.height),
                          (125, 125, 125), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width,
                                          self.pos[1] + self.height),
                          (50, 50, 50), 2)
            cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 50),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
            return True
        else:
            return False

#webcam
cap = cv2.VideoCapture(0)
#cap.set(3,1280)
#cap.set(4,720)
#cap.set(10,150)
detector = htm.HandDetector(detectionCon=0.8, maxHands=1)

#Creating Buttons
buttonListValues = [['7','8','9','*'],
                    ['4','5','6','-'],
                    ['1','2','3','+'],
                    ['0','/','.','=']]

buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 70 + 220
        ypos = y * 70 + 130
        buttonList.append(Button((xpos, ypos), 70, 70, buttonListValues[y][x]))

#Variables
myEquation = ''
delayCounter = 0

#loop
while True:
    # get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #detection of hand
    hands, img = detector.findHands(img, flipType=False)

    #draw all buttons
    cv2.rectangle(img, (220,70), (220 + 280, 70 + 60),
                  (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (220,70), (220 + 280, 70 + 60),
                  (50, 50, 50), 2)

    for button in buttonList:
        button.draw(img)

    #Check for hand
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        #print(length)
        x, y = lmList[8]
        if length < 40:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter==0:
                    myValue = buttonListValues[int(i%4)][int(i/4)]
                    if myValue == "=":
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1

    #Avoid duplicates
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    #Display the equation
    cv2.putText(img, myEquation, (230, 115),
                cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    # Display Image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        myEquation = ''