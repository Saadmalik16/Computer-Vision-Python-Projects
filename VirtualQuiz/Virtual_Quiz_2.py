import cv2
import csv
import cvzone
import time
#from cvzone.HandTrackingModule import HandDetector
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
detector = htm.HandDetector(detectionCon=0.8, maxHands=1)

class MCQ():
    def __init__(self,data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

#Import CSV file data
pathCSV = "Mcqs.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

#Create Object of each MCQS
mcqList= []
for q in dataAll:
    mcqList.append(MCQ(q))
print("Total Length of MCQS Object", len(mcqList))

qNo = 0
qTotal = len(dataAll)

while True:
    success , img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    if qNo < qTotal:
        mcq = mcqList[qNo]
        img, bbox = cvzone.putTextRect(img, mcq.question, [50, 50], 1, 2, offset=30, border=3)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [50, 150], 1, 2, offset=30, border=3)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [250, 150], 1, 2, offset=30, border=3)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [50, 250], 1, 2, offset=30, border=3)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [250, 250], 1, 2, offset=30, border=3)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, info = detector.findDistance(lmList[8], lmList[12])
            if length < 25:
                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                print(mcq.userAns)
                if mcq.userAns is not None:
                    time.sleep(0.5)
                    qNo += 1
    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score += 1
        score = round((score / qTotal) * 100, 2)
        img, _ = cvzone.putTextRect(img, f'Quiz Completed', [100, 200],
                                        1, 2, offset=20, border=2)
        img, _ = cvzone.putTextRect(img, f'Your Score: {score} %', [350, 200],
                                    1, 2, offset=20, border=2)

    #Draw Progress Bar
    barValue = 50 + (350 // qTotal) * qNo
    cv2.rectangle(img, (50, 400), (barValue, 450), (0, 255, 2), cv2.FILLED)
    cv2.rectangle(img, (50, 400), (400, 450), (255, 0, 255), 5)
    img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)} %', [430, 435],
                                2, 2, offset=15)

    cv2.imshow("IMAGE", img) #Flip horizontally 1
    cv2.waitKey(1)