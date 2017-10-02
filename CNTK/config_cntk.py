
config_n = {'path_csv': 'data_so2N.csv', 'part': 76552, 'end': 95690, 'path_save': 'model-son.dnn'}
config_m = {'path_csv': 'data_so2M.csv', 'part': 16878, 'end': 21096, 'path_save': 'model-som.dnn'}
config_ug = {'path_csv': 'data_so2UG.csv', 'part': 12331, 'end': 15411, 'path_save': 'model-soug.dnn'}
class ConfigLearning(object):

    def config(self, ga):
        if 'M' == ga:
            return config_m
        if 'N' == ga:
            return config_n
        if 'UG' == ga:
            return config_ug
        return {}
