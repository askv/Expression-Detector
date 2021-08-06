from imutils.video import VideoStream
import face_recognition         #built using dlib for face recognition
import imutils                  #basic image processing functions( here used for resizing etc)
import pickle                   #used for serializing and de-serializing a Python object structure. Any object in Python can be pickled so that it can be saved on disk.
import time                       #time.sleep halts the execution of program
import cv2
from model import FacialExpressionModel
import numpy as np                  #for scientific computing(here while predicting)
from db import databaseclass

print("[INFO] loading encodings...")
data = pickle.loads(open("C:/Users/Deeksha/PycharmProjects/test2/encodings.pickle", "rb").read())
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

facec = cv2.CascadeClassifier("C:/Users/Deeksha/PycharmProjects/test2/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

db_obj = databaseclass()

while True:
    frame = vs.read()
    rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb=imutils.resize(rgb, width=750)
    r=frame.shape[1] / float(rgb.shape[1])
    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts={}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        names.append(name)
    for ((top, right, bottom, left), name) in zip(boxes, names):
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        id=name

        fc = gray[top:bottom, left:right]
        roi = cv2.resize(fc, (48, 48))
        pred = "unknown"
        pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
        y = top - 15 if (top - 15) > 15 else top + 15
        cv2.putText(frame, id, (left, y), font, 1, (0, 255, 0), 2)
        cv2.putText(frame, pred, (left+160, y), font, 1, (0, 255, 0), 2)
        cv2.imshow("Frame", frame)

    db_obj.update_db(pred,id)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()



