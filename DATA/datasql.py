import pyodbc
import sqlite3 as lite


class GetDataFromPc(object):
    def __init__(self, login, psw, host, dbase):
        self.psw = psw
        self.login = login
        self.host = host
        self.dbase = dbase

    def read(self):
        driver = '{FreeTDS}'
        cnxn = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + self.host + ';PORT=1433;DATABASE=' + self.dbase + ';UID=' +
            self.login + ';PWD=' + self.psw)
        cursor = cnxn.cursor()
        cursor.execute('select GetDate(), (SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'Converter4_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as c4_q,'
                        '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'Converter5_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as c5_q,'
                        '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'Converter6_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as c6_q,'
                        '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'Converter7_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as c7_q,'
                        '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'Converter8_Q\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as c8_q,'
                        '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'Flue_SO2_Molodejniy\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as SO2_M,'
                        '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'Flue_SO2_Nagornaya\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as SO2_N,'
                        '(SELECT AVG([Value]) FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'Flue_SO2_UGMS\'  AND [DateTime] > DATEADD(mi, -2, GetDate()) AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\') as SO2_UG,'
                        '(SELECT TOP 1 CAST([Value] as int) & 67108864 FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'ShiberLocalRemote_RTP3\'  AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\' order by '
                        '[DateTime] desc) as RTP3,'
                        '(SELECT TOP 1 CAST([Value] as int) & 67108864 FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'ShiberLocalRemote_RTP4\'  AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\' order by '
                        '[DateTime] desc) as RTP4,'
                        '(SELECT TOP 1 CAST([Value] as int) & 1 FROM Runtime.dbo.v_AnalogHistory'
                        ' WHERE [TagName] = \'P5_mess_Furnace\' AND'
                        '[DateTime] <= GetDate() AND  wwResolution = 1000 AND wwRetrievalMode = \'CYCLIC\' order by '
                        '[DateTime] desc) as RTP5')
        return cursor.fetchall()


class SqlLiteBase(object):
    def __init__(self, base_path):
        self.base = base_path

    def writeanalizatordata(self, data):
        try:
            con = lite.connect(self.base)
            cur = con.cursor()
            cur.execute('insert into sovisu_analizatordata (an_date, '
                                    'so_m, so_n, so_ug, so_n_date, '
                                    'so_m_date, so_ug_date, so_m_nr, '
                                    'so_n_nr, so_ug_nr, so_m_nr_v, '
                                    'so_n_nr_v, o_ug_nr_v)'
                        'VALUES (:an_date,:so_m, :so_n, :so_ug, :so_n_date, '
                                    ':so_m_date, :so_ug_date, :so_m_nr, '
                                    ':so_n_nr, :so_ug_nr, :so_m_nr_v, '
                                    ':so_n_nr_v, :so_ug_nr_v)', data)

        except lite.DatabaseError as err:
            print("Error: ", err)

        finally:
            if con:
                con.close()