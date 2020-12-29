import cv2
from indexClass import DetextText

import os

url = 'http://192.168.1.21:8080/video'
vc = cv2.VideoCapture(url)
obj = DetextText()

def showCamera():
    vc = cv2.VideoCapture(url)

    while(True):
        try:
            ret, frame = vc.read()
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame', 800, 600)
            cv2.imshow('frame',frame)
            key = cv2.waitKey(1)
            if key == 27: # exit on ESC
                print("Turning off camera")
                vc.release()
                print("Program ended")
                cv2.destroyAllWindows()
                exit()
            if key == 32:
                cv2.imwrite(filename='abc.jpg',img=frame)
                print("Turning off camera")
                vc.release()
                print("Program ended")
                cv2.destroyAllWindows()
                listDetectedWords = obj.getDetectedWords("abc.jpg", True)
                text = ""
                for element in listDetectedWords:
                    text += element
                    text += ' '

                print(text)
                obj.toSound(listDetectedWords)
                vc = cv2.VideoCapture(url)
        except(KeyboardInterrupt):     
            print("Turning off camera")
            vc.release()
            print("Program ended")
            cv2.destroyAllWindows()
            break


showCamera()