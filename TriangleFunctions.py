from cv2 import *
import math
import numpy as np
import itertools


def getPointsFromLines(lines):
    points = []
    for i in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            points.append((x1, y1))
            points.append((x2, y2))
    return points


# draws a green triangle on a black and white img
# img is a binary image
def drawTriangle(img, p1, p2, p3):
    h = img.shape[0]
    w = img.shape[1]
    dst = np.zeros((h, w, 3), np.uint8)

    for y in range(0, h):
        for x in range(0, w):
            if img[y, x] == 0:
                dst[y, x] = (0, 0, 0)
            else:
                dst[y, x] = (255, 255, 255)

    line(dst, p1, p2, (0, 255, 0), 2)
    line(dst, p1, p3, (0, 255, 0), 2)
    line(dst, p3, p2, (0, 255, 0), 2)

    # imshow("cloned", dst)
    return dst

# draws a red rectangle on img
# img is a BGR image
# head and p4 should be opposing points in the rectangle
def drawRectangle(img, head, p1, p2, p3, p4):
    if head == p1:
        line(img, head, p2, (0, 0, 255), 2)
        line(img, head, p3, (0, 0, 255), 2)
        line(img, p4, p2, (0, 0, 255), 2)
        line(img, p4, p3, (0, 0, 255), 2)
    elif head == p2:
        line(img, head, p1, (0, 0, 255), 2)
        line(img, head, p3, (0, 0, 255), 2)
        line(img, p4, p1, (0, 0, 255), 2)
        line(img, p4, p3, (0, 0, 255), 2)
    elif head == p3:
        line(img, head, p2, (0, 0, 255), 2)
        line(img, head, p1, (0, 0, 255), 2)
        line(img, p4, p2, (0, 0, 255), 2)
        line(img, p4, p1, (0, 0, 255), 2)

    return img

