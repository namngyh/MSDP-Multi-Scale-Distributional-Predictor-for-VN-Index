# MSDP Report

## Executive summary

This report was generated from saved pipeline outputs. No claim of superiority is made without paired bootstrap evidence.

## Research question

Does horizon-dependent multi-scale expert fusion improve out-of-sample distribution forecasts over simple baselines?

## Data description and quality

Rows: 6306; range: 2000-07-28 to 2026-07-13. Issues: ['OHLC constraint violations: high=27, low=15'].

## Method

Features are causal rolling statistics. Targets are forward 5/20/60-session log returns, realized volatility and path drawdown. Chronological development/calibration/test partitions use a 60-session purge. Scalers are fit on development only. Test observations are never used for tuning or calibration.

The model uses short, medium, long and range-volatility convolutional experts. A horizon-conditioned softmax gate fuses their latent states. Ordered quantiles use positive softplus increments. CQR intervals are calibrated only from the calibration partition.

## Final test results

```json
{
  "h5": {
    "return_mae": 2.2476324474231375,
    "return_rmse": 3.0356450159481487,
    "return_pinball": 0.7495649648263261,
    "spearman": 0.10545937400168501,
    "sign_accuracy": 0.5945652173913043,
    "brier": 0.2451397180557251,
    "log_loss": 0.6833946108818054,
    "balanced_accuracy": 0.537948957315324,
    "f1": 0.6218951241950322,
    "mcc": 0.0763016916221073,
    "mdd_mae": 1.7733092332483669,
    "mdd_pinball": 0.688501512896055,
    "volatility_mae": 12.484167736994507,
    "volatility_rmse": 16.445991416147177,
    "roc_auc": 0.5515118806248815,
    "coverage": 0.8119565217391305,
    "width": 7.499608993530273,
    "winkler": 15.000125728651156,
    "calibrated_interval": {
      "coverage": 0.9228260869565217,
      "width": 10.632250722092692,
      "winkler": 14.227533222785864
    },
    "vs_zero_baseline": {
      "return_mae": 0.12082293830905266,
      "return_pinball": 0.037474941863250844,
      "brier": -0.001585400073463833
    }
  },
  "h20": {
    "return_mae": 4.2142591596117,
    "return_rmse": 5.647823085774389,
    "return_pinball": 1.533537649333684,
    "spearman": 0.22660046703227693,
    "sign_accuracy": 0.6434782608695652,
    "brier": 0.23843878507614136,
    "log_loss": 0.6696116328239441,
    "balanced_accuracy": 0.5915028131772003,
    "f1": 0.6762589928057554,
    "mcc": 0.18196669461129247,
    "mdd_mae": 3.0552670406256213,
    "mdd_pinball": 1.4398194769768822,
    "volatility_mae": 13.714558829904853,
    "volatility_rmse": 16.18567405408177,
    "roc_auc": 0.6027257003121334,
    "coverage": 0.5641304347826087,
    "width": 7.499608993530273,
    "winkler": 40.416085642575325,
    "calibrated_interval": {
      "coverage": 0.8934782608695652,
      "width": 18.51903760915493,
      "winkler": 25.786325544929543
    },
    "vs_zero_baseline": {
      "return_mae": -0.23076824456278366,
      "return_pinball": 0.0013341367412154082,
      "brier": -0.005985228151845878
    }
  },
  "h60": {
    "return_mae": 6.600095415330457,
    "return_rmse": 8.981113411239651,
    "return_pinball": 2.6179937108176454,
    "spearman": 0.25935124029539575,
    "sign_accuracy": 0.7195652173913043,
    "brier": 0.23206916451454163,
    "log_loss": 0.6558867692947388,
    "balanced_accuracy": 0.5521916146916147,
    "f1": 0.6712095400340715,
    "mcc": 0.09944585188455587,
    "mdd_mae": 6.6806454382718465,
    "mdd_pinball": 3.3101451526845453,
    "volatility_mae": 14.371989948977928,
    "volatility_rmse": 15.780892429621531,
    "roc_auc": 0.5926455301455301,
    "coverage": 0.43478260869565216,
    "width": 7.499608993530273,
    "winkler": 80.41425645875952,
    "calibrated_interval": {
      "coverage": 0.9641304347826087,
      "width": 37.76929701934415,
      "winkler": 42.33103571485055
    },
    "vs_zero_baseline": {
      "return_mae": -0.40740289759001413,
      "return_pinball": -0.04039597780494253,
      "brier": -0.005757986334877729
    }
  }
}
```

