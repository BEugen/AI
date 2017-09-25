from sklearn.preprocessing import StandardScaler, MinMaxScaler

import pandas as pd

so = pd.read_csv('data_so2N.csv', delimiter=';')
print(so)
sc_feat = so.copy()
col_n = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
sc_feat[col_n] = \
    MinMaxScaler().fit_transform(sc_feat[col_n].as_matrix())
sc_feat.to_csv('dt_so2n.csv', sep=';')

