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
import glob

class DetextText:

    def createCroppedDic(self):
        path = "cropped/"
        files = glob.glob(path+'*.png', recursive=True)
        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path

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
        return img

    def getPoints(self, imgPixel, val, x1, y1, x2, y2):
        dem = int(0)
        print(x2, y2)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                color2 = imgPixel[x, y]
                gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
                if gray_level == val:
                    dem = dem + 1
        return dem

    def setRectPoint(self, img, val, x1, y1, x2, y2):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                img.putpixel((x, y), (val, val, val))
        return img

    def khuNhieu(self, imagePath):
        self.resizeImage(imagePath, 500)
        img = self.toBinaryImage('scaledImage.png')
        imgPixel = img.load()
        listCroppedImage = self.cropWordsImgFromImgWithKc('scaledImage.png', 2)
        print("size", img.width, img.height)
        for ele in listCroppedImage:
            # cntWhite = self.getPoints(imgPixel, 0, ele['x1'], ele['y1'], ele['x2'], ele['y2'])
            cntBlack = self.getPoints(imgPixel, 255, ele['x1'], ele['y1'], ele['x2'], ele['y2'])
            S = (ele['x2'] - ele['x1'] + 1) * (ele['y2'] - ele['y1'] + 1)
            # if float(cntBlack) / S < 0.0001 or float(cntBlack) / S > 0.8:
            #     img = self.setRectPoint(img, 255, ele['x1'], ele['y1'], ele['x2'], ele['y2'])
            if (ele['x2'] - ele['x1'] + 1) / (ele['y2'] - ele['y1'] + 1) > 3.0:
                img = self.setRectPoint(img, 255, ele['x1'], ele['y1'], ele['x2'], ele['y2'])
            if (ele['y2'] - ele['y1'] + 1) / img.height < 0.01:
                img = self.setRectPoint(img, 255, ele['x1'], ele['y1'], ele['x2'], ele['y2'])

        img.save('khunhieu.png')


    def phongToChu(self, img):
        scaleLevel = 20
        imgPixel = img.load()
        list = []
        for y in range(0, img.height):
            for x in range(0, img.width):
                color2 = imgPixel[x, y]
                gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
                if gray_level == 0:
                    for newx in range(max(x - scaleLevel, 0), min(x + scaleLevel, img.width)):
                        # imgcopy.putpixel((newx, y), (0, 0, 0))
                        list.append((newx , y))
                    # for newy in range(max(y - scaleLevel, 0), min(y + scaleLevel, img.height)):
                    #     imgcopy.putpixel((x, newy), (0, 0, 0))
                        # list.append((x , newy))
        for element in list:
            img.putpixel((element), (0, 0, 0))
        img.save('phongtochu.png')

    def getGrayLevel(self, imgPixel, x, y):
        color2 = imgPixel[x, y]
        gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
        return gray_level

    def cropTextRegion2(self, imagePath):
        img = self.toBinaryImage(imagePath)
        imgPixel = img.load()
        
        x1, x2, y1, y2 = 0, 0, 0, 0

        for x1_ in range(0, img.width):
            for y1_ in range(0, img.height):
                for x2_ in range(x1_ + 1, img.width):
                    for y2_ in range(y1_ + 1, img.height):
                        kt = 1
                        for i in range(x1_, x2_):
                            if self.getGrayLevel(imgPixel, i, y1_) == 0 or self.getGrayLevel(imgPixel, i, y2_) == 0:
                                kt = 0
                                break
                        for i in range(y1_, y2_):
                            if self.getGrayLevel(imgPixel, x1_, i) == 0 or self.getGrayLevel(imgPixel, x2_, i) == 0:
                                kt = 0
                                break
                        if (kt == 1):
                            curS = (x2_ - x1_) * (y2_ - y1_)
                            S = (x2 - x1) * (y2- y1)
                            if (curS > S):
                                x1, x2, y1, y2 = x1_, x2_, y1_, y2_
        path = "region/"
        if not os.path.exists(path):
            os.makedirs(path)
        img.crop((x1, y1, x2 + 1, y2 + 1)).save(path + "new" + str(x) + "-" + str(y) + ".png")
        list.append({
            'x1': x1,
            'x2': x2,
            'y1': y1,
            'y2': y2
        })
        print(list)

    def cropTextRegion(self, imagePath):
        img = self.toBinaryImage(imagePath)
        imgPixel = img.load()
        
        check = self.create2DArray(img.width, img.height)
        dx = [-1, 11, 0, 0]
        dy = [0, 0, -1, 1]

        list = []

        for y in range(0, img.height):
            for x in range(0, img.width):
                if check[x][y] == 0 and self.getGrayLevel(imgPixel, x, y) > 0:
                    check[x][y] = 1
                    x1, y1, x2, y2 = img.width, img.height, 0, 0
                    queue = [(x, y)]
                    while len(queue) > 0:
                        ele = queue[-1]
                        x1 = min(x1, ele[0])
                        x2 = max(x2, ele[0])
                        y1 = min(y1, ele[1])
                        y2 = max(y2, ele[1])
                        queue.pop(-1)
                        for i in range(0, 4):
                            newx = ele[0] + dx[i]
                            newy = ele[1] + dy[i]
                            if (newx < 0 or newx >= img.width or newy < 0 or newy >= img.height):
                                continue
                            if (self.getGrayLevel(imgPixel, newx, newy) == 0):
                                continue
                            if check[newx][newy] == 0:
                                check[newx][newy] = 1
                                queue.append((newx, newy))

                    allS = img.height * img.width
                    S = (x2 - x1) * (y2 - y1)
                    if (S / allS < 0.2):
                        continue
                    path = "region/"
                    if not os.path.exists(path):
                        os.makedirs(path)
                    img.crop((x1, y1, x2 + 1, y2 + 1)).save(path + "new" + str(x) + "-" + str(y) + ".png")
                    list.append({
                        'x1': x1,
                        'x2': x2,
                        'y1': y1,
                        'y2': y2
                    })
        print(list)





    def __init__(self):
        self.grayPoint = 100

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
        return Image.open('scaledImage.png')

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
        self.createCroppedDic()
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
                    # for i in range(1, 10000):
                    #     if (os.path.isfile(path + "new" + str(i) + ".png")):
                    #         os.remove(path + "new" + str(i) + ".png")
                    self.img.crop((self.x1, self.y1, self.x2 + 1, self.y2 + 1)).save(self.path + "new" + str(groupCnt) + ".png")
                    listCroppedImage.append({
                        'filepath': self.path + "new" + str(groupCnt) + ".png",
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

    
    def getBlack(self, x1, y1, x2, y2):
        dem = 0
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                color2 = self.imgPixel[x, y]
                gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
                if gray_level == 0:
                    dem = dem + 1
        return dem
                

    def checkRectWhite(self, x1, y1, x2, y2):
        return self.getBlack(x1, y1, x1, y2) == 0 and self.getBlack(x2, y1, x2, y2) == 0 and self.getBlack(x1, y1, x2, y1) == 0 and self.getBlack(x1, y2, x2, y2) == 0

    def getDetectedWordsVer2(self, imagePath, isScale = False):
        # img = Image.open(imagePath)
        img = self.resizeImage(imagePath, 500)
        img = self.toBinaryImage('scaledImage.png')
        # img.putpixel((1, 1), (0, 0, 0))
        img.save('test.png')
        imgPixel = img.load()
        self.imgPixel = imgPixel
        # summ = self.create2DArray(img.width, img.height)
        # for i in range(0, img.width):
        #     color2 = imgPixel[i, 0]
        #     gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
        #     summ[i][0] = gray_level / 255
            
        # for j in range(0, img.height):
        #     color2 = imgPixel[0, j]
        #     gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
        #     summ[0][j] = gray_level / 255

        # print(summ)

        # for i in range(1, img.width):
        #     for j in range(1, img.height):
        #         color2 = imgPixel[i, j]
        #         gray_level = 0.299 * color2[0] + 0.587 * color2[1] + 0.114 * color2[2]
        #         summ[i][j] = summ[i - 1][j] + summ[i][j - 1] - summ[i - 1][j - 1] + gray_level / 255

        # print(summ)

        # print(self.getBlack(sum, 0, 0, 10, 10))
        for x1 in range(0, img.width):
            for y1 in range(0, img.height):
                for x2 in range(x1 + 1, img.width):
                    for y2 in range(y1 + 1, img.height):
                        # if self.checkRectWhite(x1, y1, x2, y2) and self. getBlack(x1, y1, x2, y2) > 0:
                        #     # print(x1, y1, x2, y2)
                        a = 5




# obj = DetextText()
# obj.resizeImage("test01.jpg", 500)
# print(obj.getDetectedWords("scaledImage.png"))
