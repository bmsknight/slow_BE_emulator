import threading
import random
import time

WINDOW_TIME_SECOND = 20


class WindowTypeUpdater:
    def __init__(self):
        self.thread = None
        self.read_lock = threading.Lock()
        self.started = False
        self.p = 0
        self.t = time.time()
        self.w = WindowTypeUpdater.get_window_type()
        if self.w == 2:
            self.p = WindowTypeUpdater.get_anomaly_percentage()

    def start(self):
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()

    def update(self):
        while self.started:
            if time.time() >= self.t + WINDOW_TIME_SECOND:
                print('updating')
                with self.read_lock:
                    self.t = time.time()
                    self.w = WindowTypeUpdater.get_window_type()
                    if self.w == 2:
                        self.p = WindowTypeUpdater.get_anomaly_percentage()

    @staticmethod
    def get_window_type():
        return int(random.uniform(0, 3))

    @staticmethod
    def get_anomaly_percentage():
        return random.uniform(0, 1)

    def stop(self):
        self.started = False
        self.thread.join()

    def get_w_p(self):
        return self.w, self.p
