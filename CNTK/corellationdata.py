import pandas as pd
import seaborn as sns
from CNTK import config_cntk


def conv(n):
    """
    Преобразует название класса в трехмерный вектор из нулей и единиц
    """
    if n < 0.3:
        return 0
    if 0.3 <= n < 0.5:
        return 1
    if n >= 0.5:
        return 2


def dump(seq, fname):
    with open(fname, 'w') as f:
        for x in seq:
            f.write(
                "{};{};{};{};{};{};{};{};{};{};{};{}\n".format(conv(x[14]),
                                                               x[15], x[5], x[6], x[7], x[8],
                                                               x[9], x[10], x[11], x[12],
                                                               x[13], x[14]))


conf = config_cntk.ConfigLearning().config('UG')
so = pd.read_csv(conf['path_csv'], delimiter=';')
so[15] = so.iloc[:, [0, 1, 2, 3, 4]].sum(axis=1)
dump(so.values, 'os_data_ug.csv')
#so = pd.read_csv('os_data.csv', delimiter=';')
#sns.pairplot(so, hue='kl')

