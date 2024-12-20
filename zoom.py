import cv2
from cvzone.HandTrackingModule import HandDetector


# input fomr webcam
frame=cv2.VideoCapture(0)
frame.set(3,1280)
frame.set(4,720)


# initialize hand detector module with some confidence
Hanr=HandDetector(detectionCon=0.8)

# loop
while True:
    res,img=frame.read()

    # detect the hand
    hands=Hanr.findHands(img)

    # show the output
    cv2.imshow("sample cvzone output",img)
    cv2.waitKey(1)