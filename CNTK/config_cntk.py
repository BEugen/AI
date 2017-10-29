
config_n = {'path_csv': 'data_so2n-1.csv', 'path_save': 'model-son-1g.dnn'}
config_m = {'path_csv': 'data_so2m-1.csv', 'path_save': 'model-som-1g.dnn'}
config_ug = {'path_csv': 'data_so2ug-1.csv', 'path_save': 'model-soug-1g.dnn'}
class ConfigLearning(object):

    def config(self, ga):
        if 'M' == ga:
            return config_m
        if 'N' == ga:
            return config_n
        if 'UG' == ga:
            return config_ug
        return {}
