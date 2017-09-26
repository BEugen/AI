import cntk
from cntk import Trainer
from cntk.learners import sgd
from cntk.ops import *
from cntk.io import *
from cntk.layers import *
from cntk.device import *
import pylab
from sklearn.preprocessing import StandardScaler, MinMaxScaler

import pandas as pd

so = pd.read_csv('data_so2M.csv', delimiter=';')
print(so)
sc_feat = so.copy()
col_n = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
sc_feat[col_n] = \
    MinMaxScaler().fit_transform(sc_feat[col_n].as_matrix())
#features = sc_feat.iloc[:, :14]
#features = StandardScaler().fit_transform(features.values)
#features = scaler.transform(features.values)
#sc_feat.iloc[:, :14] = features


# sc_feat[col_n] = features


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
                "|label {}|features {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" ".join(map(str, conv(x[14]))),
                                                                                        x[0], x[1], x[2], x[3],
                                                                                        x[4], x[5], x[6], x[7], x[8],
                                                                                        x[9], x[10], x[11], x[12],
                                                                                        x[13]))


x_so2 = 16877
data = np.random.permutation(sc_feat.values)
dump(data[0:x_so2], 'os_train.txt')
dump(data[x_so2:], 'os_test.txt')

reader_train = MinibatchSource(CTFDeserializer('os_train.txt',
                                               StreamDefs(
                                                   labels=StreamDef(field='label', shape=3),
                                                   features=StreamDef(field='features', shape=14))))

reader_test = MinibatchSource(CTFDeserializer('os_test.txt',
                                              StreamDefs(
                                                  labels=StreamDef(field='label', shape=3),
                                                  features=StreamDef(field='features', shape=14))))

input_var = input_variable(14)
label_var = input_variable(3)
model = Sequential([Dense(392, init=glorot_uniform(), activation=None),
                    Dense(196, init=glorot_uniform(), activation=tanh),
                    Dense(98, init=glorot_uniform(), activation=None),
                    Dense(32, init=glorot_uniform(), activation=tanh),
                    Dense(18, init=glorot_uniform(), activation=sigmoid),
                    Dense(3, init=glorot_uniform(), activation=None)])
z = model(input_var)
ce = cntk.cross_entropy_with_softmax(z, label_var)
pe = cntk.classification_error(z, label_var)

minibatch_size = 16

lr_per_minibatch = cntk.learning_rate_schedule(0.01, cntk.UnitType.minibatch)
pp = cntk.logging.ProgressPrinter()

learner = cntk.adagrad(z.parameters, lr=lr_per_minibatch)
trainer = cntk.Trainer(z, (ce, pe), [learner], [pp])

input_map = {
    input_var: reader_train.streams.features,
    label_var: reader_train.streams.labels
}

cntk.logging.log_number_of_parameters(z)
progress = []

for x in range(200):
    tloss = 0
    taccuracy = 0
    cnt = 0
    for y in range(500):
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
z.save("model-som.dnn")
print("Eval error = {}".format(metric * 100))
