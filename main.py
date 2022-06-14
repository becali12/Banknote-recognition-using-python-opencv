from ImageFunctions import *
from Dataset import *
from NeuralNetwork import *


def getTestImages():
    testImages, file_names = readPhotosFromFolder("DefaultPhotos/", 48)
    return testImages, file_names

def init():
    print("\nHow would you like to run this program?\n"
          "1: show only final result \n"
          "2: show all steps taken to achieve the result")
    program_mode = int(input())
    while program_mode < 1 or program_mode > 2:
        print("Please enter a valid input\n")
        print("How would you like to run this program?\n"
              "1: show only final result \n"
              "2: shown all steps taken to achieve the result")
        program_mode = int(input())

    print("\nWhich feature detection method would you like me to use?\n"
          "1: ORB algorithm\n"
          "2: Neural Network")
    detection_mode = int(input())

    while detection_mode < 1 or detection_mode > 2:
        print("\nWhich feature detection method would you like me to use?\n"
              "1: ORB algorithm\n"
              "2: Neural Network")
        detection_mode = int(input())

    return program_mode, detection_mode


def start():
    program_mode, detection_mode = init()
    images, names = readPhotosFromFolder("Photos/test_images/", 25)
    for i in range(len(images)):
        img = images[i]
        print("Opening " + names[i])
        main(img, program_mode, detection_mode)

def main(img, program_mode, detection_mode):

    image_height = img.shape[0]
    imshow("Initial", img)
    initial = img.copy()

    initialImage = img
    img, lines, black_white = applyFilters(img, program_mode)

    if program_mode == 2:
        imshow("black", black_white)

    points = getPointsFromLines(lines)
    triangles, no_of_triangles, thresh = getTrianglesFromPoints(points, 1, image_height)

    while no_of_triangles < 10:
        triangles, no_of_triangles, thresh = getTrianglesFromPoints(points, thresh+1, image_height)

    while no_of_triangles > 20:
        triangles, no_of_triangles, thresh = getTrianglesFromPoints(points, thresh * 0.8, image_height)

    aux_initial_image = initialImage.copy()
    triangle = chooseBestTriangle(aux_initial_image, black_white, triangles, program_mode)
    headOfTriangle = triangle[getRightAnglePoint(triangle[0], triangle[1], triangle[2])]
    fourthPoint = getFourthPoint(headOfTriangle, triangle[0], triangle[1], triangle[2])

    initialImage = drawRectangle(initialImage, headOfTriangle, triangle[0], triangle[1], triangle[2], fourthPoint)

    angle = getRotationAngle(triangle[0], triangle[1], triangle[2], fourthPoint)

    initialImage = rotate(initialImage, angle)
    initial = rotate(initial, angle)

    if program_mode == 2:
        imshow("Detected", initialImage)
    imageToWriteResultOn = initialImage

    xmin, xmax, ymin, ymax = findCroppingPoints(initialImage)
    initialImage = cropImg(initial, xmin, xmax, ymin, ymax)

    coordinatesToWriteResultAt = [int(xmax - 200), int(ymin - 20)]

    result = "No result"
    if detection_mode == 1:
        testImages, file_names = getTestImages()
        result, img_matches = compareORB(initialImage, testImages, file_names, program_mode)

        if program_mode == 2:
            imshow("Matches", img_matches)
        print("done with an image \n")

    elif detection_mode == 2:
        result = predict_banknote_NN(initialImage)
        print("Result found by the Neural Network: " + result)

    displayFinalResult(imageToWriteResultOn, coordinatesToWriteResultAt, result)

    return initialImage


# create_Dataset()
# create_Model()
start()





























