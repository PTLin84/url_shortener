import time
import threading

PROCESS_ID = "000"  # unique process/machine id


class UniqueIDGenerator:
    def __init__(self):
        self.last_millisecond = int(time.time() * 1000)
        self.counter = 0
        self.lock = threading.Lock()  # for thread safety

    def get_unique_id(self):
        with self.lock:
            current_millisecond = int(time.time() * 1000)

            if current_millisecond != self.last_millisecond:
                self.counter = 0
                self.last_millisecond = current_millisecond
            else:
                self.counter += 1

            unique_id = f"{current_millisecond}{PROCESS_ID}{self.counter:04d}"
            return unique_id
