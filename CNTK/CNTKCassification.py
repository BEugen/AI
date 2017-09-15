import cntk
from cntk import Trainer
from cntk.learners import sgd
from cntk.ops import *
from cntk.io import *
from cntk.layers import *
from cntk.device import *
import pylab
import numpy as np

from sklearn.preprocessing import StandardScaler


class CntkClassification(object):
    def __init__(self, model_path):
        self.model_path = model_path

    def evaluate(self, data_insql, data_metheo):
        z = load_model(self.model_path)
        data_insql = data_insql[0]
        rtp = int(data_insql[9] > 0 + data_insql[10] > 0 + data_insql[11] > 0)
        evdata = [data_insql[1], data_insql[2], data_insql[3], data_insql[4], data_insql[5], rtp,
                  data_metheo[0], data_metheo[1], data_metheo[3], data_metheo[4], data_metheo[5],
                  data_metheo[6], data_metheo[7], data_metheo[8]]
        ed = np.array(evdata).reshape(1, -1)
        scaler = StandardScaler().fit(ed)
        features = scaler.transform(ed)
        pass