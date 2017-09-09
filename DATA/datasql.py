import pyodbc
import sqlite3 as lite


class GetDataFromPc(object):
    def __init__(self, login, psw, host, dbase):
        self.psw = psw
        self.login = login
        self.host = host
        self.dbase = dbase

    def read(self):
        driver = '{ODBC Driver 13 for SQL Server}'
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=1433;SERVER=' + self.host + ';PORT=1443;DATABASE=' + self.dbase + ';UID=' +
            self.login + ';PWD=' + self.psw)
        cursor = cnxn.cursor()
        cursor.execute('select GetDate(), (SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'Converter4_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'DELTA\') as c4_q,'
                       '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'Converter5_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'DELTA\') as c5_q,'
                       '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'Converter6_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'DELTA\') as c6_q,'
                       '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'Converter7_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'DELTA\') as c7_q,'
                       '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'Converter8_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'DELTA\') as c8_q,'
                       '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'Flue_SO2_Molodejniy\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'DELTA\') as SO2_M,'
                       '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'Flue_SO2_Nagornaya\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'DELTA\') as SO2_N,'
                       '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'Flue_SO2_UGMS\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'DELTA\') as SO2_UG,'
                       '(SELECT CAST([Value] as int) & 67108864 FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'ShiberLocalRemote_RTP3\'  AND [DateTime] >= GetDate() AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as RTP3,'
                       '(SELECT CAST([Value] as int) & 67108864 FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'ShiberLocalRemote_RTP4\'  AND [DateTime] >= GetDate() AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as RTP4,'
                       '(SELECT CAST([Value] as int) & 1 FROM Runtime.dbo.v_AnalogHistory'
                       'WHERE [TagName] = \'P5_mess_Furnace\'  AND [DateTime] >= GetDate() AND'
                       '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as RTP5'
                       'from #tmpr')
        return cursor.fetchall()


class SqlLiteBase(object):
    def __init__(self, base_path):
        self.base = base_path

    def writedata(self, data):
        try:
            con = lite.connect(self.base)
            cur = con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')

        except lite.DatabaseError as err:
            print("Error: ", err)

        finally:
            if con:
                con.close()