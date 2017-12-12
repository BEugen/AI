from __future__ import print_function
from pip import models
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

#K.set_floatx('float32')
#String: 'float16', 'float32', or 'float64'.

#K.set_epsilon(1e-05)
#float. Sets the value of the fuzz factor used in numeric expressions.

#K.set_image_data_format('channels_first')
#data_format: string. 'channels_first' or 'channels_last'.


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
from keras.utils import np_utils
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt


def classification(x):
      if x < 0.3:
          return 0
      if 0.3 <= x < 0.5:
          return 1
      if x >= 0.5:
          return 2

def nn_model():
    model = Sequential()
    model.add(Dense(7, input_dim=7, init='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(14, init='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(28, init='normal', activation='relu'))
    model.add(Dense(18, init='normal', activation='relu'))
    model.add(Dense(3, init='normal', activation='sigmoid'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def main():
    so = pd.read_csv('data_so2m-1.csv', delimiter=';')
    so['q_c'] = so.iloc[:, [0, 1, 2, 3, 4]].sum(axis=1)
    so['label'] = so.apply(lambda x: classification(x.iloc[14]), axis=1)   
    so.drop(so.columns[[0, 1, 2, 3, 4, 8, 10, 11, 14]], inplace=True, axis=1)
    so.iloc[:, 0:7] = \
        StandardScaler().fit_transform(so.iloc[:, 0:7].as_matrix())
    so.to_csv('data_so_all.csv', sep=';')
    data = np.random.permutation(so.values)
    X = data[:, 0:7].astype(float)
    Y = data[:, 7]
    enc = LabelEncoder()
    enc_Y = enc.fit_transform(Y)
    dumm_y = np_utils.to_categorical(enc_Y)
    (X_train, X_test, Y_train, Y_test) = train_test_split(X, dumm_y, test_size=.25)

    # fit
    model = nn_model()
    history = model.fit(X_train, Y_train, batch_size=35, nb_epoch=200, verbose=1)

    # predict
    predictions = model.predict_proba(X_test)
    print('Accuracy: {}'.format(roc_auc_score(y_true=Y_test, y_score=predictions)))


    # График точности модели
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # График оценки loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

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
