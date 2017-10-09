MAX_DATA = [[62999.7598805147, 62999.84375, 62553.8267252604, 62987.2067522321, 62738.3566984954, 3.0, 27.5, 786.4,
             100.0, 16.0, 36.0, 23.1, 21.0, 360.0, 0.0]]
MIN_DATA = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -32.7, 722.3, 23.0,
             0.0, 0.0, -36.8, 0.0, 0.0, 0.0]]

MAX_DATA_1 = [[314278.993806503, 3, 27.5, 786.4,
               100.0, 16.0, 36.0, 23.1, 21.0, 360.0]]
MIN_DATA_1 = [[0.0, 0, -32.7, 722.3, 23.0,
               0.0, 0.0, -36.8, 0.0, 0.0]]


class FackeData(object):
    def maxdata(self):
        return MAX_DATA

    def mindata(self):
        return MIN_DATA

    def maxdata1(self):
        return MAX_DATA_1

    def mindata1(self):
        return MIN_DATA_1
