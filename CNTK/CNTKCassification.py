import cntk
from cntk import Trainer
from cntk.learners import sgd
from cntk.ops import *
from cntk.io import *
from cntk.layers import *
from cntk.device import *
import pylab
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler


class CntkClassification(object):
    def __init__(self, model_path):
        self.model_path = model_path

    def evaluate(self, data):
        z = load_model(self.model_path)
        ed = np.array(data)
        scaler = StandardScaler().fit(ed)
        features = scaler.transform(ed)
        #output = z.
        #features = MinMaxScaler().fit_transform(ed)
        pass