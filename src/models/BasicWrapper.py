import os
from abc import ABCMeta, abstractmethod

import numpy as np



class WrapModel(metaclass=ABCMeta):
    """
    ABC класс для имплементации общих и новых методов
    """
    @abstractmethod
    def __init__(self):
        """Тут буду передавать саму модель из либ"""
        pass
    def list_models(self):
        return ['MyLogisticRegression', 'MyXGBoost']
    
    def fit(self, X_train, y_train):
        """Model fit"""

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        self.model_.fit(X_train, y_train)

    def predict(self, X_test):
        """Model predict"""
        X_test = np.array(X_test)

        return self.model_.predict(X_test)
