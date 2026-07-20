import numpy as np
from msdp.calibration import StaticCQRCalibrator,RollingCQRCalibrator
def test_calibration_and_no_future_update():
    lo=np.array([[-1.],[-1.]]); hi=np.array([[1.],[1.]]); y=np.array([[0.],[2.]]); c=StaticCQRCalibrator().fit(lo,hi,y); a,b=c.transform(lo,hi); assert (a<=lo).all() and (b>=hi).all(); r=RollingCQRCalibrator().seed(lo,hi,y); before=len(r.history); r.predict(np.array([0.]),np.array([1.])); assert len(r.history)==before

