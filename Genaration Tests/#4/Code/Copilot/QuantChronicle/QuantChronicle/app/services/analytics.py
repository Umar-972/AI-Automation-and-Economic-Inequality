import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class AnalyticsService:
    def anomalies(self, amounts):
        df=pd.DataFrame({"amount":amounts})
        model=IsolationForest(random_state=42)
        return model.fit_predict(df).tolist()
