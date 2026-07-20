from sklearn.preprocessing import RobustScaler, StandardScaler

def fit_feature_scaler(x, kind="robust"):
    scaler=RobustScaler() if kind=="robust" else StandardScaler(); scaler.fit(x); return scaler

