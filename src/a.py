from indexClass import DetextText
from gtts import gTTS
import playsound

import os

obj = DetextText()
# obj.resizeImage("test01.jpg", 500)
# print(obj.getDetectedWords("scaledImage.png"))

listDetectedWords = obj.getDetectedWords("test02.png", True)
text = ""
for element in listDetectedWords:
    text += element
    text += ' '

print(text)

# text to speech
tts = gTTS(text, lang="vi")
file_name = 'speech.mp3'
tts.save(file_name)
playsound.playsound(file_name)
#