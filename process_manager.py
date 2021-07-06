from multiprocessing import Process, Queue
from time import sleep
from typing import List


def kill_process(jobs: List[Process]):
    jobs[0].terminate()
    sleep(0.1)
    if not jobs[0].is_alive():
        print("[MAIN]: WORKER is a goner")
        jobs[0].join(timeout=1.0)
        print("[MAIN]: Joined WORKER successfully!")
        del jobs[0]
        print(jobs)


def watchdog(system_messages_queue: Queue, jobs: List[Process]):
    # kill all process
    while True:
        msg = system_messages_queue.get()
        if msg == "Kill_Streamer":
            print("[MAIN]: Terminating slacking WORKER")
            kill_process(jobs)
        elif msg == "Kill_Detector":
            print("[MAIN]: Terminating slacking WORKER")
            kill_process(jobs)
        elif msg == "Kill_Shower":
            print("[MAIN]: Terminating slacking WORKER")
            kill_process(jobs)
        else:
            print('New System message')

        if len(jobs) == 0:  # watchdog process daemon gets terminated
            system_messages_queue.close()
            break
