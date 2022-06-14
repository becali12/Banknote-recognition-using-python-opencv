from TriangleFunctions import *
from Filters import *
import os
import matplotlib.pyplot as plt
import sys


# limit = the number of photos read
def readPhotosFromFolder(folder, limit):
    images = []
    names = []
    count = 0
    for filename in os.listdir(folder):
        if count != limit:
            img = imread(os.path.join(folder, filename))
            if img is not None:
                names.append(filename)
                # images.append(resizePhotoExact(img, 900, 900))
                images.append(resizePhotoExact(img, 1000, 1000))
            count += 1
    return images, names


def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = getRotationMatrix2D(center, angle, scale)
    rotated = warpAffine(image, M, (w, h))

    return rotated


def max4numbers(n1, n2, n3, n4):
    if n1 >= n2 and n1 >= n3 and n1 >= n4:
        return n1
    if n2 >= n1 and n2 >= n3 and n2 >= n4:
        return n2
    if n3 >= n1 and n3 >= n2 and n3 >= n4:
        return n3


def min4numbers(n1, n2, n3, n4):
    if n1 <= n2 and n1 <= n3 and n1 <= n4:
        return n1
    if n2 <= n1 and n2 <= n3 and n2 <= n4:
        return n2
    if n3 <= n1 and n3 <= n2 and n3 <= n4:
        return n3


def cropImg(img, xmin, xmax, ymin, ymax):
    croppedImg = img[ymin:ymax, xmin:xmax]
    return croppedImg


# searches for the 4 points of the red rectangle in an image, starting from the middle of the image
# basically finds the position of the banknote in the picture
def findCroppingPoints(img):
    h = img.shape[0]
    w = img.shape[1]
    middle_w = int(w / 2)
    i = 0
    found = False
    ymin = ymax = xmin = xmax = 0
    while i < h and found is False:
        if img[i, middle_w][2] == 255 and img[i, middle_w][1] == img[i, middle_w][0] == 0:
            found = True
            ymin = i
        i += 1
    i = h - 1
    found = False
    while i >= 0 and found is False:
        if img[i, middle_w][2] == 255 and img[i, middle_w][1] == img[i, middle_w][0] == 0:
            found = True
            ymax = i
        i -= 1
    x = 0
    found = False
    while x < w and found is False:
        y = 0
        while y < h:
            if img[y, x][2] == 255 and img[y, x][0] == img[y, x][1] == 0:
                found = True
                xmin = x
            y += 1
        x += 1
    x = w - 1
    found = False
    while x >= 0 and found is False:
        y = 0
        while y < h:
            if img[y, x][2] == 255 and img[y, x][0] == img[y, x][1] == 0:
                found = True
                xmax = x
            y += 1
        x -= 1

    return xmin, xmax, ymin, ymax

# not in use
def compareHSV(initialImage):
    i1 = imread("DefaultPhotos/1.jpg")
    i5 = imread("DefaultPhotos/5.jpg")
    i10 = imread("DefaultPhotos/10.jpg")
    i50 = imread("DefaultPhotos/50.jpg")
    i100 = imread("DefaultPhotos/100.jpg")
    i200 = imread("DefaultPhotos/200.jpg")
    i500 = imread("DefaultPhotos/500.jpg")

    initialImage = resizePhotoExact(initialImage, 300, 400)
    i1 = resizePhotoExact(i1, 300, 400)
    i5 = resizePhotoExact(i5, 300, 400)
    i10 = resizePhotoExact(i10, 300, 400)
    i50 = resizePhotoExact(i50, 300, 400)
    i100 = resizePhotoExact(i100, 300, 400)
    i200 = resizePhotoExact(i200, 300, 400)
    i500 = resizePhotoExact(i500, 300, 400)
    initialImage = cvtColor(initialImage, COLOR_BGR2HSV)
    i1 = cvtColor(i1, COLOR_BGR2HSV)
    i5 = cvtColor(i5, COLOR_BGR2HSV)
    i10 = cvtColor(i10, COLOR_BGR2HSV)
    i50 = cvtColor(i50, COLOR_BGR2HSV)
    i100 = cvtColor(i100, COLOR_BGR2HSV)
    i200 = cvtColor(i200, COLOR_BGR2HSV)
    i500 = cvtColor(i500, COLOR_BGR2HSV)

    hist = calcHist([initialImage], [0], None, [256], [0, 180])
    h1 = calcHist([i1], [0], None, [256], [0, 180])
    h2 = calcHist([i5], [0], None, [256], [0, 180])
    h3 = calcHist([i10], [0], None, [256], [0, 180])
    h4 = calcHist([i50], [0], None, [256], [0, 180])
    h5 = calcHist([i100], [0], None, [256], [0, 180])
    h6 = calcHist([i200], [0], None, [256], [0, 180])
    h7 = calcHist([i500], [0], None, [256], [0, 180])

    print(compareHist(hist, h1, HISTCMP_INTERSECT))
    print(compareHist(hist, h2, HISTCMP_INTERSECT))
    print(compareHist(hist, h3, HISTCMP_INTERSECT))
    print(compareHist(hist, h4, HISTCMP_INTERSECT))
    print(compareHist(hist, h5, HISTCMP_INTERSECT))
    print(compareHist(hist, h6, HISTCMP_INTERSECT))
    print(compareHist(hist, h7, HISTCMP_INTERSECT))

    imshow("500", i500)
    imshow("50", i50)
    imshow("100", i100)

