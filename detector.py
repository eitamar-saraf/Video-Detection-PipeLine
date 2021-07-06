from multiprocessing import Queue
import cv2 as cv
import imutils


class Detector:
    def __init__(self, min_area: int, frames_queue: Queue, processed_frames_queue: Queue):
        self.frames_queue = frames_queue
        self.min_area = min_area
        self.first_frame = None
        self.processed_frames_queue = processed_frames_queue

    def start(self, system_messages_queue: Queue):
        while True:
            frame = self.frames_queue.get()

            if isinstance(frame, str) and frame == "NO_MORE_FRAMES":
                system_messages_queue.put('Kill_Streamer')
                system_messages_queue.put('Kill_Detector')
                break

            if self.first_frame is None:
                self.first_frame = frame.copy()
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frame_delta = cv.absdiff(self.first_frame, frame)
            thresh = cv.threshold(frame_delta, 25, 255, cv.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv.dilate(thresh, None, iterations=2)
            cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv.contourArea(c) < self.min_area:
                    continue
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv.boundingRect(c)
                self.processed_frames_queue.put((frame, (x, y, w, h)))


def start_detector(min_area: int, frames_queue: Queue, processed_frames_queue: Queue, system_messages_queue: Queue):
    detector = Detector(min_area, frames_queue, processed_frames_queue)
    detector.start(system_messages_queue)
