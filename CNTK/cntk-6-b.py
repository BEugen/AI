import cntk
from cntk import Trainer
from cntk.learners import sgd
from cntk.ops import *
from cntk.io import *
from cntk.initializer import *
from cntk.layers import *
from cntk.device import *
import pylab
from sklearn.preprocessing import StandardScaler, MinMaxScaler

import pandas as pd
from CNTK import config_cntk

cfg_name = ('N', 'M', 'UG')
for cfg in cfg_name:
    conf = config_cntk.ConfigLearning().config(cfg)
    so = pd.read_csv(conf['path_csv'], delimiter=';')
    sc_feat = so.copy()
    sc_feat[15] = sc_feat.iloc[:, [0, 1, 2, 3, 4]].sum(axis=1)
    sc_feat.iloc[:, 4:16] = \
        StandardScaler().fit_transform(sc_feat.iloc[:, 4:16].as_matrix())


    def conv(n):
        """
        Преобразует название класса в трехмерный вектор из нулей и единиц
        """
        if n < 0.3:
            return [1, 0, 0]
        if 0.3 <= n < 0.5:
            return [0, 1, 0]
        if n >= 0.5:
            return [0, 0, 1]


    def dump(seq, fname):
        with open(fname, 'w') as f:
            for x in seq:
                f.write(
                    "|label {}|features {} {} {} {} {} {} {}\n".format(" ".join(map(str, conv(x[14]))),
                                                                                x[15], x[5], x[6], x[7],
                                                                                x[9], x[12],
                                                                                x[13]))


    part = int(sc_feat.shape[0]*0.8)
    data = np.random.permutation(sc_feat.values)
    dump(data[0:part], 'os_train.txt')
    dump(data[part:], 'os_test.txt')

    reader_train = MinibatchSource(CTFDeserializer('os_train.txt',
                                                   StreamDefs(
                                                       labels=StreamDef(field='label', shape=3),
                                                       features=StreamDef(field='features', shape=7))))

    reader_test = MinibatchSource(CTFDeserializer('os_test.txt',
                                                  StreamDefs(
                                                      labels=StreamDef(field='label', shape=3),
                                                      features=StreamDef(field='features', shape=7))))

    input_var = input_variable(7)
    label_var = input_variable(3)
    # model = Sequential([Dense(84, init=he_uniform(), activation=None),
    #                    Dense(36, init=he_uniform(), activation=tanh),
    #                    Dense(18, init=he_uniform(), activation=relu),
    #                    Dense(3, init=he_uniform(), activation=None)])
    model = Sequential([Dense(70, init=glorot_uniform(), activation=tanh),
                        Dense(140, init=glorot_uniform(), activation=sigmoid),
                        Dense(105, init=glorot_uniform(), activation=sigmoid),
                        Dense(70, init=he_uniform(), activation=relu),
                        Dense(48, init=he_uniform(), activation=sigmoid),
                        Dense(32, init=he_uniform(), activation=tanh),
                        Dense(16, init=glorot_uniform(), activation=relu),
                        Dense(8, init=glorot_uniform(), activation=tanh),
                        Dense(6, init=he_uniform(), activation=relu),
                        Dense(3, init=he_uniform(), activation=None)
                        ])
    z = model(input_var)
    ce = cntk.cross_entropy_with_softmax(z, label_var)
    pe = cntk.classification_error(z, label_var)

    minibatch_size = 16

    lr_per_minibatch = cntk.learning_rate_schedule(0.001, cntk.UnitType.minibatch)
    pp = cntk.logging.ProgressPrinter()

    learner = cntk.adagrad(z.parameters, lr=lr_per_minibatch)
    trainer = cntk.Trainer(z, (ce, pe), [learner], [pp])

    input_map = {
        input_var: reader_train.streams.features,
        label_var: reader_train.streams.labels
    }

    cntk.logging.log_number_of_parameters(z)
    progress = []

    for x in range(3000):
        tloss = 0
        taccuracy = 0
        cnt = 0
        for y in range(300):
            data = reader_train.next_minibatch(minibatch_size, input_map)
            t = trainer.train_minibatch(data)
            tloss += trainer.previous_minibatch_loss_average * trainer.previous_minibatch_sample_count
            taccuracy += trainer.previous_minibatch_evaluation_average * trainer.previous_minibatch_sample_count
            cnt += trainer.previous_minibatch_sample_count
            pp.update_with_trainer(trainer, with_metric=True)
        progress.append([float(x), tloss / cnt, taccuracy / cnt])
        pp.epoch_summary(with_metric=True)

    progress = np.array(progress)
    print(progress[:, 0], progress[:, 2])

    test_size = 20

    data = reader_test.next_minibatch(test_size, input_map=input_map)
    metric = trainer.test_minibatch(data)
    z.save(conf['path_save'])
    print("Eval error = {}".format(metric))

import os
os.system('python3 /home/eugen/PycharmProjects/AI/CNTK/evaluation_test.py')
