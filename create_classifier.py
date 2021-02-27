import numpy as np
from PIL import Image
import os, cv2

from resources.constants.uriConstants import *


# train custom classifier to recognize face
def train_classifer(name):
    # Read all the images in custom data-set
    path = os.path.join(os.getcwd() + classifierDataDir + name + "/")

    faces = []
    ids = []
    labels = []
    pictures = {}

    # Store images in a numpy array and ids of the user on the same index in imageNp and id lists

    for root, dirs, files in os.walk(path):
        pictures = files

    for pic in pictures:
        imgpath = path + pic
        img = Image.open(imgpath).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(pic.split(name)[0])
        # names[name].append(id)
        faces.append(imageNp)
        ids.append(id)

    ids = np.array(ids)

    # Train and save classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write(classifierWriteDir + name + classifierPostfix)
