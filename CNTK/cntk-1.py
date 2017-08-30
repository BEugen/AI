import pylab
from matplotlib import gridspec
from sklearn.datasets import make_classification
import numpy as np
import cntk
from cntk import Trainer
from cntk.device import gpu
from cntk.learners import sgd
from cntk.ops import *

np.random.seed(0)
n = 100
X, Y = make_classification(n_samples=n, n_features=2,
                           n_redundant=0, n_informative=2, flip_y=0.3)
X = X.astype(np.float32)
Y = Y.astype(np.int32)

train_x, valid_x, test_x = np.split(X, [n//8, n*8//10])
train_labels, valid_labels, test_labels = np.split(Y, [n//8, n*8//10])

def plot_dataset(suptitle, features, labels):
    # prepare the plot
    fig, ax = pylab.subplots(1, 1)
    #pylab.subplots_adjust(bottom=0.2, wspace=0.4)
    fig.suptitle(suptitle, fontsize = 16)
    ax.set_xlabel('$x_i[0]$ -- (feature 1)')
    ax.set_ylabel('$x_i[1]$ -- (feature 2)')

    colors = ['r' if l else 'b' for l in labels]
    ax.scatter(features[:, 0], features[:, 1], marker='o', c=colors, s=100, alpha = 0.5)
    fig.show()

plot_dataset('Scatterplot of the training data', train_x, train_labels)