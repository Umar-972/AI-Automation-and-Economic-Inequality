import numpy as np
class AnalyticsService:
 def summary(self,data):
  return {"count":len(data),"avg":float(np.mean(data))}
