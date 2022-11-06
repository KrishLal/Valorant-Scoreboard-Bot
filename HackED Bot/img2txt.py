from PIL import Image, ImageFilter, ImageEnhance
from pytesseract import pytesseract
import re

#NOTE: May not always work
pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
#path_to_image = 'C:/Users/Amogh Panhale/Desktop/picture2.jpg'
def process(path_to_image):
    img = Image.open(path_to_image).convert('HSV')
    img = img.resize((1920,1080))
    # Split channels, just retaining the Value channel
    _, _, V = img.split()

    # Select pixels where V>220
    res = V.point(lambda p: p > 210 and 255)
    # res.save('result-pre.png')
    res = res.crop((382, 340, 1555 , 880))
    res = res.resize((round(res.size[0]*2), round(res.size[1]*2)))
    # res.save('result-resized.png')
    res = res.filter(ImageFilter.GaussianBlur(radius = 1))
    # res.save('result-gausian.png')

    enhancer = ImageEnhance.Contrast(res)

    factor = 1.5 #increase contrast
    res = enhancer.enhance(factor)

    left_x = 0
    left_y = 30
    right_x = 1200
    right_y = 130
    players = []
    for i in range(10):
        temp = res.crop((left_x, left_y, right_x-600, right_y))
        temp2 = res.crop((800, left_y, right_x, right_y))
        players.append([temp, temp2])
        # temp.save(str(i)+"_name.png")
        # temp2.save(str(i)+"_kda.png")
        left_y += 100
        right_y += 100



    pytesseract.run_tesseract.tesseract_cmd = 'C:/OCR/Tesseract-OCR/tesseract.exe'
    kd_dict = {}
    for i in range(10):
        name = pytesseract.image_to_string(players[i][0])
        kda = pytesseract.image_to_string(players[i][1])
        kd = kda.split(" ")
        kd = re.split(r'(\d+)', kda)
        temp = []
        name = name.strip()
        for i in kd:
            if i.isdigit():
                temp.append(i.strip())
        kd = temp

        kd_dict[name] = kd

    return(kd_dict)


