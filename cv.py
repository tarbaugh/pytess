from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import numpy as np
import pytesseract
import argparse
import glob
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("-T", "--type", help="Specify file type without '.', ex. 'tiff', 'jpeg'", default="tiff")
args = parser.parse_args()

LANGUAGE = 'english'
SENTENCES_COUNT = 10
IMAGE_PATH = 'Images/*.{0}'.format(args.type)

images = sorted(glob.glob(IMAGE_PATH))
drawing = False
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

class Points:
    def __init__(self):
        self.points = []

    def get_point(self,event,x,y,flags,param):
        global X1, Y1, drawing

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            X1, Y1 = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                copy = img.copy()
                cv2.rectangle(copy,(X1,Y1),(x,y),(255,0,0), 3)
                cv2.imshow('image', copy)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            if x != X1 & y != Y1:
                cv2.rectangle(img, (X1,Y1), (x,y), (255, 0, 0), 3)
                cv2.imshow('image',img)
                self.points.append(((X1, Y1), (x, y)))

curr_points = Points()
fullstring = ''

for i in images:
    img = cv2.imread(i)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', curr_points.get_point)
    cv2.resizeWindow('image', 800, 800)
    while True:
        cv2.imshow('image',img)
        k = cv2.waitKey(0) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

    print('Selected Coordinates: ')

    crops = []
    for i in curr_points.points:
        if i[0][0] <= i[1][0]:
            x1_val = i[0][0]
            x2_val = i[1][0]
        else:
            x1_val = i[1][0]
            x2_val = i[0][0]
        if i[0][1] <= i[1][1]:
            y1_val = i[0][1]
            y2_val = i[1][1]
        else:
            y1_val = i[1][1]
            y2_val = i[0][1]
        crops.append(img[y1_val:y2_val,x1_val:x2_val].copy())
        print(i)

    if len(crops) > 0:
        for i in crops:
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('image', 600, 600)
            while True:
                cv2.imshow('image',i)
                k = cv2.waitKey(0) & 0xFF
                if k == 27:
                    break
        cv2.destroyAllWindows()

    for i in crops:
        img_new = Image.fromarray(i)
        text = pytesseract.image_to_string(img_new, lang='eng')
        fullstring += text

    curr_points = Points()

parser = PlaintextParser.from_string(fullstring, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)
