import time

import cv2

from resources.constants.commonConstants import *
from resources.constants.uriConstants import *


def faceDetector(names):
    if not names:
        return failed
    face_cascade = cv2.CascadeClassifier(cascadeClassifierDir)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    while True:
        for name in names:
            recognizer.read(f"{classifierWriteDir}{name}{classifierPostfix}")
            cap = cv2.VideoCapture(0)
            pred = 0
            timeout = 6  # [seconds]
            timeout_start = time.time()
            while True:
                ret, frame = cap.read()
                # default_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                """ @note: change scaleFactor (param2) and minNeighbours(param3) and check confidence level"""
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:

                    roi_gray = gray[y:y + h, x:x + w]

                    id, confidence = recognizer.predict(roi_gray)
                    confidence = 100 - int(confidence)
                    pred = 0
                    print("current confidence>>>>", confidence)

                    """ @note: decrese this value for confidence check.
                        @note: Please note this will enable face detection easily. But less accurately"""
                    if confidence > 65:
                        pred += +1
                        text = name.upper()
                        font = cv2.FONT_HERSHEY_PLAIN
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        frame = cv2.putText(frame, text, (x, y - 4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)
                        print("detected! confidence level: " + str(confidence))

                    else:
                        pred += -1
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                cv2.imshow(messageBoxTitle + " - " + faceDetecting, frame)
                key = cv2.waitKey(1) & 0xFF

                if pred > 0:
                    time.sleep(3)
                    cap.release()
                    cv2.destroyAllWindows()
                    return name

                if time.time() > timeout_start + timeout:
                    cap.release()
                    break
