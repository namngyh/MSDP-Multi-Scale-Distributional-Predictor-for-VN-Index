# Hồ sơ dự báo theo khoảng thời gian mới nhất

```json
{
  "data_date": "2026-07-13 00:00:00",
  "current_vnindex": 1800.54,
  "note": "H\u1ed3 s\u01a1 d\u1ef1 b\u00e1o theo kho\u1ea3ng th\u1eddi gian; kh\u00f4ng ph\u1ea3i \u0111\u01b0\u1eddng gi\u00e1 t\u01b0\u01a1ng lai",
  "horizons": [
    {
      "horizon": 5,
      "probability_positive": 0.5258725881576538,
      "return_quantiles": [
        -2.7663979530334473,
        -0.7972712516784668,
        0.5948701500892639,
        1.0365599393844604,
        3.742177963256836
      ],
      "raw_interval": [
        -2.7663979530334473,
        3.742177963256836
      ],
      "calibrated_interval": [
        -4.576669756898527,
        5.5524497671219155
      ],
      "mdd_quantiles": [
        -3.2568535804748535,
        -1.6724845170974731,
        -0.4062780439853668
      ],
      "volatility": 13.190559387207031,
      "expert_weights": [
        0.2172781378030777,
        0.2579295039176941,
        0.270363986492157,
        0.25442835688591003
      ],
      "expert_disagreement": 0.3012348413467407,
      "seed_dispersion": 0.0,
      "confidence": {
        "score": 76,
        "label": "High"
      }
    },
    {
      "horizon": 20,
      "probability_positive": 0.5960896015167236,
      "return_quantiles": [
        -7.024903297424316,
        -0.8801931738853455,
        1.3868260383605957,
        3.3436248302459717,
        7.8552165031433105
      ],
      "raw_interval": [
        -7.024903297424316,
        7.8552165031433105
      ],
      "calibrated_interval": [
        -8.835175101289396,
        9.66548830700839
      ],
      "mdd_quantiles": [
        -7.537947654724121,
        -3.4476380348205566,
        -1.1412017345428467
      ],
      "volatility": 14.985648155212402,
      "expert_weights": [
        0.18763692677021027,
        0.24524153769016266,
        0.3126835823059082,
        0.25443801283836365
      ],
      "expert_disagreement": 0.6235888004302979,
      "seed_dispersion": 0.0,
      "confidence": {
        "score": 69,
        "label": "Medium"
      }
    },
    {
      "horizon": 60,
      "probability_positive": 0.590431272983551,
      "return_quantiles": [
        -12.38461971282959,
        -0.6657103896141052,
        3.7146594524383545,
        7.608800888061523,
        16.386127471923828
      ],
      "raw_interval": [
        -12.38461971282959,
        16.386127471923828
      ],
      "calibrated_interval": [
        -14.19489151669467,
        18.196399275788906
      ],
      "mdd_quantiles": [
        -13.521459579467773,
        -7.405277729034424,
        -2.113604784011841
      ],
      "volatility": 16.27939796447754,
      "expert_weights": [
        0.14174526929855347,
        0.23650872707366943,
        0.3406568467617035,
        0.2810892164707184
      ],
      "expert_disagreement": 1.5356025695800781,
      "seed_dispersion": 0.0,
      "confidence": {
        "score": 57,
        "label": "Medium"
      }
    }
  ],
  "interpretation": [
    "The 5-session forecast is primarily influenced by the long expert.",
    "The 20-session forecast is primarily influenced by the long expert.",
    "The 60-session forecast is primarily influenced by the long expert.",
    "The downside scenario includes a material drawdown."
  ]
}
```
