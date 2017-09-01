import cntk
from cntk import Trainer
from cntk.learners import sgd
from cntk.ops import *
from cntk.io import *
from cntk.layers import *
from cntk.device import *
import pylab

import pandas as pd

iris = pd.read_csv('iris.csv')
# print(iris)
# Строим отображение типов ирисов на номер класса
fwmap = dict(enumerate(set(iris.values[:, 4])))
bkmap = {fwmap[k]: k for k in fwmap}
print(fwmap, bkmap)


def conv(n):
    """
    Преобразует название класса в трехмерный вектор из нулей и единиц
    """
    return [1 if x == n else 0 for i, x in fwmap.items()]


def dump(seq, fname):
    with open(fname, 'w') as f:
        for x in seq:
            f.write("|label {}|features {} {} {} {}\n".format(" ".join(map(str, conv(x[4]))), x[0], x[1], x[2], x[3]))


data = np.random.permutation(iris.values)
dump(data[0:130], 'iris_train.txt')
dump(data[130:], 'iris_test.txt')

reader_train = MinibatchSource(CTFDeserializer('iris_train.txt',
                                               StreamDefs(
                                                   labels=StreamDef(field='label', shape=3),
                                                   features=StreamDef(field='features', shape=4))))

reader_test = MinibatchSource(CTFDeserializer('iris_test.txt',
                                              StreamDefs(
                                                  labels=StreamDef(field='label', shape=3),
                                                  features=StreamDef(field='features', shape=4))))

input_var = input_variable(4)
label_var = input_variable(3)
model = Sequential([Dense(16, init=glorot_uniform(), activation=sigmoid),
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

for x in range(150):
    tloss = 0;
    taccuracy = 0;
    cnt = 0;
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

print("Eval error = {}".format(metric))

