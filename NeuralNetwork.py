from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import pickle
import numpy as np
import cv2 as cv
from Dataset import IMG_WIDTH, IMG_HEIGHT, labels

model = load_model("banknote_model.model")

def create_Model():
    X = pickle.load(open("X.pickle", "rb"))
    y = pickle.load(open("y.pickle", "rb"))

    # converts labels to 0...6 values instead of 1 5 10 100 200 500
    LE = LabelEncoder().fit(y)
    y = LE.transform(y)

    y = to_categorical(y, num_classes=7)

    model = Sequential()
    model.add(Conv2D(64, (3,3), input_shape=X.shape[1:]))
    model.add(Activation("relu"))
    model.add(MaxPooling2D())

    model.add(Conv2D(64, (3,3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D())

    model.add(Flatten())
    model.add(Dense(64))

    model.add(Dense(7))
    model.add(Activation('softmax'))

    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(X, y, batch_size=32, validation_split=0.2, epochs=15)

    # print(model.summary())
    model.save("banknote_model.model")

def predict_banknote_NN(img):
    img = cv.resize(img, (IMG_WIDTH, IMG_HEIGHT))

    X = [img]
    X = np.array(X).reshape(-1, IMG_WIDTH, IMG_HEIGHT, 3)
    X = X / 255

    prediction = np.argmax(model.predict(X))
    return labels[prediction]