## Latest forecast

```json
{
  "data_date": "2026-07-13 00:00:00",
  "current_vnindex": 1800.54,
  "horizons": [
    {
      "horizon": 5,
      "probability_positive": 0.5353589653968811,
      "return_quantiles": {
        "5": -2.3011746406555176,
        "25": -1.2388924360275269,
        "50": 0.9359545707702637,
        "75": 3.4642672538757324,
        "95": 5.299813270568848
      },
      "projected_index_quantiles": {
        "5": 1759.579503389597,
        "50": 1817.4713187932969,
        "95": 1898.539113664627
      },
      "calibrated_interval": [
        -3.867495480795224,
        6.866134110708554
      ],
      "mdd_quantiles": [
        -2.794715642929077,
        -2.6225688457489014,
        -1.690586805343628
      ],
      "volatility": 4.0293989181518555,
      "expert_weights": [
        0.24369658529758453,
        0.23314905166625977,
        0.2736705243587494,
        0.24948382377624512
      ],
      "confidence": {
        "score": 79,
        "label": "High"
      },
      "interval_width": 10.733629591503778
    },
    {
      "horizon": 20,
      "probability_positive": 0.5353589653968811,
      "return_quantiles": {
        "5": -2.3011746406555176,
        "25": -1.2388924360275269,
        "50": 0.9359545707702637,
        "75": 3.464266777038574,
        "95": 5.2998127937316895
      },
      "projected_index_quantiles": {
        "5": 1759.579503389597,
        "50": 1817.4713187932969,
        "95": 1898.539113664627
      },
      "calibrated_interval": [
        -7.810888936344455,
        10.809527089420627
      ],
      "mdd_quantiles": [
        -2.794715642929077,
        -2.6225688457489014,
        -1.690586805343628
      ],
      "volatility": 4.0293989181518555,
      "expert_weights": [
        0.24369658529758453,
        0.23314903676509857,
        0.2736705243587494,
        0.24948382377624512
      ],
      "confidence": {
        "score": 83,
        "label": "High"
      },
      "interval_width": 18.62041602576508
    },
    {
      "horizon": 60,
      "probability_positive": 0.5353589653968811,
      "return_quantiles": {
        "5": -2.3011746406555176,
        "25": -1.2388924360275269,
        "50": 0.9359545707702637,
        "75": 3.464266777038574,
        "95": 5.2998127937316895
      },
      "projected_index_quantiles": {
        "5": 1759.579503389597,
        "50": 1817.4713187932969,
        "95": 1898.539113664627
      },
      "calibrated_interval": [
        -17.436018623379507,
        20.43465677645568
      ],
      "mdd_quantiles": [
        -2.794715642929077,
        -2.6225688457489014,
        -1.6905869245529175
      ],
      "volatility": 4.0293989181518555,
      "expert_weights": [
        0.24369658529758453,
        0.23314903676509857,
        0.2736705243587494,
        0.24948382377624512
      ],
      "confidence": {
        "score": 69,
        "label": "Medium"
      },
      "interval_width": 37.870675399835186
    }
  ],
  "interpretation": [
    "The 5-session forecast is primarily influenced by the long expert.",
    "The 20-session forecast is primarily influenced by the long expert.",
    "The 60-session forecast is primarily influenced by the long expert."
  ]
}
```

## Limitations

This is research software, not investment advice. Non-stationarity, limited samples, transaction costs, model/seed sensitivity and time-series dependence constrain interpretation. Conformal coverage is empirical; no iid finite-sample guarantee is claimed. A forecast profile across horizons is not a future price path.

## Conclusion

Conclusions must follow the metrics and uncertainty intervals above. No claim of superiority is made without paired bootstrap evidence.
