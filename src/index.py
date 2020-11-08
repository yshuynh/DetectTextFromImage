from PIL import Image
import main as detectText
from Constraint import constraint
from Model import Model
from SamplePreprocessor import preprocess
from DataLoader import DataLoader, Batch
import cv2
import os


img = Image.open('image.png') # Can be many different formats.
imgPixel = img.load()
print('width: ', img.width, 'height: ', img.height)  # Get the width and hight of the image for iterating over
#print(pix[99,29])  # Get the RGBA Value of the a pixel of an image
#pix[0,0] = (0, 0, 0)  # Set the RGBA Value of the image (tuple)
#im.save('crop_text.png')  # Save the modified pixels as .png

### CROP WORDS IMG FROM img
### OUTPUT: listCroppedImage
#######################################################################################

cropList = []
visited = [] 
queueVisit = [(0, 0, 1)]
for i in range(img.width): 
    col = [] 
    for j in range(img.height): 
        col.append(0) 
    visited.append(col) 
#visited = [[0] * im.height] * im.width # SAI


def visit(x, y, id):
    global img, imgPixel, visited, queueVisit
    #print(x, " ", y)
    global x1, x2, y1, y2
    x1 = min(x1, x)
    y1 = min(y1, y)
    x2 = max(x2, x)
    y2 = max(y2, y) 
    #print("visited 0,0", visited[0][0])
    #print(x, y, id)
    kc = 10
    xL = max(0, x - kc)
    xR = min(x + kc, img.width - 1)
    yL = max(0, y - kc)
    yR = min(y + kc, img.height - 1)
    #print(xL, xR, yL, yR)
    for u in range(xL, xR + 1):
        for v in range(yL, yR + 1):
            color2 = imgPixel[u, v]
            gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
            if gray_level < 150 and visited[u][v] == 0:
                queueVisit.append([u, v, id])
                visited[u][v] = id 
                #visit(u, v, id)
    return

groupCnt = 0
listCroppedImage = []

for y in range(0, img.height):
    for x in range(0, img.width):
        #print(x, y, visited[x][y])
        #print(visited[15][17])
        color2 = imgPixel[x, y]
        gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
        if gray_level < 150 and visited[x][y] == 0:
            #print(x, y)
            x1 = 1000
            x2 = 0
            y1 = 1000
            y2 = 0
            groupCnt = groupCnt + 1
            #visit(x, y, groupCnt)
            queueVisit = [[x, y, groupCnt]]
            visited[x][y] = groupCnt 
            while len(queueVisit) > 0:
                ele = queueVisit[0]
                visit(ele[0], ele[1], ele[2])
                queueVisit.pop(0)
            #print(x1, " ", y1, " ", x2, " ", y2)
            path = "../cropped/"
            if not os.path.exists(path):
	            os.makedirs(path)
            img.crop((x1, y1, x2 + 1, y2 + 1)).save(path + "new" + str(groupCnt) + ".png")
            listCroppedImage.append({
                'filepath': path + "new" + str(groupCnt) + ".png",
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2
            })

#print(visited[15][17])
#print(visited[0][0])

#print(groupCnt, "group\n")

### DETECT TEXT FROM listImage
### OUTPUT: listRecognizedWords
########################################################################################
def infer(model, fnImg):
	"recognize text in image provided by file path"
	img = preprocess(cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE), Model.imgSize)
	batch = Batch(None, [img])
	(recognized, probability) = model.inferBatch(batch, True)
	print('Recognized:', '"' + recognized[0] + '"')
	print('Probability:', probability[0])
	return recognized[0]

decoderType = 0
model = Model(open('../model/charList.txt').read(), decoderType, mustRestore=True, dump=False)

for element in listCroppedImage:
    #path = "../cropped/"
    #constraint.detectFile = path + filename
    #detectText.main()
    #listTextRecognized.append(constraint.textRecognized)
    #print(filename)
    detectedWord = infer(model, element['filepath'])
    print(detectedWord)
    element['word'] = detectedWord
#print(x1, y1, x2, y2)

# Sắp xếp lại trật tự các chữ (bằng cách sử dụng vị trí các chữ trong image)
for i in range(0, len(listCroppedImage)):
    for j in range(i + 1, len(listCroppedImage)):
        first = listCroppedImage[i]
        second = listCroppedImage[j]
        if (first['x1'] > second['x2'] or first['y1'] > second['x2']):
            listCroppedImage[i], listCroppedImage[j] = listCroppedImage[j], listCroppedImage[i]

# In ra kết quả các chữ nhận diện được trong hình
for element in listCroppedImage:
    print(element['word'], end=" ")

######################################################################################