def distance2Points(point1, point2):
    dist = (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2
    return math.sqrt(dist)


def areaTriangle(p1, p2, p3):
    l12 = distance2Points(p1, p2)
    l13 = distance2Points(p1, p3)
    l23 = distance2Points(p2, p3)
    s = (l12 + l13 + l23) / 2  # semiperimeter
    return math.sqrt(s * (s - l12) * (s - l13) * (s - l23))  # heron's formula


# img = the initial black and white image with a green triangle
# calculates the ratio between white and black pixels within a drawn green triangle from the image
def whiteBlackRatioTriangle(img, p1, p2, p3):
    h = img.shape[0]
    w = img.shape[1]

    area = areaTriangle(p1, p2, p3)

    start_point = [0, 0]
    start_point[0] = (p1[0] + p2[0] + p3[0]) / 3
    start_point[1] = (p1[1] + p2[1] + p3[1]) / 3  # we start from the triangle's center of gravity

    neighbours = [start_point]
    visited = np.zeros((h, w), dtype=int)
    white_pixels = 0
    dx = [0, 0, 1, 1, 1, -1, -1, -1]
    dy = [1, -1, 0, 1, -1, 0, 1, -1]

    test_img = np.zeros((h, w, 3), np.uint8)
    tested_pixels = 0
    while len(neighbours) != 0:
        point = neighbours.pop()

        # get the coordinates of the point and mark it as visited
        x = int(point[0])
        y = int(point[1])
        test_img[y, x] = (255,255,255)
        tested_pixels += 1

        if img[y, x][0] == 255 and img[y, x][1] == 255 and img[y, x][2] == 255 and visited[y, x] == 0:
            white_pixels += 1
        visited[y, x] = 1
        for k in range(0, 8):
            if visited[y + dy[k], x + dx[k]] == 0:
                # if the pixel is green => just mark it as visited
                if img[y + dy[k], x + dx[k]][1] == 255 \
                        and img[y + dy[k], x + dx[k]][2] == 0 \
                        and img[y + dy[k], x + dx[k]][0] == 0:
                    visited[y + dy[k], x + dx[k]] = 1
                else:
                    point2 = [0, 0]
                    point2[0] = x + dx[k]
                    point2[1] = y + dy[k]
                    neighbours.append(point2)

    # print("Pixeli albi: " + str(white_pixels))
    # print("Aria: " + str(area))
    # print("Pixeli testati " + str(tested_pixels))
    # imshow("TEST", test_img)
    return white_pixels / area

def approx_equal(p1, p2):
    if p1 * 0.97 <= p2 <= p1 * 1.03:
        return True
    return False

def approx_equalPoints(p1, p2):
    if p1[0] * 0.9 < p2[0] < p1[0] * 1.1:
        if p1[1] * 0.9 < p2[1] < p1[1] * 1.1:
            return True
    return False

def checkIfSameTriangle(t1, t2):
    a1 = areaTriangle(t1[0], t1[1], t1[2])
    a2 = areaTriangle(t2[0], t2[1], t2[2])
    if approx_equal(a1, a2) and (approx_equalPoints(t1[0], t2[0])
                                 or approx_equalPoints(t1[0], t2[1])
                                 or approx_equalPoints(t1[0], t2[2])):
        return True
    return False

# img = the initial black and white image
def chooseBestTriangle(initial_image, img, triangles, program_mode):

    ratio_max = 0
    best_triangles = []
    ratio = []

    for tr1, tr2 in itertools.combinations(triangles, 2):
        if tr2 in triangles:
            if checkIfSameTriangle(tr1, tr2):
                triangles.remove(tr2)

    n_triangles = len(triangles)
    print("Triunghiuri ramase dupa filtrare: " + str(n_triangles))
    for i in range(0, n_triangles):
        point1 = triangles[i][0]
        point2 = triangles[i][1]
        point3 = triangles[i][2]
        bw_triangle_image = drawTriangle(img, point1, point2, point3)
        ratio.append(whiteBlackRatioTriangle(bw_triangle_image, point1, point2, point3))  # ratio = white pixels / area
        # print(ratio[i])
        if ratio[i] > ratio_max:
            ratio_max = ratio[i]

    score_max = 0
    final_triangle = None
    # pick the top 15% ratio triangles
    for i in range(0, n_triangles):
        if ratio[i] >= 0.85 * ratio_max:
            best_triangles.append(triangles[i])
            area = areaTriangle(triangles[i][0], triangles[i][1], triangles[i][2])
            score = area / 5 + ratio[i] * 50000
            print("Triangle's white & black ratio is " + str(ratio[i]))
            print("Triangle's overall score is " + str(score))
            print("Triangle's area is " + str(area))
            print()
            if score >= score_max:
                score_max = score
                final_triangle = triangles[i]
                print("Picked triangle with ratio: " + str(ratio[i]))

    if program_mode == 2:
        # draw the best triangles on the initial image
        triangles_image = drawTriangles(initial_image, best_triangles)
        imshow("found_triangles", triangles_image)

    return final_triangle

# thresh = % of error accepted when calculating pythagoras
# all triangles must have edges of at least a fourth of the image's height in length and respect Pythagoras theorem
def checkIfRightTriangle(point1, point2, point3, thresh, image_height):
    line12 = distance2Points(point1, point2)
    line13 = distance2Points(point1, point3)
    line23 = distance2Points(point2, point3)

    # if line12 < 200 or line13 < 200 or line23 < 200:
    #     return False

    min_edge_length = image_height / 4
    if line12 < min_edge_length or line13 < min_edge_length or line23 < min_edge_length:
        return False

    # line12 & line 13 catete
    if line23**2 * (100 - thresh)/100 < line12**2 + line13**2 < line23**2 * (100 + thresh)/100:
        return True
    # line12 & line 23 catete
    if line13**2 * (100 - thresh)/100 < line23**2 + line12**2 < line13**2 * (100 + thresh)/100:
        return True
    # line13 & line 23 catete
    if line12**2 * (100 - thresh)/100 < line13**2 + line23**2 < line12**2 * (100 + thresh)/100:
        return True

    return False


def getTrianglesFromPoints(points, thresh, image_height):
    n = len(points)
    no_of_triangles = 0
    triangles_list = []
    for i in range(0, n-2):
        for j in range(i+1, n-1):
            for k in range(j+1, n):
                if checkIfRightTriangle([points[i][0], points[i][1]],
                                        [points[j][0], points[j][1]],
                                        [points[k][0], points[k][1]],
                                        thresh,
                                        image_height):
                    no_of_triangles += 1
                    triangles_list.append([points[i],
                                           points[j],
                                           points[k]])
    return triangles_list, no_of_triangles, thresh


def drawTriangles(img, triangles):
    len_triangles = len(triangles)
    for i in range(0, len_triangles):
        line(img, triangles[i][0], triangles[i][1], (0, 255, 0), 3)
        line(img, triangles[i][0], triangles[i][2], (255, 0, 0), 3)
        line(img, triangles[i][1], triangles[i][2], (0, 0, 255), 3)
    return img

# determines which of the 3 points is associated with the right angle
# the hypotenuse is the largest line in a square triangle
def getRightAnglePoint(p1, p2, p3):
    l12 = distance2Points(p1, p2)
    l13 = distance2Points(p1, p3)
    l23 = distance2Points(p2, p3)
    if l12 > l13 and l12 > l23:
        return 2
    if l13 > l12 and l13 > l23:
        return 1
    return 0

def getFourthPoint(head, point1, point2, point3):
    p2 = point2
    p3 = point3
    if head == point2:
        p2 = point1
        p3 = point3
    else:
        if head == point3:
            p2 = point1
            p3 = point2
    offsetX = head[0] - p2[0]
    offsetY = head[1] - p2[1]
    x = p3[0] - offsetX
    y = p3[1] - offsetY
    p4 = (x, y)
    return p4

def order3numbers(n1, n2, n3):
    if n1 > n2 > n3:
        return 123
    elif n1 > n3 > n2:
        return 132
    elif n2 > n1 > n3:
        return 213
    elif n2 > n3 > n1:
        return 231
    elif n3 > n1 > n2:
        return 312
    elif n3 > n2 > n1:
        return 321

# calculates the angle needed for rotating the image so that the rectangle is not tilted
# linia pX -> p4 va fi cea pt care calculam panta, aceasta e a 2a cea mai mare linie din dreptunghi, dupa diagonala
# functia returneaza arctangenta pantei acestei linii, care este unghiul cu care va trebui rotita imaginea
# pentru ca bancnota sa fie orizontala
def getRotationAngle(p1, p2, p3, p4):
    l1 = distance2Points(p1, p4)
    l2 = distance2Points(p2, p4)
    l3 = distance2Points(p3, p4)
    order = order3numbers(l1, l2, l3)
    slope = 0
    # l2
    if order == 123 or order == 321:
        slope = (p2[1] - p4[1]) / (p2[0] - p4[0])
    # l3
    elif order == 132 or order == 231:
        slope = (p3[1] - p4[1]) / (p3[0] - p4[0])
    # l1
    elif order == 213 or order == 312:
        slope = (p1[1] - p4[1]) / (p1[0] - p4[0])
    return math.degrees(math.atan(slope))







