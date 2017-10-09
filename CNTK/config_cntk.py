
config_n = {'path_csv': 'data_so2N-2y.csv', 'part': 364856, 'end': 456069, 'path_save': 'model-son-1g.dnn'}
config_m = {'path_csv': 'data_so2M-2y.csv', 'part': 95787, 'end': 119733, 'path_save': 'model-som-1g.dnn'}
config_ug = {'path_csv': 'data_so2UG-2y.csv', 'part': 24353, 'end': 30441, 'path_save': 'model-soug-1g.dnn'}
class ConfigLearning(object):

    def config(self, ga):
        if 'M' == ga:
            return config_m
        if 'N' == ga:
            return config_n
        if 'UG' == ga:
            return config_ug
        return {}
