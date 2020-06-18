import cv2
import numpy as np
import tensorflow as tf
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import load_model

from project_util import LoggerControl


class Identificator:
    size = (48, 48)

    def __init__(self, net_name):
        K.clear_session()
        LoggerControl().get_logger('logic_signal').info('Initializing Identificator with net named ' + net_name)
        self.net_name = net_name
        self.net = None
        self.result = None
        self._load_net()
        self._session = K.get_session()
        self._graph = tf.get_default_graph()
        #self._graph.finalize()

    def _load_net(self):
        model_path = '/home/recognition/SignalRecognition/nets/' + self.net_name + '/model.h5'
        weights_path = '/home/recognition/SignalRecognition/nets/' + self.net_name + '/weights.h5'

        self.net = load_model(model_path)
        LoggerControl().get_logger('logic_signal').info('Model of ' + self.net_name + ' was load')

        self.net.load_weights(weights_path)
        LoggerControl().get_logger('logic_signal').info('Weights of ' + self.net_name + ' was load')

    def evaluate(self, image):
        with self._session.as_default():
            with self._graph.as_default():
                net_input = np.expand_dims(cv2.resize(image, Identificator.size), axis=0)
                result = self.net.predict(net_input)
                self.result = np.argmax(result[0])

