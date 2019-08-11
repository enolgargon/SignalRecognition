import time
from datetime import datetime

import cv2
from ipcqueue import posixmq

import proyect_util as util


def init():
    cap = cv2.VideoCapture('../../prueba.MOV')
    queue = posixmq.Queue('/camera_control')

    try:
        while cap.isOpened():
            read_flag, frame = cap.read()
            if not read_flag:
                # log error
                pass
            else:
                util.put(queue, util.Message('control_camera', 'New frame', frame, 'New frame has '
                                                                                   'been read',
                                             datetime.now().strftime('%Y%m%d%H%M%S')))
                time.sleep(.5)
    finally:
        cap.release()


if __name__ == '__main__':
    init()
