import time
from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread, current_thread

from ipcqueue import posixmq


class AbstractExecutor(ABC):
    def __init__(self):
        self.camera_queue = posixmq.Queue('/camera_control')
        self.segment_queue = Queue()
        self.identify_queue = Queue()
        self.thread1 = None
        self.thread2 = None
        self.thread3 = None

    def _dequeue(self, queue):
        if queue.qsize() > 0:
            message = queue.get()
            if message is None:
                time.sleep(.2)
            else:
                return message
        else:
            time.sleep(.2)
        return None

    @abstractmethod
    def preprocess(self, message):
        pass

    @abstractmethod
    def segment(self, message):
        pass

    @abstractmethod
    def identify(self, message):
        pass

    def __preprocess_and_segment(self):
        while True:
            message = self._dequeue(self.camera_queue)
            if message is not None:
                self.preprocess(message)

            message = self._dequeue(self.segment_queue)
            if message is not None:
                self.segment(message)

    def _dequeue_identify(self):
        while True:
            message = self._dequeue(self.identify_queue)
            if message is not None:
                self.identify(message)

    def create_threads(self):
        current_thread().setName(f"{self.__class__.__name__} preprocess and segmentation thread")
        self.thread2 = Thread(target=self._dequeue_identify,
                              name=f"{self.__class__.__name__} identification first thread")
        self.thread3 = Thread(target=self._dequeue_identify,
                              name=f"{self.__class__.__name__} identification second thread")

        self.thread2.start()
        self.thread3.start()
        return self.__preprocess_and_segment
