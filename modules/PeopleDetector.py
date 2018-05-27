import cv2
import imutils
import numpy as np

from imutils.object_detection import non_max_suppression


class PeopleDetector:
    """Represents people recognition."""

    def __init__(self, detector_parameters):
        """Initializes people detector"""
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.parameters = detector_parameters

    def detect_people(self, img, preview=False):
        """
        :return: list of boundary boxes
        """
        img = imutils.resize(img, width=min(self.parameters["img_width"], img.shape[1]))

        (rects, weights) = self.hog.detectMultiScale(img, winStride=self.parameters["winStride"],
                                                     padding=self.parameters["padding"],
                                                     scale=self.parameters["scale"])

        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        if preview:
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv2.imshow("Detected people", img)
            cv2.waitKey()

        return pick

    def count_people(self, img):
        return len(self.detect_people(img))
