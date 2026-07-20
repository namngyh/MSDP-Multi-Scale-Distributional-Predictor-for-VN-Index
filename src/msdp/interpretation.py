import numpy as np

EXPERTS=["short","medium","long","range_vol"]
def confidence_score(width_percentile,coverage_error,disagreement,seed_dispersion=0,drift=0):
    penalty=.30*width_percentile+.25*min(1,coverage_error/.1)+.20*disagreement+.10*seed_dispersion+.15*drift; score=int(round(100*(1-min(1,penalty)))); return score,"High" if score>=70 else "Medium" if score>=40 else "Low"
def interpret(horizons,p_up,weights,width_percentile=None,mdd_q10=None):
    notes=[]
    if p_up[0]<.45 and p_up[-1]>.60: notes.append("Short-term signal is negative while the longer-term outlook leans positive.")
    for j,h in enumerate(horizons): notes.append(f"The {h}-session forecast is primarily influenced by the {EXPERTS[int(np.argmax(weights[j]))]} expert.")
    if width_percentile is not None and width_percentile>.8: notes.append("Forecast uncertainty is higher than most of its history.")
    if mdd_q10 is not None and np.min(mdd_q10)<-10: notes.append("The downside scenario includes a material drawdown.")
    return notes

