import time

from ipcqueue import posixmq

from logic import Identificator
from project_util import get, LoggerControl


def init():
    LoggerControl().get_logger('control_screen').info('Screen control is initializing...')

    queue = posixmq.Queue('/signals')
    LoggerControl().get_logger('control_screen').info('Initialized posixmq queue')

    while True:
        if queue.qsize() == 0:
            time.sleep(.2)
        else:
            print("A ver")
            message = get(queue)
            print(message)
            LoggerControl().get_logger('control_screen').info('New signal: ' +
                                                              Identificator.codification[message.content])


if __name__ == '__main__':
    init()
