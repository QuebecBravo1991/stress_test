from multiprocessing import get_context
from os import sched_setaffinity, getpid
from stress_test_utils import get_max_subprocess, get_core_temp
import time
from datetime import datetime, timedelta
from hashlib import sha256


LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

def workload(target_core, stop_event):
    sched_setaffinity(getpid(), [target_core])
    with open("test_strings.txt") as strings:
        with open("hashes.txt") as hashes:
            strings_lines = strings.readlines()
            hashes_lines = hashes.readlines()

            assert len(hashes_lines) == len(strings_lines), ("The hashes and strings files are malformed and do not have "
                                                             "the same length.")

            j = 0
            while not stop_event.is_set():
                assert sha256(strings_lines[j].strip('\n').encode('utf-8')).hexdigest() == hashes_lines[j].strip('\n'), ("The generated hashes don't match "
                                                                                     "known good ones.")
                if j == 999:
                    j = 0
                else:
                    j += 1


if __name__ == "__main__":
    try:
        num_workers = int(input(f"Enter the number of cores to run the stress test on. Max {get_max_subprocess()} : "))
        if num_workers > get_max_subprocess():
            raise ValueError
        duration = float(input("Enter the desired test duration in minutes: "))
        if duration < 0:
            raise ValueError
    except ValueError:
        print(f"Invalid input.")
        exit()

    input(f"Press enter to start {num_workers} workers. ")

    ctx = get_context("spawn")

    workers = []
    stop_events = []

    for i in range(num_workers):
        stop = ctx.Event()
        stop_events.append(stop)

        p = ctx.Process(target=workload, args=(i, stop))

        p.start()
        workers.append(p)

    print("Done. Displaying CPU temperature.\n")
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration)

    while datetime.now() < end_time:
        core_name, core_temp = get_core_temp()
        display_lines = [f"{core_name} is {core_temp} C",
                         f"Time lapsed: {(datetime.now() - start_time).seconds/60:.1f} of {duration}"
                         ]
        for line in display_lines:
            print(line)
        time.sleep(0.2)
        for line in display_lines:
            print(LINE_UP, end=LINE_CLEAR)

    print("Stress test done. Shutting down workers.")

    for i in range(len(workers)):
        stop_events[i].set()
        workers[i].join()

    print("Done.")