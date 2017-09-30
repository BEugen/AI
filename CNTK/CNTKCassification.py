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
        z = load_model(self.model_path)
        so = pd.DataFrame(data)
        so = so.append(fd.maxdata1())
        so = so.append(fd.mindata1())
        so.iloc[:, :11] = \
            MinMaxScaler().fit_transform(so.iloc[:, :11].as_matrix())
        print(so)
        features = np.ascontiguousarray(so.iloc[:1, :11], dtype=np.float32)
        output = z.eval({z.arguments[0]: [features]})
        top_class = np.argmax(output)
        return top_class

    def reevaluate(self, path, data):
        self.model_path = path
        return self.evaluate(data)
