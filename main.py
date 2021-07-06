from multiprocessing import Process, Queue
from time import sleep
import argparse

from streamer import start_streaming


def worker(q: Queue):
    """thread worker function"""
    print(f'Worker: {q.get()}')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video Detector Pipeline.')
    parser.add_argument('--video_path', type=str, default='People.mp4', help='Path to video')
    args = parser.parse_args()

    process = ['streamer', 'detector', 'show']
    num_of_process = len(process)

    frames_queue = Queue()
    jobs = []

    for i in range(num_of_process):
        if process[i] == 'streamer':
            p = Process(target=start_streaming, args=(args.video_path, frames_queue,))
            jobs.append(p)

    for job in jobs:
        job.start()

    # kill all process
    while True:
        msg = frames_queue.get()
        if isinstance(msg, str) and msg == "NO_MORE_FRAMES":
            print("[MAIN]: Terminating slacking WORKER")
            jobs[0].terminate()
            sleep(0.1)
            if not jobs[0].is_alive():
                print("[MAIN]: WORKER is a goner")
                jobs[0].join(timeout=1.0)
                print("[MAIN]: Joined WORKER successfully!")
                frames_queue.close()
                break  # watchdog process daemon gets terminated

    print(jobs)
