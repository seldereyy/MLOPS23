from .BasicWrapper import WrapModel
from xgboost import XGBClassifier


class MyXGBoost(WrapModel):
    def __init__(self, **kwargs):
        self.model_ = XGBClassifier(**kwargs)
        super().__init__
