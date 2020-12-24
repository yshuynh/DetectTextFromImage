from indexClass import DetextText
from detexttextregion import CropTextRegion
from gtts import gTTS
import playsound
import glob
import time

import os


obj = DetextText()


#---------------
# obj.cropTextRegion("tho01.jpg")
# text = ""
# path = "region/"
# files = glob.glob(path+'*.png', recursive=True)
# for f in files:
#     print(f)
#     listDetectedWords = obj.getDetectedWords(f, True)
#     for element in listDetectedWords:
#         text += element
#         text += ' '
# print(text)
# exit()


#--------------

#------------------
list = obj.getDetectedWords("tho01.jpg", True)
# obj.toBinaryImage("tho03.jpg")
# list = obj.cropWordsImgFromImgWithKc("test01.jpg", 2)
print(list)
exit()

#------------------

cropTextRegion = CropTextRegion()
# obj.resizeImage("test01.jpg", 500)
# print(obj.getDetectedWords("test02.png", True))
# exit()
imagePath = "arial01.png"

cropTextRegion.cropTextRegion(imagePath)
# exit()

path = "region/"
files = glob.glob(path+'*.png', recursive=True)

text = ""
for f in files:
    print(f)
    listDetectedWords = obj.getDetectedWords(f, True)
    for element in listDetectedWords:
        text += element
        text += ' '
    # time.sleep(2)
    # break

print(text)

# # text to speech
# tts = gTTS(text, lang="vi")
# file_name = 'speech.mp3'
# tts.save(file_name)
# playsound.playsound(file_name)
#