import keras
from keras import backend as K
from keras.optimizers import SGD
import numpy as np
import pandas as pd
from DATA import fakedata
from keras.models import model_from_json
from sklearn.preprocessing import StandardScaler

fd = fakedata.FackeData()


class KTFClassification(object):
    def __init__(self, path):
        self.model_n = self.model_nn(path + '/model_n')
        self.model_m = self.model_nn(path + '/model_m')
        self.model_ug = self.model_nn(path + '/model_ug')

    def model_nn(self, name):
        json_file = open(name + '.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(name + '.h5')
        sgd = SGD(lr=0.001, momentum=0.8, decay=0.0, nesterov=False)
        loaded_model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        return loaded_model

    def evaluate(self, data):
        so = pd.DataFrame(data)
        so = so.append(fd.maxdata1())
        so = so.append(fd.mindata1())
        if so.shape[0] > 2:
            count = so.shape[0] - 2
            so.iloc[:, [0, 1, 2, 3, 5, 8, 9]] = \
                StandardScaler().fit_transform(so.iloc[:, [0, 1, 2, 3, 5, 8, 9]].as_matrix())
            features = np.ascontiguousarray(so.iloc[:count, [0, 1, 2, 3, 5, 8, 9]], dtype=np.float32)
            out_n = self.model_n.predict_classes(features)
            out_m = self.model_m.predict_classes(features)
            out_ug = self.model_ug.predict_classes(features)
            return out_n, out_m, out_ug
        else:
            return None, None, None
