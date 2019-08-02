from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread


class AbstractExecutor(ABC):
    def __init__(self):
        self.segment_queue = Queue()
        self.identify_queue = Queue()
        self.thread1 = None
        self.thread2 = None
        self.thread3 = None

    @abstractmethod
    def preprocess(self):
        pass

    @abstractmethod
    def segment(self):
        pass

    @abstractmethod
    def identify(self):
        pass

    def __preprocess_and_segment(self):
        self.preprocess()
        self.segment()

    def create_threads(self):
        self.thread1 = Thread(target=self.__preprocess_and_segment,
                              name=f"{self.__class__.__name__} preprocess and segmentation thread")
        self.thread2 = Thread(target=self.identify, name=f"{self.__class__.__name__} identification first thread")
        self.thread3 = Thread(target=self.identify, name=f"{self.__class__.__name__} identification second thread")

        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
