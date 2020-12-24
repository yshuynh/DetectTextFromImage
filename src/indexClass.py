from PIL import Image
import main as detectText
from Constraint import constraint
from Model import Model
from SamplePreprocessor import preprocess
from DataLoader import DataLoader, Batch
import cv2
from cv2 import boundingRect, countNonZero, cvtColor, drawContours, findContours, getStructuringElement, imread, morphologyEx, pyrDown, rectangle, threshold
import os
import shutil
import pathlib
import glob
import numpy as np

class DetextText:
    def __init__(self):
        self.grayPoint = 50
        decoderType = 0
        self.model = Model(open('../model/charList.txt').read(), decoderType, mustRestore=True, dump=False)

        # path = str(pathlib.Path().absolute()) + "/cropped/"
        # for i in range(1, 10000):
        #     if (os.path.isfile(path + "new" + str(i) + ".png")):
        #         os.remove(path + "new" + str(i) + ".png")

    # output: folder region
    def cropTextRegion(self, imagePath, scale = 500):
        self.resizeImage(imagePath, scale)
        image_path = "scaledImage.png"
        path = "region/"
        self.createCroppedDic(path)


        large = imread(image_path)
        # downsample and use it for processing
        rgb = pyrDown(large)
        # apply grayscale
        small = cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        # morphological gradient
        morph_kernel = getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        grad = morphologyEx(small, cv2.MORPH_GRADIENT, morph_kernel)
        # binarize
        _, bw = threshold(src=grad, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        morph_kernel = getStructuringElement(cv2.MORPH_RECT, (9, 1))
        # connect horizontally oriented regions
        connected = morphologyEx(bw, cv2.MORPH_CLOSE, morph_kernel)
        mask = np.zeros(bw.shape, np.uint8)
        # find contours
        contours, hierarchy = findContours(connected, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        # filter contours
        dem = 0
        obj = DetextText()
        text = ' '
        for idx in range(0, len(hierarchy[0])):
            rect = x, y, rect_width, rect_height = boundingRect(contours[idx])
            # fill the contour
            mask = drawContours(mask, contours, idx, (255, 255, 2555), cv2.FILLED)
            # ratio of non-zero pixels in the filled region
            r = float(countNonZero(mask)) / (rect_width * rect_height)
            if r > 0.45 and rect_height > 8 and rect_width > 8:
                # rgb = rectangle(rgb, (x, y+rect_height), (x+rect_width, y), (0,255,0),3)
                crop_img = rgb[y+1:y+rect_height-2, x+1:x+rect_width-2]
                # cv2.imshow("cropped", crop_img)
                dem = dem + 1
                cv2.imwrite(self.path + str(dem) + ".png", crop_img)
                # listDetectedWords = obj.getDetectedWords(path + str(dem) + ".png")
                # for element in listDetectedWords:
                #     text += element
                #     text += ' '
                # print(text)
                # cv2.waitKey(0)

    def toBinaryImage(self, imagePath, destinationPath = 'binary.png'):
        # img = self.resizeImage(imagePath, 1000)
        img = Image.open(imagePath)
        imgPixel = img.load()
       
       
        for y in range(0, img.height):
            for x in range(0, img.width):
                color2 = imgPixel[x, y]
                gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
                if gray_level < self.grayPoint:
                    img.putpixel((x, y), (0, 0, 0))
                else:
                    img.putpixel((x, y), (255, 255, 255))
        img.save(destinationPath)
        self.binaryImg = Image.open(destinationPath)
        return img

    def createCroppedDic(self, path):
        files = glob.glob(path+'*.png', recursive=True)
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path

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
        path = "cropped/"
        self.createCroppedDic(path)
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
                    self.x1 = 100000
                    self.x2 = 0
                    self.y1 = 100000
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
                    # for i in range(1, 10000):
                    #     if (os.path.isfile(path + "new" + str(i) + ".png")):
                    #         os.remove(path + "new" + str(i) + ".png")
                    # khu nhieu
                    if self.x2 - self.x1 + 1 <= 5:
                        continue

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
        listCroppedImage = self.cropWordsImgFromImgWithKc(imagePath, 2)
        sum = 0
        dem = 0

        for element in listCroppedImage:
            kc = max(kc, element['x2'] - element['x1'])
            sum = sum + element['x2'] - element['x1']
            dem = dem + 1
        kc = int(kc / 3)
        print("sum =", sum, "dem=", dem)
        kc = int(sum / dem * 0.8)
        # print(listCroppedImage)
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
        
        path = "sorted/"
        self.createCroppedDic(path)
        dem = 0
        for ele in listCroppedImage:
            dem = dem + 1
            self.img.crop((ele['x1'], ele['y1'], ele['x2'] + 1, ele['y2'] + 1)).save(path + "sort" + str(dem) + ".png")

        return listCroppedImage

    def getDetectedWords(self, imagePath, isScale = False):
        self.toBinaryImage(imagePath)

        if isScale:
            self.resizeImage(imagePath, 1000)
            imagePath = 'scaledImage.png'

        listCroppedImage = self.cropWordsImgFromImg(imagePath)
        # listCroppedImage = self.cropWordsImgFromImgWithKc(imagePath, 1)
        
        for element in listCroppedImage:
            #path = "../cropped/"
            #constraint.detectFile = path + filename
            #detectText.main()
            #listTextRecognized.append(constraint.textRecognized)
            #print(filename)
            detectedWord = self.infer(self.model, element['filepath'])
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