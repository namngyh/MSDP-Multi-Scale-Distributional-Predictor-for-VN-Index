import numpy as np
from msdp.calibration import StaticCQRCalibrator,RollingCQRCalibrator,conformity_scores

def test_conformity_score_cases_and_interval_expansion():
    lo=np.array([[-1.],[-1.],[-1.]]); hi=np.array([[1.],[1.],[1.]]); y=np.array([[0.],[-2.],[3.]])
    assert np.array_equal(conformity_scores(lo,hi,y).ravel(),[0,1,2])
    c=StaticCQRCalibrator().fit(lo,hi,y); a,b=c.transform(lo,hi)
    assert (c.qhat>=0).all() and (a<=lo).all() and (b>=hi).all()

def test_rolling_does_not_use_unmatured_future_residual():
    r=RollingCQRCalibrator(window=20,horizons=(5,20,60)).seed(np.zeros((3,3)),np.ones((3,3)),np.full((3,3),.5)); before=len(r.history)
    r.update(np.zeros(3),np.ones(3),np.array([2.,2.,2.]),forecast_time=10); r.predict(np.zeros(3),np.ones(3),current_time=14); assert len(r.history)==before
    r.predict(np.zeros(3),np.ones(3),current_time=15); assert len(r.history)==before+1

