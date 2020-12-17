from PIL import Image
import main as detectText
from Constraint import constraint
from Model import Model
from SamplePreprocessor import preprocess
from DataLoader import DataLoader, Batch
import cv2
import os
import shutil
import pathlib

class DetextText:
    def __init__(self):
        self.grayPoint = 150

        # path = str(pathlib.Path().absolute()) + "/cropped/"
        # for i in range(1, 10000):
        #     if (os.path.isfile(path + "new" + str(i) + ".png")):
        #         os.remove(path + "new" + str(i) + ".png")

    def resizeImage(self, imagePath, width):
        img = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
        print('Original Dimensions : ',img.shape)
        scale_percent = width / img.shape[1] * 100 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite("scaledImage.png", resized)
        print('Resized Dimensions : ',resized.shape) 

    def create2DArray(self, width, height):
        arr = []
        for i in range(width): 
            col = [] 
            for j in range(height): 
                col.append(0) 
            arr.append(col) 
        return arr

    def visit(self, x, y, id, kc):
        self.x1 = min(self.x1, x)
        self.y1 = min(self.y1, y)
        self.x2 = max(self.x2, x)
        self.y2 = max(self.y2, y) 
        #print("visited 0,0", visited[0][0])
        #print(x, y, id)
        xL = max(0, x - kc)
        xR = min(x + kc, self.img.width - 1)
        yL = max(0, y - kc)
        yR = min(y + kc, self.img.height - 1)
        #print(xL, xR, yL, yR)
        for u in range(xL, xR + 1):
            for v in range(yL, yR + 1):
                color2 = self.imgPixel[u, v]
                gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
                if gray_level < self.grayPoint and self.visited[u][v] == 0:
                    self.queueVisit.append([u, v, id])
                    self.visited[u][v] = id 
                    #visit(u, v, id)
        return

    def cropWordsImgFromImgWithKc(self, imagePath, kc):
        print("Start Crop Words Img From Img")
        print("imagePath", imagePath)
        self.img = Image.open(imagePath)
        self.imgPixel = self.img.load()
        print('width: ', self.img.width, 'height: ', self.img.height)

        self.visited = self.create2DArray(self.img.width, self.img.height)
        self.queueVisit = [(0, 0, 1)]
        groupCnt = 0
        listCroppedImage = []

        for y in range(0, self.img.height):
            for x in range(0, self.img.width):
                #print(x, y, visited[x][y])
                #print(visited[15][17])
                color2 = self.imgPixel[x, y]
                gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
                if gray_level < self.grayPoint and self.visited[x][y] == 0:
                    #print(x, y)
                    self.x1 = 1000
                    self.x2 = 0
                    self.y1 = 1000
                    self.y2 = 0
                    groupCnt = groupCnt + 1
                    #visit(x, y, groupCnt)
                    self.queueVisit = [[x, y, groupCnt]]
                    self.visited[x][y] = groupCnt 
                    while len(self.queueVisit) > 0:
                        ele = self.queueVisit[-1]
                        self.visit(ele[0], ele[1], ele[2], kc)
                        self.queueVisit.pop(-1)
                    #print(x1, " ", y1, " ", x2, " ", y2)
                    path = str(pathlib.Path().absolute()) + "/cropped/"
                    if not os.path.exists(path):
                        os.makedirs(path)
                    # for i in range(1, 10000):
                    #     if (os.path.isfile(path + "new" + str(i) + ".png")):
                    #         os.remove(path + "new" + str(i) + ".png")
                    self.img.crop((self.x1, self.y1, self.x2 + 1, self.y2 + 1)).save(path + "new" + str(groupCnt) + ".png")
                    listCroppedImage.append({
                        'filepath': path + "new" + str(groupCnt) + ".png",
                        'x1': self.x1,
                        'x2': self.x2,
                        'y1': self.y1,
                        'y2': self.y2
                    })

        return listCroppedImage

    def getKc(self, imagePath):
        kc = 0
        listCroppedImage = self.cropWordsImgFromImgWithKc(imagePath, 1)

        for element in listCroppedImage:
            kc = max(kc, element['x2'] - element['x1'])
        kc = int(kc / 2)
        print(listCroppedImage)
        print("kc = ", kc)

        # kc = 1000
        # for i in range(0, len(listCroppedImage)):
        #     for j in range(i + 1, len(listCroppedImage)):
        #         kc = min(kc, abs(listCroppedImage[i]['x1'] - listCroppedImage[j]['x1'])


        return kc

    def cropWordsImgFromImg(self, imagePath):
        return self.cropWordsImgFromImgWithKc(imagePath, self.getKc(imagePath))

    def infer(self, model, fnImg):
        "recognize text in image provided by file path"
        img = preprocess(cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE), Model.imgSize)
        batch = Batch(None, [img])
        (recognized, probability) = model.inferBatch(batch, True)
        print('Recognized:', '"' + recognized[0] + '"')
        print('Probability:', probability[0])
        return recognized[0]

    def sortByPosition(self, listCroppedImage):
        for i in range(0, len(listCroppedImage)):
            for j in range(i + 1, len(listCroppedImage)):
                first = listCroppedImage[i]
                second = listCroppedImage[j]
                if ((first['y1'] > second['y2']) or (first['y1'] <= second['y2'] and first['y2'] >= second['y1'] and first['x1'] > second['x2'])):
                    listCroppedImage[i], listCroppedImage[j] = listCroppedImage[j], listCroppedImage[i]
        return listCroppedImage

    def getDetectedWords(self, imagePath, isScale = False):

        if isScale:
            self.resizeImage(imagePath, 500)
            imagePath = 'scaledImage.png'

        listCroppedImage = self.cropWordsImgFromImg(imagePath)
        # listCroppedImage = self.cropWordsImgFromImgWithKc(imagePath, 1)
        decoderType = 0
        model = Model(open('../model/charList.txt').read(), decoderType, mustRestore=True, dump=False)
        for element in listCroppedImage:
            #path = "../cropped/"
            #constraint.detectFile = path + filename
            #detectText.main()
            #listTextRecognized.append(constraint.textRecognized)
            #print(filename)
            detectedWord = self.infer(model, element['filepath'])
            print(detectedWord)
            element['word'] = detectedWord
        
        listCroppedImage = self.sortByPosition(listCroppedImage)
        listDetectedWords = []
        for element in listCroppedImage:
            listDetectedWords.append(element['word']) 
        return listDetectedWords



# obj = DetextText()
# obj.resizeImage("test01.jpg", 500)
# print(obj.getDetectedWords("scaledImage.png"))