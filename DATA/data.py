from DATA import datasql
from METHEO import htmltotable
from CNTK import  CNTKCassification
import datetime
import time
import locale
import re

sql = datasql.GetDataFromPc('sa', 'cproject', '172.31.185.41', 'Runtime')
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
       'Ветер, дующий с юго-юго-востока': 112, 'Ветер, дующий с юго-юго-запада': 202,
       'Штиль, безветрие': 0, '': 0}

obj = htmltotable.HtmlTables('http://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0'
                             '%B2_%D0%9D%D0%B8%D0%BA%D0%B5%D0%BB%D0%B5', None)
sql = datasql.SqlLiteBase('/home/eugen/PycharmProjects/WebSOVisu/db.sqlite3')
hour = -1
while True:
    dt = datetime.datetime.now()
    if dt.hour != hour:
        try:
            hour = dt.hour
            table = obj.read()[8]
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
            wd['T'] = float(re.search(r'(?P<d>\d*.\d*)', series[2]).group('d'))
            wd['Po'] = float(re.search(r'(?P<d>\d*.\d*)', series[3]).group('d'))
            wd['P'] = float(re.search(r'(?P<d>\d*.\d*)', series[4]).group('d'))
            wd['U'] = float(re.search(r'(?P<d>\d*)', series[6]).group('d'))
            wd['ff10'] = float(re.search(r'(?P<d>\d*)', series[9]).group('d'))
            wd['ff3'] = float(re.search(r'(?P<d>\d*)', series[10]).group('d'))
            wd['Td'] = float(re.search(r'(?P<d>\d*.\d*)', series[23]).group('d'))
            wd['RRR'] = float(re.search(r'(?P<d>\d*.\d*)', series[24]).group('d'))
            wd['Wg'] = wnd[series[7]]
            sql.writewheterdata(wd)
        except Exception as exp:
            hour = -1
            print(exp)

    if dt.second % 10 == 0:
        data = sql.read()

    time.sleep(1)
