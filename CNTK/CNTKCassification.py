import cntk
from cntk import Trainer
from cntk.learners import sgd
from cntk.ops import *
from cntk.io import *
from cntk.layers import *
from cntk.device import *
import pylab


class CntkClassification(object):
    def __init__(self, model_path):
        self.model_path = model_path

    def evaluate(self, data):
        z = load_model(self.model_path)
