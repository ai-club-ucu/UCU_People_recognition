import cv2
import tensorflow as tf
from mtcnn.mtcnn import MTCNN

cap = cv2.VideoCapture("vid_2.avi")
detector = MTCNN()
n = 0
while True:
    ret, frame = cap.read()
    if n % 2 == 0:
        faces = detector.detect_faces(frame)
        for face in faces:
            cv2.rectangle(frame, (face['box'][0], face['box'][1]),
                          (face['box'][0] + face['box'][2],
                           face['box'][1] + face['box'][3]), (255, 0, 0), 2)
    cv2.imshow('frame', frame)
    n += 1
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()