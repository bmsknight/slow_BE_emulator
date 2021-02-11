import threading
import random
import time


class WindowTypeUpdater:
    def __init__(self,window_time_second):
        self.thread = None
        self.read_lock = threading.Lock()
        self.started = False

        self.window_time_second = window_time_second
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
            if time.time() >= self.t + self.window_time_second:
                print('updating')
                with self.read_lock:
                    self.t = time.time()
                    self.w = WindowTypeUpdater.get_window_type()
                    if self.w == 2:
                        self.p = WindowTypeUpdater.get_anomaly_percentage()

    @staticmethod
    def get_window_type():
        v = random.uniform(0, 1)
        if v < 0.8:
            return 0
        elif v < 0.95:
            return 1
        else:
            return 2

    @staticmethod
    def get_anomaly_percentage():
        return random.uniform(0, 1)

    def stop(self):
        self.started = False
        self.thread.join()

    def get_w_p(self):
        return self.w, self.p
