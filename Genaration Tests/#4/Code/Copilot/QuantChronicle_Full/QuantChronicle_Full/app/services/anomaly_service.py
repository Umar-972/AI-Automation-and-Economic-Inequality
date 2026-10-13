import pandas as pd
from sklearn.ensemble import IsolationForest
class AnomalyService:
 def detect(self,values):
  return IsolationForest(random_state=42).fit_predict(pd.DataFrame({"v":values})).tolist()
