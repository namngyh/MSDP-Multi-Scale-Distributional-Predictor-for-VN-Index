# Hồ sơ dự báo theo khoảng thời gian mới nhất

```json
{
  "run_id": "20260720_154038_quick",
  "artifact_role": "production",
  "data_date": "2026-07-13 00:00:00",
  "current_vnindex": 1800.54,
  "horizons": [
    {
      "horizon": 5,
      "probability_positive": 0.480314165353775,
      "return_quantiles": [
        -4.726933479309082,
        -1.796768307685852,
        0.19762763381004333,
        0.6827290058135986,
        3.637368679046631
      ],
      "raw_interval": [
        -4.726933479309082,
        3.637368679046631
      ],
      "calibrated_interval": [
        -6.608065719174705,
        5.518500918912254
      ],
      "projected_index_quantiles": [
        1717.4098261749743,
        1804.1017543172836,
        1867.2377882552146
      ],
      "mdd_quantiles": [
        -3.5209662914276123,
        -1.7600829601287842,
        -0.4343343675136566
      ],
      "volatility": 15.730810165405273,
      "expert_weights": [
        0.2101370096206665,
        0.2828831970691681,
        0.25670868158340454,
        0.25027117133140564
      ],
      "expert_disagreement": 0.3494890332221985,
      "seed_dispersion_return": 0.0,
      "seed_dispersion_direction": 0.0,
      "seed_dispersion_mdd": 0.0,
      "seed_dispersion_volatility": 0.0,
      "confidence_score": 48.03180441111042,
      "confidence_label": "Medium",
      "confidence_components": {
        "interval": 1.0,
        "coverage": 0.005428226779252143,
        "disagreement": 0.3618817852834741,
        "seed": 0.5,
        "drift": 0.4747996898423365
      },
      "confidence_component_sources": {
        "interval": "calibration interval-width percentile",
        "coverage": "calibration coverage",
        "disagreement": "calibration auxiliary disagreement percentile",
        "seed": "calibration seed-dispersion percentiles",
        "drift": "development robust-distance percentile"
      },
      "confidence_missing_components": [],
      "confidence_components_used": [
        "interval",
        "coverage",
        "disagreement",
        "seed",
        "drift"
      ]
    },
    {
      "horizon": 20,
      "probability_positive": 0.5133011341094971,
      "return_quantiles": [
        -11.251998901367188,
        -3.0787031650543213,
        -0.051620811223983765,
        1.6974947452545166,
        6.246392250061035
      ],
      "raw_interval": [
        -11.251998901367188,
        6.246392250061035
      ],
      "calibrated_interval": [
        -14.652476805665792,
        9.64687015435964
      ],
      "projected_index_quantiles": [
        1608.9256023788453,
        1799.6107113826274,
        1916.595795714855
      ],
      "mdd_quantiles": [
        -8.599516868591309,
        -3.9971024990081787,
        -1.3117059469223022
      ],
      "volatility": 17.487215042114258,
      "expert_weights": [
        0.18534375727176666,
        0.2895573377609253,
        0.2719816267490387,
        0.25311729311943054
      ],
      "expert_disagreement": 1.1690932512283325,
      "seed_dispersion_return": 0.0,
      "seed_dispersion_direction": 0.0,
      "seed_dispersion_mdd": 0.0,
      "seed_dispersion_volatility": 0.0,
      "confidence_score": 47.12709994790174,
      "confidence_label": "Medium",
      "confidence_components": {
        "interval": 0.9071170084439083,
        "coverage": 0.005428226779252143,
        "disagreement": 0.5464414957780458,
        "seed": 0.5,
        "drift": 0.4747996898423365
      },
      "confidence_component_sources": {
        "interval": "calibration interval-width percentile",
        "coverage": "calibration coverage",
        "disagreement": "calibration auxiliary disagreement percentile",
        "seed": "calibration seed-dispersion percentiles",
        "drift": "development robust-distance percentile"
      },
      "confidence_missing_components": [],
      "confidence_components_used": [
        "interval",
        "coverage",
        "disagreement",
        "seed",
        "drift"
      ]
    },
    {
      "horizon": 60,
      "probability_positive": 0.5257642865180969,
      "return_quantiles": [
        -19.593111038208008,
        -4.4367146492004395,
        0.8941175937652588,
        4.126744270324707,
        12.643189430236816
      ],
      "raw_interval": [
        -19.593111038208008,
        12.643189430236816
      ],
      "calibrated_interval": [
        -26.8847541457597,
        19.93483253778851
      ],
      "projected_index_quantiles": [
        1480.167775990963,
        1816.711274678707,
        2043.2027036976813
      ],
      "mdd_quantiles": [
        -14.65210247039795,
        -8.426502227783203,
        -2.4420368671417236
      ],
      "volatility": 18.65452766418457,
      "expert_weights": [
        0.14188344776630402,
        0.30110859870910645,
        0.24278181791305542,
        0.3142261505126953
      ],
      "expert_disagreement": 3.3706607818603516,
      "seed_dispersion_return": 0.0,
      "seed_dispersion_direction": 0.0,
      "seed_dispersion_mdd": 0.0,
      "seed_dispersion_volatility": 0.0,
      "confidence_score": 44.82311924826362,
      "confidence_label": "Medium",
      "confidence_components": {
        "interval": 0.6936067551266586,
        "coverage": 0.005428226779252143,
        "disagreement": 0.9819059107358263,
        "seed": 0.5,
        "drift": 0.4747996898423365
      },
      "confidence_component_sources": {
        "interval": "calibration interval-width percentile",
        "coverage": "calibration coverage",
        "disagreement": "calibration auxiliary disagreement percentile",
        "seed": "calibration seed-dispersion percentiles",
        "drift": "development robust-distance percentile"
      },
      "confidence_missing_components": [],
      "confidence_components_used": [
        "interval",
        "coverage",
        "disagreement",
        "seed",
        "drift"
      ]
    }
  ]
}
```
