import time

from ipcqueue import posixmq


def init():
    queue = posixmq.Queue('/signals')

    while True:
        if queue.qsize() == 0:
            time.sleep(.2)
        else:
            message = queue.get()
            print(message)


if __name__ == '__main__':
    init()
