from cv2 import *
import numpy as np
import sys
np.set_printoptions(threshold=np.inf)

def resizePhoto(img, scale_factor):
    dimensions = int(scale_factor / 100 * img.shape[0]), int(scale_factor / 100 * img.shape[1])
    return resize(img, dimensions)

def resizePhotoExact(img, h, w):
    dimensions = w, h
    return resize(img, dimensions)

# finds the average grayscale colour of the middle of the picture (the banknote)
# not in use at the moment
def getAverageGrayCoef(gray_img):
    h = gray_img.shape[0]
    w = gray_img.shape[1]
    y = int(h/2)
    x = int(w/2)

    suma = 0
    for i in range(0,20):
        suma += gray_img[y + i, x + i]

    return int(suma/20)



def binarize(img, inferior_thresh, superior_tresh):
    h = img.shape[0]
    w = img.shape[1]
    for y in range(0, h):
        for x in range(0, w):
            # if thresh < img[y, x] < 255:
            if inferior_thresh < img[y, x] < superior_tresh:
                img[y, x] = 255
            else:
                img[y, x] = 0
    return img


def Contours(img):
    edges = Canny(img, 50, 100, apertureSize=3)

    cnts = findContours(edges, RETR_TREE, CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    h = img.shape[0]
    w = img.shape[1]
    dst = np.zeros((h, w, 3), np.uint8)

    for c in cnts:
        drawContours(dst, [c], 0, (0, 255, 0), 1)

    return dst


def edgeDetection(img, program_mode):

    edges = Canny(img, 800, 1000, apertureSize=3)

    if program_mode == 2:
        imshow("Canny", edges)

    lines = HoughLinesP(edges, 1, np.pi / 180, threshold=120, minLineLength=200, maxLineGap=150)

    h = img.shape[0]
    w = img.shape[1]
    dst = np.zeros((h, w, 3), np.uint8)

    if lines is not None:
        lines_no = len(lines)
        for i in range(0, lines_no):
            for x1, y1, x2, y2 in lines[i]:
                line(dst, (x1, y1), (x2, y2), (0, 255, 0), 3)

        if program_mode == 2:
            imshow("edges", dst)

        return dst, lines
    else:
        sys.exit("No triangles found")

def applyFilters(img, program_mode):
    gray = GaussianBlur(img, (5, 5), BORDER_DEFAULT)
    gray = cvtColor(gray, COLOR_BGR2GRAY)
    # gray = binarize(gray, 100, 240)
    gray = binarize(gray, 130, 255)

    # average_colour = getAverageGrayCoef(gray)
    # print(average_colour)
    # gray = binarize(gray, 0.75 * average_colour, 1.25 * average_colour)

    kernel = np.ones((3,3), np.uint8)

    black_white = erode(gray, kernel, gray, iterations=5)

    gray = Contours(gray)  # finds contours using findCountours()
    gray, lines = edgeDetection(gray, program_mode)  # finds edges in the above generated image using houghP

    return gray, lines, black_white  # lines contains all the lines detected by the edgeDetection function

