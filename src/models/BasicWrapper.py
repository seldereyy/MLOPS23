import os
import pickle
import sys
from abc import ABCMeta, abstractmethod

sys.path.append("/Users/user/HSE/ml_ops/src/ml_ops_1/")
import numpy as np
from utils import load_yaml

config = load_yaml("/Users/user/HSE/ml_ops/src/ml_ops_1/cnf.yml")
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
        if filename[-4:] != ".pkl":
            filename += ".pkl"
        os.makedirs(path_to_models, exist_ok=True)

        with open(os.path.join(path_to_models, filename), "wb") as f:
            pickle.dump(self.model_, f)
