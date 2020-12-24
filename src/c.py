import cv2
import os
import numpy as np
from cv2 import boundingRect, countNonZero, cvtColor, drawContours, findContours, getStructuringElement, imread, morphologyEx, pyrDown, rectangle, threshold
from indexClass import DetextText
import os
import glob

path = "region/"
files = glob.glob(path+'*.png', recursive=True)
for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))
if not os.path.exists(path):
    os.makedirs(path)


imagePath = "tho07.jpg"
width = 2000
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

image_path = "scaledImage.png"



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
        rgb = rectangle(rgb, (x, y+rect_height), (x+rect_width, y), (0,255,0),3)
        crop_img = rgb[y:y+rect_height, x:x+rect_width]
        # cv2.imshow("cropped", crop_img)
        
       
        dem = dem + 1
        cv2.imwrite(path + str(dem) + ".png", crop_img)
        # listDetectedWords = obj.getDetectedWords(path + str(dem) + ".png")
        # for element in listDetectedWords:
        #     text += element
        #     text += ' '
        # print(text)
        # cv2.waitKey(0)

print(text)
from PIL import Image
print(rgb)
Image.fromarray(rgb).show()