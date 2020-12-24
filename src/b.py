from indexClass import DetextText
import os

obj = DetextText()

# obj.toBinaryImage("nhieu02.png", "binary.png")
# obj.cropTextRegion("test02.png")
# img = obj.toBinaryImage('test02.png')
# obj.phongToChu(img)
obj.cropTextRegion('nhieu01.jpg')

exit()

list = obj.cropWordsImgFromImgWithKc("test01.jpg", 1)

newlist = []
for element in list:
    x1 = element['x1']
    x2 = element['x2']
    y1 = element['y1']
    y2 = element['y2']
    S = (x2 - x1) * (y2 - y1)
    print(S)
    if (S >= 1000):
        print('get')
        newlist.append(element)
    else:
        os.remove(element['filepath'])

print(newlist)

a = [1, 2, 3]
a.remove(1)
print(a)
