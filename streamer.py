from multiprocessing import Queue
import cv2 as cv


class Streamer:
    def __init__(self, video_path: str, q: Queue):
        self.video_path = video_path
        self.q = q

    def start(self):
        cap = cv.VideoCapture(self.video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                self.q.put('NO_MORE_FRAMES')
                break
            gray = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            self.q.put(gray)
            if cv.waitKey(1) == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()


def start_streaming(video_path: str, q: Queue):
    streamer = Streamer(video_path, q)
    streamer.start()
