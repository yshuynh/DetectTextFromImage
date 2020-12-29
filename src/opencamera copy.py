import cv2
from indexClass import DetextText
from gtts import gTTS
import playsound

import os

obj = DetextText()
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    if key == 32:
        cv2.imwrite("abc.jpg", frame)
        listDetectedWords = obj.getDetectedWords("abc.jpg", True)
        text = ""
        for element in listDetectedWords:
            text += element
            text += ' '

        print(text)

    

cv2.destroyWindow("preview")