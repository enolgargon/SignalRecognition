import time

import cv2
from ipcqueue import posixmq


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
                # extern this to util class
                # the queue should contain a message
                queue.put(frame)
                time.sleep(.5)
    finally:
        cap.release()


if __name__ == '__main__':
    init()
