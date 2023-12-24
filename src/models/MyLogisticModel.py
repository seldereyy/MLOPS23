import numpy as np
from .BasicWrapper import WrapModel
from sklearn.linear_model import LogisticRegression as LR


class MyLogisticRegression(WrapModel):
    def __init__(self, **kwargs):
        self.model_ = LR(**kwargs)
        super().__init__
