import cv2
import numpy as np
from tensorflow.python.keras.models import load_model


class Identificator:
    size = (48, 48)
    codification = {
        0: 'Límite 20km/h',
        1: 'Límite 30km/h',
        2: 'Límite 50km/h',
        3: 'Límite 60km/h',
        4: 'Límite 70km/h',
        5: 'Límite 80km/h',
        6: 'Fin de límite 80km/h',
        7: 'Límite 100km/h',
        8: 'Límite 120km/h',
        9: 'Prohibido adelantar',
        10: 'Prohibido adelantar (camiones)',
        11: 'Peligro cruce a ambos lados',
        12: 'Señal de prioridad',
        13: 'Ceda el paso',
        14: 'STOP',
        15: 'Prohibido circular en ambos sentidos',
        16: 'Prohibido camiones',
        17: 'Prohibido pasar',
        18: 'Peligro indeterminado',
        19: 'Peligro curva a la izquierda',
        20: 'Peligro curva a la derecha',
        21: 'Peligro curvas peligrosas',
        22: 'Peligro baches',
        23: 'Peligro suelo deslizante',
        24: 'Peligro estrechamiento',
        25: 'Peligro obras',
        26: 'Peligro semáforo',
        27: 'Peligro peatones',
        28: 'Peligro niños',
        29: 'Peligro bicicletas',
        30: 'Peligro heladas',
        31: 'Peligro animales',
        32: 'Fin de todas las prohibiciones',
        33: 'Girar a la derecha',
        34: 'Girar a la izquierda',
        35: 'Seguir de frente',
        36: 'Seguir de frente o girar a la derecha',
        37: 'Seguir de frente o girar a la izquierda',
        38: 'Flecha derecha',
        39: 'Flecha izquierda',
        40: 'Glorieta',
        41: 'Fin de prohibicion adelantar',
        42: 'Fin de prohibicion adelantar (camiones)'
    }

    def __init__(self, net_name):
        self.net_name = net_name
        self.net = None
        self.result = None
        self._load_net()

    def _load_net(self):
        model_path = '../nets/' + self.net_name + '/model.h5'
        weights_path = '../nets/' + self.net_name + '/weights.h5'
        self.net = load_model(model_path)
        self.net.load_weights(weights_path)

    def evaluate(self, image):
        net_input = np.expand_dims(cv2.resize(image, Identificator.size), axis=0)
        result = self.net.predict(net_input)[0]
        return np.argmax(result)
