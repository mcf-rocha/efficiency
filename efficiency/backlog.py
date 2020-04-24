import numpy as np

class Backlog:
    #TODO: __features could be a pandas data frame so as to eliminate all "for" loops.
    def __init__(self, features):
        self.__features = features
        self.__set_features_adjacent_list(features)
        self.__start_node = features['start_node']

    @property
    def features(self):
        return self.__features

    @features.setter
    def features(self, features):
        self.__features = features

    @property
    def features_adjacent_list(self):
        return self.__features_adjacent_list

    def __get_requirements(self, n):
        for k in self.__features['features']:
            if k['id'] == n:
                return k['requirements']

    def __get_benefits(self, n):
        for k in self.__features['features']:
            if k['id'] == n:
                return k['benefits']

    def get_total_requirements(self, features):
        total = []
        for n in features:
            total = np.sum([self.__get_requirements(n), total], axis=0)
        #print('********* The total requirements for', features, 'are', total)
        return total.tolist()

    def get_total_benefits(self, features):
        total = []
        for n in features:
            total = np.sum([self.__get_benefits(n), total], axis=0)
        #print('********* The total benefits of', features, 'are', total)
        return total.tolist()


    def __set_features_adjacent_list(self, features):
        self.__features_adjacent_list = []
        if features['features']:
            for f in features['features']:
                if f['adj_list']:
                    for j in f['adj_list']:
                        t = f['id'], j
                        self.__features_adjacent_list.append(t)
        else:
            raise Exception('Features parameter must be a dict with specific format.')

    @property
    def start_node(self):
        return self.__start_node