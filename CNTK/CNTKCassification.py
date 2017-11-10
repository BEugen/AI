import cntk
from cntk import Trainer
from cntk.learners import sgd
from cntk.ops import *
from cntk.io import *
from cntk.layers import *
from cntk.device import *
import pylab
import numpy as np
import pandas as pd
from DATA import fakedata

from sklearn.preprocessing import StandardScaler, MinMaxScaler

fd = fakedata.FackeData()


class CntkClassification(object):
    def __init__(self, model_path):
        self.model_path = model_path

    def evaluate(self, data):
        so = pd.DataFrame(data)
        so = so.append(fd.maxdata1())
        so = so.append(fd.mindata1())
        z = load_model(self.model_path)
        if so.shape[0] > 2:
            count = so.shape[0] - 2
            so.iloc[:, [0, 1, 2, 3, 5, 8, 9]] = \
                StandardScaler().fit_transform(so.iloc[:, [0, 1, 2, 3, 5, 8, 9]].as_matrix())
            features = np.ascontiguousarray(so.iloc[:count, [0, 1, 2, 3, 5, 8, 9]], dtype=np.float32)
            out = []
            for row in features:
                out.append(np.argmax(z.eval({z.arguments[0]: [row]})))
            return np.rint(np.average(out))
        else:
            return 0

    def reevaluate(self, path, data):
        self.model_path = path
        return self.evaluate(data)