# not in use
def compareBGR(initialImage):
    i1 = imread("DefaultPhotos/1.jpg")
    i5 = imread("DefaultPhotos/5.jpg")
    i10 = imread("DefaultPhotos/10.jpg")
    i50 = imread("DefaultPhotos/50.jpg")
    i100 = imread("DefaultPhotos/100.jpg")
    i200 = imread("DefaultPhotos/200.jpg")
    i500 = imread("DefaultPhotos/500.jpg")

    initialImage = resizePhotoExact(initialImage, 300, 600)
    i1 = resizePhotoExact(i1, 300, 600)
    i5 = resizePhotoExact(i5, 300, 600)
    i10 = resizePhotoExact(i10, 300, 600)
    i50 = resizePhotoExact(i50, 300, 600)
    i100 = resizePhotoExact(i100, 300, 600)
    i200 = resizePhotoExact(i200, 300, 600)
    i500 = resizePhotoExact(i500, 300, 600)

    hist = calcHist([initialImage], [0, 1, 2], None, [128, 128, 128], [0, 256, 0, 256, 0, 256])
    h1 = calcHist([i1], [0, 1, 2], None, [128, 128, 128], [0, 256, 0, 256, 0, 256])
    h2 = calcHist([i5], [0, 1, 2], None, [128, 128, 128], [0, 256, 0, 256, 0, 256])
    h3 = calcHist([i10], [0, 1, 2], None, [128, 128, 128], [0, 256, 0, 256, 0, 256])
    h4 = calcHist([i50], [0, 1, 2], None, [128, 128, 128], [0, 256, 0, 256, 0, 256])
    h5 = calcHist([i100], [0, 1, 2], None, [128, 128, 128], [0, 256, 0, 256, 0, 256])
    h6 = calcHist([i200], [0, 1, 2], None, [128, 128, 128], [0, 256, 0, 256, 0, 256])
    h7 = calcHist([i500], [0, 1, 2], None, [128, 128, 128], [0, 256, 0, 256, 0, 256])

    print(compareHist(hist, h1, HISTCMP_INTERSECT))
    print(compareHist(hist, h2, HISTCMP_INTERSECT))
    print(compareHist(hist, h3, HISTCMP_INTERSECT))
    print(compareHist(hist, h4, HISTCMP_INTERSECT))
    print(compareHist(hist, h5, HISTCMP_INTERSECT))
    print(compareHist(hist, h6, HISTCMP_INTERSECT))
    print(compareHist(hist, h7, HISTCMP_INTERSECT))

    imshow("500", i500)
    imshow("50", i50)
    imshow("100", i100)
    imshow("5", i5)

    # hist = calcHist([initialImage], [0,1], None, [128,128], [0, 256,0, 256])
    # h1 = calcHist([i1], [0,1], None, [128,128], [0, 256,0, 256])
    # h2 = calcHist([i5], [0,1], None, [128,128], [0, 256,0, 256])
    # h3 = calcHist([i10], [0,1], None, [128,128], [0, 256,0, 256])
    # h4 = calcHist([i50], [0,1], None, [128,128], [0, 256,0, 256])
    # h5 = calcHist([i100], [0,1], None, [128,128], [0, 256,0, 256])
    # h6 = calcHist([i200], [0,1], None, [128,128], [0, 256,0, 256])
    # h7 = calcHist([i500], [0,1], None, [128,128], [0, 256,0, 256])


def compareORB(initialImage, testImages, names, program_mode):
    most_matches = 0
    bestTestImage = []
    best_kp1 = []
    best_kp2 = []
    best_matches = []
    for i in range(len(testImages)):
        testImage = testImages[i]
        # testImage = cvtColor(resizePhotoExact(testImage, 300, 600), COLOR_BGR2GRAY)
        # cvtColor(initialImage, COLOR_BGR2GRAY, initialImage)
        testImage = resizePhotoExact(testImage, 300, 570)
        orb = ORB_create()
        kp1, des1 = orb.detectAndCompute(initialImage, None)
        kp2, des2 = orb.detectAndCompute(testImage, None)

        bf = BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # sum_distances = 0
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:  # standard 0.75
                good.append([m])
                # sum_distances += m.distance

        if program_mode == 2:
            print("For image " + names[i] + " there are {} matches.".format(len(good)))

        if len(good) > most_matches:
            picture_name = names[i]
            most_matches = len(good)
            bestTestImage = testImage
            best_kp1 = kp1
            best_kp2 = kp2
            best_matches = good


    if bestTestImage is None:
        sys.exit("No matches found")
    img_matches = drawMatchesKnn(initialImage, best_kp1, bestTestImage, best_kp2, best_matches, None,
                                 flags=DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)


    result = picture_name[:picture_name.index("_")] + " RON"
    print("The result found is: " + result)
    return result, img_matches


def displayFinalResult(img, coord, result):
    putText(img, result, (coord[0], coord[1]), fontFace=FONT_HERSHEY_SIMPLEX, fontScale=2,
            color=(0, 0, 255), thickness=3, lineType=2)

    imshow("Final", img)
    waitKey(0)
