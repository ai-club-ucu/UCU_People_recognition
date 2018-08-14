import cv2
import numpy as np
from modules.utils import parse_datetime
from modules.config import *


class VideoProcessor:
    """Represents video and image processing."""

    def __init__(self, video_path="../assets/sample_3.avi"):
        """
        Subtracting background from the video frames and find contours on the
        original frame which could be a person in the queue.
        :string video_path: path to the video to process
        """
        self.stream = cv2.VideoCapture(video_path)
        self.video_time = parse_datetime(video_path)
        # self.background_subtractor = cv2.bgsegm.createBackgroundSubtractorMOG(
        #     history=1000)
        self.min_area = min_contour_area_to_be_a_person
        self.max_area = max_contour_area_to_be_a_person
        self.prev = None

    @staticmethod
    def crop_interesting_region(frame):
        """Crop specific frame region."""
        return frame[interesting_region_y_1:interesting_region_y_2,
               interesting_region_x_1:interesting_region_x_2]

    @staticmethod
    def leave_only_persons(frame, boxes):
        """
        Makes all areas without possible people black
        :ndarray frame: original frame from the video
        :list of (x,y,w,h) boxes: boxes suspected to have a person in
        :ndarray: frame_with_persons: frame with only suspected boxes to have person in
        """
        mask = np.zeros(frame.shape[:2], dtype="uint8")
        for x, y, w, h in boxes:
            mask[y:y + h, x:x + w] = 1

        frame_with_persons = cv2.bitwise_and(frame, frame, mask=mask)
        return frame_with_persons

    def process_frame(self, frame, preview=False, crop=False):
        """
        Subtract background from the video. Leaves only contours which can be a person
        :ndarray frame: frame of the video
        :boolean preview:
        :ndarray: processed_frame: frame with only possible persons in the queue
        """
        if crop:
            frame = self.crop_interesting_region(frame)

        original_frame = frame.copy()
        # frame = imutils.resize(frame, width=500)
        gray = self.prepare_frame(frame)

        if self.prev is None:
            self.prev = gray
            self.init_frame = gray.copy
            self.f_frame = original_frame

        self.thresh = thresh = self.compare_with_prev(gray)
        im2, contours, hierarchy = cv2.findContours(self.thresh,
                                                    cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_SIMPLE)

        good_boxes = []
        # loop over the contours
        for c in contours:
            if self.min_area < cv2.contourArea(c) < self.max_area:
                (x, y, w, h) = cv2.boundingRect(c)
                good_boxes.append((x, y, w, h))
                cv2.rectangle(
                    frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        processed_frame = self.leave_only_persons(
            original_frame, good_boxes)

        if preview:
            cv2.imshow('Only persons', processed_frame)
            cv2.imshow("gray", gray)
            cv2.imshow("thresh", thresh)

            # cv2.imshow("Dilated", cpp)
            # cv2.imshow("a", a)
            cv2.waitKey()

    def make_heatmap(self, frame, reset=None):
        """
        Make heatmap from prepared frame.

        :param frame: frame
        :param reset: reset heatmap or not
        :return: None
        """
        if self.prev is None:
            gray = self.prepare_frame(frame)
            self.prev = gray
            self.res = (0.05 * gray).astype(np.float64)
            self.compare_with_prev(gray)
        else:
            gray = self.prepare_frame(frame)
            if reset is not None:
                self.res = (0.05 * gray).astype(
                    np.float64) + self.prev_show * 3.0
            processed = self.compare_with_prev(gray)
            processed = processed.astype(np.float64)
            self.res += (40 * processed + gray) * 0.01
            show_res = (self.res) / self.res.max()
            show_res = np.floor(show_res * 255)
            self.prev_show = show_res
            show_res = show_res.astype(np.uint8)
            show_res = cv2.applyColorMap(show_res, cv2.COLORMAP_JET)
            cv2.imshow("res", show_res)

    def prepare_frame(self, frame):
        """
        Process frame to prepare for heatmap.

        :param frame: frame to prepare
        :return: None
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 2, 2)
        gray = self.adjust_gamma(gray, 1.5)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        return clahe.apply(gray)

    def compare_with_prev(self, frame):
        """
        Compare current frame with previous.

        :param frame: frame to compare with previous
        :return: frame with threshold
        """
        delta = cv2.absdiff(self.prev, frame)
        self.prev = frame
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (5, 5))
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        return closing

    def get_next_frame(self):
        """Gets next frame."""
        grabbed, frame = self.stream.read()
        return grabbed, frame

    def initialize(self, frame):
        """Copies the current frame"""
        self.init_frame = frame.copy()

    def show_video(self):
        """Plays the video."""
        grabbed, frame = self.get_next_frame()
        n = 0
        while grabbed:
            if n % 220 == 0:
                self.make_heatmap(frame, n)
            else:
                self.make_heatmap(frame)
            # self.process_frame(frame, preview=True, crop=False)
            cv2.imshow("frame", frame)
            grabbed, frame = self.get_next_frame()
            n += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def adjust_gamma(self, img, gamma=1.5):
        """Brightens the frame."""
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(img, table)


if __name__ == "__main__":
    vidya = VideoProcessor()
    vidya.show_video()
