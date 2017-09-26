from sklearn.preprocessing import StandardScaler, MinMaxScaler
from DATA import datasql
import pandas as pd

so = pd.read_csv('data_so2N.csv', delimiter=';')
sc_feat = so.copy()
col_n = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
sc_feat.iloc[col_n] = \
    MinMaxScaler().fit_transform(sc_feat.iloc[col_n].as_matrix())
sc_feat.to_csv('dt_so2n.csv', sep=';')
#sql = datasql.SqlLiteBase('/home/administrator/projects/websovisu/db.sqlite3')
sql = datasql.SqlLiteBase('/home/eugen/PycharmProjects/WebSOVisu/db.sqlite3')
data_full = sql.getwheterdata()
so = pd.DataFrame(data_full)
scaler = MinMaxScaler().fit(so[[7]].as_matrix())
print(scaler.data_max_)
print(scaler.data_min_)
scaler.data_max_ = 790.0
scaler.data_min_ = 710.0
so[[7]] = \
    scaler.transform(so[[7]].as_matrix())
print(so[[7]])


