import numpy as np, pandas as pd
from msdp.features import build_features
def test_features_are_causal():
    n=400; z=np.exp(np.arange(n)/1000); d=pd.DataFrame({"close":100*z,"open":100*z,"high":101*z,"low":99*z,"volume":np.arange(n)+100}); a,_=build_features(d); d.loc[301:,"close"]*=2; b,_=build_features(d); pd.testing.assert_series_equal(a.loc[300],b.loc[300])

