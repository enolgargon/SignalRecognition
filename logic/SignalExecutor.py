import cv2

import proyect_util as util
from . import AbstractExecutor


class SignalExecutor(AbstractExecutor):
    def preprocess(self, message):
        color = cv2.cvtColor(message.content, cv2.COLOR_BGR2LAB)
        gauss = cv2.GaussianBlur(color, (9, 9), 0)
        canny = cv2.Canny(gauss, 10, 250)
        util.queue_util.put(self.segment_queue, util.Message.Message('preprocess signals', 'Frame preprocessed', canny,
                                                                     'A frame was read and preprocessed',
                                                                     message.image_id))

    def segment(self, message):
        (contornos, hierarchy) = cv2.findContours(message.content.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        hierarchy = hierarchy[0]

        margin = 10
        for i in range(len(contornos)):
            if hierarchy[i][2] >= 0 and hierarchy[i][3] >= 0:
                c = contornos[i]
                x, y, w, h = cv2.boundingRect(c)
                if abs(w - h) < 10:
                    util.queue_util.put(self.identify_queue,
                                        util.Message.Message('segment signals', 'Signal extracted',
                                                             message.content[x - margin:y - margin,
                                                             x + w + margin:y + h + margin],
                                                             'Possible signal extracted from frame',
                                                             message.image_id + '_' + str(i)))
