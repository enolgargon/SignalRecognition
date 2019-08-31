import statistics as stats
from threading import Thread

import cv2
from ipcqueue import posixmq

import proyect_util as util
from .AbstractExecutor import AbstractExecutor
from .Identificator import Identificator


class SignalExecutor(AbstractExecutor):
    def __init__(self, nets):
        super().__init__()
        self.exit_queue = posixmq.Queue('/signals')

        self.identificators = []
        if type(nets) == 'array':
            for net in nets:
                self.identificators += [Identificator(net)]
        elif type(nets) == 'string':
            self.identificators += [Identificator(nets)]
        else:
            TypeError('The constructor param must be of type array or string')

    def preprocess(self, message):
        color = cv2.cvtColor(message.content, cv2.COLOR_BGR2LAB)
        gauss = cv2.GaussianBlur(color, (9, 9), 0)
        canny = cv2.Canny(gauss, 10, 250)
        util.put(self.segment_queue, util.Message('logic_signal', 'Frame preprocessed', canny,
                                                  'A frame was read and preprocessed',
                                                  message.image_id))

    def segment(self, message):
        (contours, hierarchy) = cv2.findContours(message.content.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        hierarchy = hierarchy[0]

        margin = 10
        for i in range(len(contours)):
            if hierarchy[i][2] >= 0 and hierarchy[i][3] >= 0:
                c = contours[i]
                x, y, w, h = cv2.boundingRect(c)
                if abs(w - h) < 10:
                    util.put(self.identify_queue,
                             util.Message('logic_signal', 'Signal extracted',
                                          message.content[x - margin:y - margin,
                                          x + w + margin:y + h + margin],
                                          'Possible signal extracted from frame',
                                          message.image_id + '_' + str(i)))

    def identify(self, message):
        threads = []
        for identificator in self.identificators:
            thread = Thread(target=identificator.net, args=(message.content,),
                            name=f"Identificator of net {identificator.net_name}")
            threads += [thread]
            thread.start()

        for thread in threads:
            thread.join()

        result = []
        for identificator in self.identificators:
            result += [identificator.result]

        signal = stats.mode(result)
        if result.count(signal) > len(result) / 2:
            util.put(self.exit_queue, util.Message('logic_signal', 'Identify new signal', signal,
                                                   f"The threads give the result {str(result)}"
                                                   f" so the signal with code {signal} has been recognized. "
                                                   f"This signal has described as {Identificator.codification[signal]}",
                                                   message.image_id))
