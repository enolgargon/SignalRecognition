import json
import time

from flask import Flask, Response
from ipcqueue import posixmq
from playhouse.shortcuts import model_to_dict

from project_util import getText, LoggerControl, register_signal, get_current_signals, codification, datetime_wrapper


def init():
    LoggerControl().get_logger('control_screen').info('Screen control is initializing...')

    queue = posixmq.Queue('/signals')
    LoggerControl().get_logger('control_screen').info('Initialized posixmq queue')

    while True:
        if queue.qsize() == 0:
            time.sleep(.2)
        else:
            message = getText(queue)
            print(message)
            register_signal(int(message.content))
            LoggerControl().get_logger('control_screen').info('New signal: ' + codification[int(message.content)])


app = Flask(__name__)


@app.route('/current-signals')
def current_signals():
    return Response(json.dumps([model_to_dict(s) for s in get_current_signals()], default=datetime_wrapper),
                    mimetype="application/json")


if __name__ == '__main__':
    from threading import Thread

    init_thread = Thread(target=init, name="Main screen control thread")
    init_thread.start()
    app.run()
    init_thread.join(0)
