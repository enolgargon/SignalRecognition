import time
from datetime import datetime

import cv2
from ipcqueue import posixmq

import project_util as util


def init():
    util.LoggerControl().get_logger('control_camera').info('Camera control is initializing...')

    cap = cv2.VideoCapture('../../prueba.mp4')
    util.LoggerControl().get_logger('control_camera').debug('Video capture initialized')

    queue = posixmq.Queue('/camera_control')
    util.LoggerControl().get_logger('control_camera').info('Initialized posixmq queue')

    try:
        while cap.isOpened():
            read_flag, frame = cap.read()
            if not read_flag:
                util.LoggerControl().get_logger('control_camera').error('Error while new frame was reading')
                pass
            else:
                util.put(queue, util.Message('control_camera', 'New frame', cv2.resize(frame, (0, 0), fx=0.5, fy=0.5),
                                             'New frame has been read',
                                             datetime.now().strftime('%Y%m%d%H%M%S%f')), 'camera_control')
                time.sleep(.5)
    except:
        util.LoggerControl().get_logger('control_camera').error('Un handler error', exc_info=True)
    finally:
        cap.release()
        util.LoggerControl().get_logger('control_camera').info('Capture release')


if __name__ == '__main__':
    init()
