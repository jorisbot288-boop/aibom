import xgboost as xgb
import lightgbm as lgb
from sklearn.datasets import load_iris

data = load_iris()
xgb_model = xgb.XGBClassifier(n_estimators=100)
lgb_model = lgb.LGBMClassifier(n_estimators=100)