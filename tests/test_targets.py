import numpy as np, pandas as pd
from msdp.targets import build_targets
def test_target_alignment_and_mdd():
    c=[100,110,105,120,90,95]; t=build_targets(pd.DataFrame({"close":c}),[5]); assert np.isclose(t.loc[0,"return_h5"],100*np.log(.95)); assert np.isclose(t.loc[0,"mdd_h5"],-25.0)

