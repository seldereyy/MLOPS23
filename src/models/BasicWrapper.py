import os
from abc import ABCMeta, abstractmethod

import numpy as np
from src.pickle_utils import load_yaml, pickle_dump

config = load_yaml("src/cnf.yml")
path_to_models = config["path_to_models"]


class WrapModel(metaclass=ABCMeta):
    """
    ABC класс для имплементации общих и новых методов
    """

    @abstractmethod
    def __init__(self):
        """Тут буду передавать саму модель из либ"""
        pass

    def fit(self, X_train, y_train):
        """Model fit"""

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        self.model_.fit(X_train, y_train)

    def predict(self, X_test):
        """Model predict"""
        X_test = np.array(X_test)

        return self.model_.predict(X_test)

    def dump(self, filename):
        """ Dump model """

        os.makedirs(path_to_models, exist_ok=True)
        path=os.path.join(path_to_models, filename)
        pickle_dump(self.model_, path)
