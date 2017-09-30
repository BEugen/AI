MAX_DATA = [[60000.0, 60000.0, 60000.0, 60000.0, 60000.0, 3, 35.0, 780.0, 100.0,
            30.0, 30.0, 35.0, 20.0, 360]]
MIN_DATA = [[0.0, 0.0, 0.0, 0.0, 0.0, 0, -35.0, 710.0, 0.0,
            0.0, 0.0, -35.0, 0.0, 0]]

MAX_DATA_1 = [[300000.0, 3, 35.0, 780.0, 100.0,
              30.0, 30.0, 35.0, 20.0, 360]]
MIN_DATA_1 = [[0.0, 0, -35.0, 710.0, 0.0,
              0.0, 0.0, -35.0, 0.0, 0]]


class FackeData(object):
    def maxdata(self):
        return MAX_DATA

    def mindata(self):
        return MIN_DATA

    def maxdata1(self):
        return MAX_DATA_1

    def mindata1(self):
        return MIN_DATA_1
