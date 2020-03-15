import json
import time

from flask import Flask, Response, request
from flask_cors import CORS
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
cors = CORS(app)
cf = None


@app.route('/current-signals', methods=['GET'])
def current_signals():
    return Response(json.dumps([model_to_dict(s) for s in get_current_signals()], default=datetime_wrapper),
                    mimetype="application/javascript")


@app.route('/current-frame', methods=['GET', 'POST'])
def current_frame():
    global cf
    if request.method == 'POST':
        new_frame = request.form.get('frame', current_frame)
        if new_frame is not None and isinstance(new_frame, str):
            cf = new_frame
            return Response(json.dumps({'msg': 'New frame change succesfully'}), mimetype="application/javascript",
                            status=201)
        return Response(json.dumps({'msg': 'New frame is not valid'}), mimetype="application/javascript", status=400)
    return Response(json.dumps({'frame': cf}), mimetype="application/javascript")


if __name__ == '__main__':
    from threading import Thread

    init_thread = Thread(target=init, name="Main screen control thread")
    init_thread.start()
    app.run()
    init_thread.join(0)
