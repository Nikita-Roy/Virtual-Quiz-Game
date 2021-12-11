import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detect_hand = HandDetector(detectionCon=0.8)

class MCQ():
    def __init__(self,data):
        self.question = data[0]
        self.ch1 = data[1]
        self.ch2 = data[2]
        self.ch3 = data[3]
        self.ch4 = data[4]
        self.ans = int(data[5])

        self.UserAns = None

    def clickoption(self, cursor, bboxlist):
        for x, bbox in enumerate(bboxlist):
            x1, y1, x2, y2, = bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.UserAns = x+1
                cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), cv2.FILLED)

#import csv file data
pathCSV = "MCQ_Questions.csv"
with open(pathCSV, newline = '\n') as f:
    reader = csv.reader(f)
    csv_data = list(reader)[1:]
#print(len(qdata))

#creating object for each MCQ
MCQList = []
for q in csv_data:
    MCQList.append(MCQ(q))
print(len(MCQList))

q_no = 0
total_q = len(csv_data)
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detect_hand.findHands(img, flipType= False)

    if q_no<total_q:
        MCQ = MCQList[q_no]
        img, bboxq = cvzone.putTextRect(img, MCQ.question, [100,100], 2, 2, offset = 20, border = 5)
        img, bbox1 = cvzone.putTextRect(img, MCQ.ch1, [100, 250], 2, 2, offset=20, border=5)
        img, bbox2 = cvzone.putTextRect(img, MCQ.ch2, [400, 250], 2, 2, offset=20, border=5)
        img, bbox3 = cvzone.putTextRect(img, MCQ.ch3, [100, 400], 2, 2, offset=20, border=5)
        img, bbox4 = cvzone.putTextRect(img, MCQ.ch4, [400, 400], 2, 2, offset=20, border=5)

        if hands:
            lmList = hands[0]['lmList']
            pointer = lmList[8]
            len, info = detect_hand.findDistance(lmList[4], lmList[8])
            #print(len)
            if len<60:
                MCQ.clickoption(pointer, [bbox1, bbox2, bbox3, bbox4])
                print(MCQ.UserAns)
                if MCQ.UserAns is not None:
                    time.sleep(0.3)
                    q_no += 1

    else:
        score = 0
        for MCQ in MCQList:
            if MCQ.ans == MCQ.UserAns:
                score +=1
        img, _ = cvzone.putTextRect(img, "Quiz is completed", [250, 300], 2, 2, offset=50, border=5)
        img, _ = cvzone.putTextRect(img, f'Your SCORE: {score}', [700, 300], 2, 2, offset=50, border=5)
        #print(score)

    #Draw progress bar
    Value_of_bar = 150 +(950//total_q)*q_no
    cv2.rectangle(img, (150,600), (Value_of_bar, 650),(0,255,0), cv2.FILLED)
    cv2.rectangle(img, (150,600), (1100, 650), (255, 0, 255), 5)
    img, _ =cvzone.putTextRect(img, f'{round((q_no/total_q)*100)}%', [1130, 635], 2, 2, offset=16)

    cv2.imshow("Img",img)
    if cv2.waitKey(1) == ord('q'):
      break
cap.release()
cv2.destroyAllWindows()
