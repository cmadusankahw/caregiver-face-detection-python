import cv2
import os

from resources.constants.commonConstants import *
from resources.constants.uriConstants import *


def start_capture(name):
    path = datasetDir + name
    num_of_images = 0
    detector = cv2.CascadeClassifier(cascadeClassifierDir)
    try:
        os.makedirs(path)
    except:
        print('Directory Already Created')
    vid = cv2.VideoCapture(0)
    while True:

        ret, img = vid.read()
        new_img = None
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = detector.detectMultiScale(image=grayimg, scaleFactor=scaleFactorVal, minNeighbors=minNeighboursVal)
        for x, y, w, h in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Face Detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, str(str(num_of_images) + " images captured"), (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255))
            new_img = img[y:y + h, x:x + w]
        cv2.imshow(detectorTitle, img)
        key = cv2.waitKey(1) & 0xFF

        try:
            cv2.imwrite(str(path + "/" + str(num_of_images) + name + jpgType), new_img)
            num_of_images += 1
        except:

            pass
        if key == ord("q") or key == 27 or num_of_images > noOfImgToCapture:
            break
    cv2.destroyAllWindows()
    return num_of_images
