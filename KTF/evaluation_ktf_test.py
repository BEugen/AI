# ﻿from pip import models
import numpy as np
import sys
import os
import argparse

###################################################################
# Variables                                                       #
# When launching project or scripts from Visual Studio,           #
# input_dir and output_dir are passed as arguments.               #
# Users could set them from the project setting page.             #
###################################################################

input_dir = None
output_dir = None
log_dir = None

#################################################################################
# Keras configs.                                                                #
# Please refer to https://keras.io/backend .                                    #
#################################################################################

import keras
from keras import backend as K

# K.set_floatx('float32')
# String: 'float16', 'float32', or 'float64'.

# K.set_epsilon(1e-05)
# float. Sets the value of the fuzz factor used in numeric expressions.

# K.set_image_data_format('channels_first')
# data_format: string. 'channels_first' or 'channels_last'.


#################################################################################
# Keras imports.                                                                #
#################################################################################

from keras.models import Model
from keras.models import Sequential
from keras.layers import Input
from keras.layers import Lambda
from keras.layers import Layer
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Activation
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.optimizers import SGD
from keras.optimizers import RMSprop
from keras.callbacks import TensorBoard
from keras.utils import np_utils
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
# import matplotlib.pyplot as plt
from time import time
from keras.models import model_from_json


def classification(x):
    if x < 0.3:
        return 0
    if 0.3 <= x < 0.5:
        return 1
    if x >= 0.5:
        return 2


def model_nn(name):
    json_file = open(name + '.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(name + '.h5')
    sgd = SGD(lr=0.001, momentum=0.8, decay=0.0, nesterov=False)
    loaded_model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return loaded_model


def main():
    so = pd.read_csv('data_so.csv', delimiter=';')
    so['c8_q'] = so.iloc[:, [1, 2, 3, 4, 5]].sum(axis=1)
    so['label_n'] = so.apply(lambda x: classification(x.iloc[15]), axis=1)
    so['label_m'] = so.apply(lambda x: classification(x.iloc[16]), axis=1)
    so['label_ug'] = so.apply(lambda x: classification(x.iloc[17]), axis=1)
    so.drop(so.columns[[0, 1, 2, 3, 4, 9, 11, 12, 15, 16, 17]], inplace=True, axis=1)
    so.iloc[:, 0:7] = \
        StandardScaler().fit_transform(so.iloc[:, 0:7].as_matrix())
    so.to_csv('data_so_all-pr.csv', sep=';')
    data = np.random.permutation(so.values)
    X = data[:, 0:7].astype(float)
    Y_n = data[:, 7]
    Y_m = data[:, 8]
    Y_u = data[:, 9]
    enc = LabelEncoder()
    enc_Y = enc.fit_transform(Y_n)
    Y_n_f = np_utils.to_categorical(enc_Y)
    enc_Y = enc.fit_transform(Y_m)
    Y_m_f = np_utils.to_categorical(enc_Y)
    enc_Y = enc.fit_transform(Y_u)
    Y_u_f = np_utils.to_categorical(enc_Y)
    model = model_nn('model_n')
    score = model.evaluate(X, Y_n_f, verbose=1)
    print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))
    model = model_nn('model_m')
    score = model.evaluate(X, Y_m_f, verbose=1)
    print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))
    model = model_nn('model_ug')
    score = model.evaluate(X, Y_u_f, verbose=1)
    print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str,
                        default=None,
                        help="Input directory where where training dataset and meta data are saved",
                        required=False
                        )
    parser.add_argument("--output_dir", type=str,
                        default=None,
                        help="Input directory where where logs and models are saved",
                        required=False
                        )

    args, unknown = parser.parse_known_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    log_dir = output_dir

    main()
