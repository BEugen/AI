from DATA import datasql
from METHEO import htmltotable
from CNTK import CNTKCassification
from KTF import KTFClassificator
import datetime
import time
import locale
import re
import numpy as np
# test data format
# k4, k5, k6, k7, k8, rtp, T, P, U, ff, ff10, Td, RRR, Wg
#                      5   6  7  8   9  10    11   12  13
#                  0   1   2  3  4   5  6      7    8   9
insql = datasql.GetDataFromPc()
proxies = {
    "http": "127.0.0.1:3128",
    "https": "127.0.0.1:3128",
}

wnd = {'Ветер, дующий с востока': 90, 'Ветер, дующий с востоко-северо-востока': 68,
       'Ветер, дующий с востоко-юго-востока': 112, 'Ветер, дующий с запада': 270,
       'Ветер, дующий с западо-северо-запада': 292, 'Ветер, дующий с западо-юго-запада': 248,
       'Ветер, дующий с севера': 360, 'Ветер, дующий с северо-востока': 45,
       'Ветер, дующий с северо-запада': 298, 'Ветер, дующий с северо-северо-востока': 22,
       'Ветер, дующий с северо-северо-запада': 318, 'Ветер, дующий с юга': 180,
       'Ветер, дующий с юго-востока': 135, 'Ветер, дующий с юго-запада': 225,
       'Ветер, дующий с юго-юго-востока': 158, 'Ветер, дующий с юго-юго-запада': 202,
       'Штиль, безветрие': 0, '': 0}

obj = htmltotable.HtmlTables('https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0'
                             '%B2_%D0%9D%D0%B8%D0%BA%D0%B5%D0%BB%D0%B5', proxies)
# sql = datasql.SqlLiteBase('/home/eugen/PycharmProjects/WebSOVisu/db.sqlite3')
sql = datasql.SqlLiteBase('/home/administrator/projects/websovisu/db.sqlite3')
hour = -1
ktf = KTFClassificator.KTFClassification('/home/administrator/projects/KTF')
while True:
    dt = datetime.datetime.now()
    if dt.hour != hour:
        try:
            hour = dt.hour
            table = obj.read()
            if table is None:
                continue
            series = table.iloc[1]
            dats = series[0]
            year = re.search(r'(?P<year>\d+)', dats).group('year')
            day_month = re.search(r'(?P<dm>\d+\W\w+)', dats).group('dm')
            d = re.search(r'(?P<d>\d+)', day_month).group('d')
            m = re.search(r'(?P<m>\D+\W*)', day_month).group('m')[1:4]
            h = re.search(r'(?P<d>\d*)', series[1]).group('d')
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
            result = datetime.datetime.strptime(d + '-' + m + '-' + year + ' ' + h + ':00', u'%d-%b-%Y %H:%M')
            wd = dict()
            wd['wth_date'] = result
            match = re.search(r'(?P<d>-\d+.\d+|\d+.\d+)', series[2])
            wd['T'] = float(match.group('d')) if match else -999.0
            match = re.search(r'(?P<d>\d+.\d+)', series[3])
            wd['Po'] = float(match.group('d')) if match else -999.0
            match = re.search(r'(?P<d>\d+.\d+)', series[4])
            wd['P'] = float(match.group('d')) if match else -999.0
            match = re.search(r'(?P<d>\d+)', series[6])
            wd['U'] = float(match.group('d')) if match else 0.0
            match = re.search(r'(?P<d>\d+)', series[8])
            wd['ff10'] = float(match.group('d')) if match else 0.0
            match = re.search(r'(?P<d>\d+)', series[9])
            wd['ff3'] = float(match.group('d')) if match else 0.0
            match = re.search(r'(?P<d>-\d+.\d+|\d+.\d+)', series[23])
            wd['Td'] = float(match.group('d')) if match else -999.0
            match = re.search(r'(?P<d>\d+.\d+)', series[24])
            wd['RRR'] = float(match.group('d')) if match else 0.0
            wd['Wg'] = wnd[series[7]]
            sql.writewheterdata(wd)
        except Exception as exp:
            print(exp)

    if dt.second % 10 == 0:
        try:
            data_insql = insql.read()
            ind = dict()
            gdata = dict()
            ind['an_date'] = data_insql[0][0]
            ind['c4_q'] = data_insql[0][1]
            ind['c5_q'] = data_insql[0][2]
            ind['c6_q'] = data_insql[0][3]
            ind['c7_q'] = data_insql[0][4]
            ind['c8_q'] = data_insql[0][5]
            ind['so2_m'] = data_insql[0][6]
            ind['so2_n'] = data_insql[0][7]
            ind['so2_ug'] = data_insql[0][8]
            ind['rtp'] = int((data_insql[0][9] > 0 if data_insql[0][9] else 0) +
                             (data_insql[0][10] > 0 if data_insql[0][10] else 0) +
                             (data_insql[0][11] > 0 if data_insql[0][11] else 0))
            sql.writeinsqldata(ind)
            data_full = sql.getwheterdata1()
            #cntk = CNTKCassification.CntkClassification('/home/administrator/projects/CNTK/model-som-1g.dnn')
            ktf_n, ktf_m, ktf_ug = ktf.evaluate(data_full)
            if ktf_n is not None and len(ktf_n) > 0:
                gdata['so_n_nr'] = int(np.mean(ktf_n).round())
            if ktf_m is not None and len(ktf_m) > 0:
                gdata['so_m_nr'] = int(np.mean(ktf_m).round())
            if ktf_ug is not None and len(ktf_ug) > 0:
                gdata['so_ug_nr'] = int(np.mean(ktf_ug).round())
            #gdata['so_m_nr'] = int(cntk.evaluate(data_full))
            #gdata['so_n_nr'] = int(cntk.reevaluate('/home/administrator/projects/CNTK/model-son-1g.dnn', data_full))
            #gdata['so_ug_nr'] = int(cntk.reevaluate('/home/administrator/projects/CNTK/model-soug-1g.dnn', data_full))
            print('{M} {N} {UG}', gdata['so_m_nr'], gdata['so_n_nr'], gdata['so_ug_nr'])
            gdata['an_date'] = ind['an_date']
            gdata['so_n_date'] = ind['an_date']
            gdata['so_m_date'] = ind['an_date']
            gdata['so_ug_date'] = ind['an_date']
            gdata['so_m'] = ind['so2_m']
            gdata['so_n'] = ind['so2_n']
            gdata['so_ug'] = ind['so2_ug']
            gdata['so_m_nr_v'] = 0.7
            gdata['so_n_nr_v'] = 0.7
            gdata['so_ug_nr_v'] = 0.7
            sql.writeanalizatordata(gdata)
        except Exception as exp:
            print(exp)

    time.sleep(1)
