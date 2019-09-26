import statistics as stats
from threading import Thread

import cv2
from ipcqueue import posixmq

import project_util as util
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
        util.LoggerControl().get_logger('logic_signal').info('Preprocess of ' + message.image_id + ' has started')

        color = cv2.cvtColor(message.content, cv2.COLOR_BGR2LAB)
        util.LoggerControl().get_logger('logic_signal').debug(
            'Applied ctv color transform to image ' + message.image_id)

        gauss = cv2.GaussianBlur(color, (9, 9), 0)
        util.LoggerControl().get_logger('logic_signal').debug('Applied gaussian transform to image ' + message.image_id)

        canny = cv2.Canny(gauss, 10, 250)
        util.LoggerControl().get_logger('logic_signal').debug('Applied canny transform to image ' + message.image_id)

        util.put(self.segment_queue, util.Message('logic_signal', 'Frame preprocessed', canny,
                                                  'A frame was read and preprocessed',
                                                  message.image_id + 'p'), 'segment_queue')

    def segment(self, message):
        util.LoggerControl().get_logger('logic_signal').info('Segment of ' + message.image_id + ' has started')

        (contours, hierarchy) = cv2.findContours(cv2.cvtColor(message.content, cv2.COLOR_BGR2GRAY), cv2.RETR_CCOMP,
                                                 cv2.CHAIN_APPROX_SIMPLE)
        hierarchy = hierarchy[0]
        util.LoggerControl().get_logger('logic_signal').debug(
            str(len(contours)) + ' contours found in image ' + message.image_id)

        margin = 10
        for i in range(len(contours)):
            if hierarchy[i][2] >= 0 or hierarchy[i][3] >= 0:
                c = contours[i]
                x, y, w, h = cv2.boundingRect(c)
                if abs(w - h) < 10:
                    util.put(self.identify_queue,
                             util.Message('logic_signal', 'Signal extracted',
                                          cv2.imread(util.Message.base_image_route + message.image_id[:-1:] + '.png')[
                                          x - margin:y - margin, x + w + margin:y + h + margin],
                                          'Possible signal extracted from frame',
                                          message.image_id + '_' + str(i)), 'identify_queue')

    def identify(self, message):
        util.LoggerControl().get_logger('logic_signal').info('Starting identification of image ' + message.image_id)

        threads = []
        for identificator in self.identificators:
            thread = Thread(target=identificator.net, args=(message.content,),
                            name=f"Identificator of net {identificator.net_name}")
            threads += [thread]
            thread.start()
            util.LoggerControl().get_logger('logic_signal').info(
                'Identificator ' + identificator.net_name + ' thread launched for image ' + message.image_id)

        util.LoggerControl().get_logger('logic_signal').debug(
            'Waiting while all threads finish for image ' + message.image_id)
        for thread in threads:
            thread.join()
        util.LoggerControl().get_logger('logic_signal').info('All threads finished. Computing results...')

        result = []
        for identificator in self.identificators:
            result += [identificator.result]

        signal = stats.mode(result)
        print(signal)
        if result.count(signal) > len(result) / 2:
            util.put(self.exit_queue, util.Message('logic_signal', 'Identify new signal', signal,
                                                   f"The threads give the result {str(result)}"
                                                   f" so the signal with code {signal} has been recognized. "
                                                   f"This signal has described as {Identificator.codification[signal]}",
                                                   message.image_id), 'signals_queue')
