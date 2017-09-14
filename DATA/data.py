from DATA import datasql
from METHEO import htmltotable
from CNTK import  CNTKCassification
import datetime
import time
import re

sql = datasql.GetDataFromPc('sa', 'cproject', '172.31.185.41', 'Runtime')
proxies = {
    "http": "127.0.0.1:3128",
    "https": "127.0.0.1:3128",
}
obj = htmltotable.HtmlTables('http://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0'
                             '%B2_%D0%9D%D0%B8%D0%BA%D0%B5%D0%BB%D0%B5', proxies)
hour = -1
while True:
    dt = datetime.datetime.now()
    if dt.hour != hour:
        try:
            hour = dt.hour
            table = obj.read()[8]
            series = table.Series[1]
            year = re.search(r'(?P<year>\d+)', '').group('year')
            day_month = re.search(r'(?P<dmyear>\d+ \w+)', '').group('dm')
            print(table)
        except Exception as exp:
            print(exp)

    if dt.second % 10 == 0:
        data = sql.read()

    time.sleep(1)
