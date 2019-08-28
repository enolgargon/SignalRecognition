import time

from ipcqueue import posixmq

from proyect_util import get


def init():
    queue = posixmq.Queue('/signals')

    while True:
        if queue.qsize() == 0:
            time.sleep(.2)
        else:
            message = get(queue)
            print(message)


if __name__ == '__main__':
    init()
