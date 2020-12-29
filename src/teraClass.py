import pytesseract       
from PIL import Image     
import glob


path = "hinh/"
files = glob.glob(path+'*', recursive=True)

text = ""
for f in files:
    print(f)
    result = pytesseract.image_to_string(Image.open(f), lang='vie')   
    text += result

text = text.replace('\x0c',' ')
text = text.replace('\n',' ')
text = text.replace('\n',' ')
text = text.replace('\n',' ')
text = text.replace('\n',' ')
text = text.replace('  ',' ')
text = text.replace('  ',' ')
text = text.replace('  ',' ')
text = text.replace('  ',' ')
print(text)
list = text.split(' ')
print(list)
print(len(list))
file = open('words(sub05).txt', mode = 'w')
dem = 1
for element in list:
    file.write('sub05/sub05-' + str(dem) + ' X X X X X X ' + element + '\n') 
    dem = dem + 1

# img = Image.open('hinh/12.jpeg')                             
 