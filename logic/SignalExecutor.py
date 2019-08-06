import cv2

import proyect_util as util
from . import AbstractExecutor


class SignalExecutor(AbstractExecutor):
    def preprocess(self, message):
        color = cv2.cvtColor(message.content, cv2.COLOR_BGR2LAB)
        gauss = cv2.GaussianBlur(color, (9, 9), 0)
        canny = cv2.Canny(gauss, 10, 250)
        util.queue_util.put(self.segment_queue, util.Message.Message('preprocess signals', 'Frame preprocessed', canny,
                                                                     'A frame was read and preprocessed'))
