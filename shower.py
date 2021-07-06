from multiprocessing import Queue
import cv2 as cv


class Shower:
    def __init__(self, video_path: str, processed_frames_queue: Queue):
        cap = cv.VideoCapture(video_path)
        fps = int(cap.get(cv.CAP_PROP_FPS))
        cap.release()
        self.fps = int(fps)
        self.wait_time = int(1000 / self.fps)
        self.processed_frames_queue = processed_frames_queue

    def start(self, system_messages_queue: Queue):
        while True:
            proc_frame = self.processed_frames_queue.get()
            if isinstance(proc_frame, str) and proc_frame == "NO_MORE_FRAMES":
                system_messages_queue.put('Kill_Detector')
                system_messages_queue.put('Kill_Shower')
                break
            frame, rects = proc_frame[0], proc_frame[1]
            for rect in rects:
                (x, y, w, h) = rect
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # show the frame and record if the user presses a key
            cv.imshow("Security Feed", frame)
            cv.waitKey(self.wait_time)

            if cv.waitKey(1) == ord('q'):
                break
            # cleanup the camera and close any open windows
        cv.destroyAllWindows()


def start_shower(video_path: str, processed_frames_queue: Queue, system_messages_queue: Queue):
    shower = Shower(video_path, processed_frames_queue)
    shower.start(system_messages_queue)

# text = "Occupied"

# draw the text and timestamp on the frame
# cv.putText(frame, "Room Status: {}".format(text), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
#            2)
# cv.putText(frame, datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
#            cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
