import pickle
import numpy as np
import random
import cv2 as cv
import os
# data image augmentation
# transfer learning

data_dir = "Photos/Dataset/"
labels = ["1RON", "5RON", "10RON", "50RON", "100RON", "200RON", "500RON"]
training_data = []

IMG_WIDTH = 220
IMG_HEIGHT = 115

def create_Dataset():
    print("Fetching images for dataset...")
    for label in labels:
        path = os.path.join(data_dir, label)
        for file_name in os.listdir(path):
            if file_name == ".DS_Store":  # automatic file that macOS generates, we skip this
                continue
            img = cv.imread(os.path.join(path, file_name))
            img = cv.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            label_integer = int(label[:label.index("R")])
            training_data.append([img, label_integer])
    random.shuffle(training_data)
    # print(len(training_data))

    X = []
    y = []

    for img, label in training_data:
        X.append(img)
        y.append(label)

    X = np.array(X).reshape(-1, IMG_WIDTH, IMG_HEIGHT, 3)
    y = np.array(y)

    X = X / 255.0

    pickle_X = open("X.pickle", "wb")
    pickle.dump(X, pickle_X)
    pickle_X.close()

    pickle_y = open("y.pickle", "wb")
    pickle.dump(y, pickle_y)
    pickle_y.close()

    print("Dataset containing {} images created successfully!\n".format(len(X)))