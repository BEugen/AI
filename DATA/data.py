from DATA import datasql
from METHEO import htmltotable
from CNTK import CNTKCassification
import datetime
import time
import locale
import re

# test data format
# k4, k5, k6, k7, k8, rtp, T, P, U, ff, ff10, Td, RRR, Wg
#                      5   6  7  8   9  10    11   12  13
#                  0   1   2  3  4   5  6      7    8   9
# insql = datasql.GetDataFromPc()
# proxies = {
#     "http": "127.0.0.1:3128",
#     "https": "127.0.0.1:3128",
# }

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
                             '%B2_%D0%9D%D0%B8%D0%BA%D0%B5%D0%BB%D0%B5', None)
sql = datasql.SqlLiteBase('/home/eugen/PycharmProjects/WebSOVisu/db.sqlite3')
#sql = datasql.SqlLiteBase('/home/administrator/projects/websovisu/db.sqlite3')
hour = -1
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
            re_search = re.search(r'(?P<d>-\d+.\d+|\d+.\d+)',
                                  '0.0' if not str(series[2]).strip() else series[2]).group('d')
            wd['T'] = float(re_search) if re_search else -999.0
            re_search = re.search(r'(?P<d>\d+.\d+)',
                                  '0.0' if not str(series[3]).strip() else series[3]).group('d')
            wd['Po'] = float(re_search) if re_search else -999.0
            re_search = re.search(r'(?P<d>\d+.\d+)',
                                  '0.0' if not str(series[4]).strip() else series[4]).group('d')
            wd['P'] = float(re_search) if re_search else -999.0
            re_search = re.search(r'(?P<d>\d+)',
                                  '0.0' if not str(series[6]).strip() else series[6]).group('d')
            wd['U'] = float(re_search) if re_search else 0.0
            re_search = re.search(r'(?P<d>\d+)',
                                  '0.0' if not str(series[8]).strip() else series[8]).group('d')
            wd['ff10'] = float(re_search) if re_search else 0.0
            re_search = re.search(r'(?P<d>\d+)',
                                  '0.0' if not str(series[9]).strip() else series[9]).group('d')
            wd['ff3'] = float(re_search) if re_search else 0.0
            re_search = re.search(r'(?P<d>-\d+.\d+|\d+.\d+)',
                                  '0.0' if not str(series[23]).strip() else series[23]).group('d')
            wd['Td'] = float(re_search) if re_search else -999.0
            re_search = re.search(r'(?P<d>\d+.\d+)',
                                  '0.0' if not str(series[24]).strip() else series[24]).group('d')
            wd['RRR'] = float(re_search) if re_search else 0.0
            wd['Wg'] = wnd[series[7]]
            sql.writewheterdata(wd)
        except Exception as exp:
            print(exp)

    # if dt.second % 10 == 0:
    #     try:
    #         data_insql = insql.read()
    #         ind = dict()
    #         gdata = dict()
    #         ind['an_date'] = data_insql[0][0]
    #         ind['c4_q'] = data_insql[0][1]
    #         ind['c5_q'] = data_insql[0][2]
    #         ind['c6_q'] = data_insql[0][3]
    #         ind['c7_q'] = data_insql[0][4]
    #         ind['c8_q'] = data_insql[0][5]
    #         ind['so2_m'] = data_insql[0][6]
    #         ind['so2_n'] = data_insql[0][7]
    #         ind['so2_ug'] = data_insql[0][8]
    #         ind['rtp'] = int((data_insql[0][9] > 0 if data_insql[0][9] else 0) +
    #                          (data_insql[0][10] > 0 if data_insql[0][10] else 0) +
    #                          (data_insql[0][11] > 0 if data_insql[0][11] else 0))
    #         sql.writeinsqldata(ind)
    #         data_full = sql.getwheterdata1()
    #         cntk = CNTKCassification.CntkClassification('/home/administrator/projects/CNTK/model-som-1g.dnn')
    #         gdata['so_m_nr'] = int(cntk.evaluate(data_full))
    #         gdata['so_n_nr'] = int(cntk.reevaluate('/home/administrator/projects/CNTK/model-son-1g.dnn', data_full))
    #         gdata['so_ug_nr'] = int(cntk.reevaluate('/home/administrator/projects/CNTK/model-soug-1g.dnn', data_full))
    #         print('{M} {N} {UG}', gdata['so_m_nr'], gdata['so_n_nr'], gdata['so_ug_nr'])
    #         gdata['an_date'] = ind['an_date']
    #         gdata['so_n_date'] = ind['an_date']
    #         gdata['so_m_date'] = ind['an_date']
    #         gdata['so_ug_date'] = ind['an_date']
    #         gdata['so_m'] = ind['so2_m']
    #         gdata['so_n'] = ind['so2_n']
    #         gdata['so_ug'] = ind['so2_ug']
    #         gdata['so_m_nr_v'] = 0.7
    #         gdata['so_n_nr_v'] = 0.7
    #         gdata['so_ug_nr_v'] = 0.7
    #         sql.writeanalizatordata(gdata)
    #     except Exception as exp:
    #         print(exp)

    time.sleep(1)
