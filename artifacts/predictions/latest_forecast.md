# Hồ sơ dự báo mới nhất theo kỳ hạn

```json
{
  "run_id": "20260722_154609_gpu",
  "artifact_role": "production",
  "data_date": "2026-07-13 00:00:00",
  "current_vnindex": 1800.54,
  "note": "Hồ sơ dự báo theo khoảng thời gian; độ tin cậy không phải xác suất dự báo đúng",
  "horizons": [
    {
      "horizon": 5,
      "probability_positive": 0.518169105052948,
      "return_quantiles": [
        -5.520383358001709,
        -1.8820565938949585,
        -0.49920010566711426,
        1.1751314401626587,
        3.6174657344818115
      ],
      "raw_interval": [
        -5.520383358001709,
        3.6174657344818115
      ],
      "calibrated_interval": [
        -5.931746248452318,
        4.02882862493242
      ],
      "mdd_quantiles": [
        -4.486928462982178,
        -1.23317551612854,
        -0.3154729902744293
      ],
      "volatility": 14.47845458984375,
      "expert_weights": [
        0.2544335424900055,
        0.2541098892688751,
        0.24690718948841095,
        0.24454934895038605
      ],
      "expert_disagreement": 0.062356945127248764,
      "seed_dispersion_return": 0.6056423783302307,
      "seed_dispersion_direction": 0.06480712443590164,
      "seed_dispersion_mdd": 0.17090018093585968,
      "seed_dispersion_volatility": 1.1692286729812622,
      "confidence_score": 62.0185354123167,
      "confidence_label": "Trung bình",
      "confidence_components": {
        "interval": 0.5223160434258143,
        "coverage": 0.005428226779252143,
        "disagreement": 0.17370325693606756,
        "seed": 0.7738238841978287,
        "drift": 0.4747996898423365
      },
      "confidence_component_sources": {
        "interval": "calibration interval-width percentile",
        "coverage": "calibration coverage (rolling history unavailable)",
        "disagreement": "calibration auxiliary-forecast disagreement percentile",
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
      "probability_positive": 0.527008593082428,
      "return_quantiles": [
        -10.808524131774902,
        -3.9644734859466553,
        -0.9633484482765198,
        2.7699835300445557,
        8.60811710357666
      ],
      "raw_interval": [
        -10.808524131774902,
        8.60811710357666
      ],
      "calibrated_interval": [
        -11.876747815051836,
        9.676340786853594
      ],
      "mdd_quantiles": [
        -10.641020774841309,
        -3.964209794998169,
        -1.274548888206482
      ],
      "volatility": 16.4031925201416,
      "expert_weights": [
        0.24184612929821014,
        0.24454717338085175,
        0.2494492083787918,
        0.2641575038433075
      ],
      "expert_disagreement": 0.2189158797264099,
      "seed_dispersion_return": 1.397296667098999,
      "seed_dispersion_direction": 0.06529323011636734,
      "seed_dispersion_mdd": 0.3864552974700928,
      "seed_dispersion_volatility": 1.2105305194854736,
      "confidence_score": 67.27034482124313,
      "confidence_label": "Trung bình",
      "confidence_components": {
        "interval": 0.503015681544029,
        "coverage": 0.005428226779252143,
        "disagreement": 0.018094089264173704,
        "seed": 0.6697828709288298,
        "drift": 0.4747996898423365
      },
      "confidence_component_sources": {
        "interval": "calibration interval-width percentile",
        "coverage": "calibration coverage (rolling history unavailable)",
        "disagreement": "calibration auxiliary-forecast disagreement percentile",
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
      "probability_positive": 0.5472291707992554,
      "return_quantiles": [
        -19.9241886138916,
        -7.0055999755859375,
        -1.5639313459396362,
        5.731710910797119,
        17.478330612182617
      ],
      "raw_interval": [
        -19.9241886138916,
        17.478330612182617
      ],
      "calibrated_interval": [
        -21.185139556503337,
        18.739281554794353
      ],
      "mdd_quantiles": [
        -18.017385482788086,
        -8.765674591064453,
        -3.390629529953003
      ],
      "volatility": 18.071929931640625,
      "expert_weights": [
        0.22229059040546417,
        0.20085667073726654,
        0.27784156799316406,
        0.2990112006664276
      ],
      "expert_disagreement": 0.6753698587417603,
      "seed_dispersion_return": 2.7139978408813477,
      "seed_dispersion_direction": 0.05087043717503548,
      "seed_dispersion_mdd": 0.9450982213020325,
      "seed_dispersion_volatility": 0.856613278388977,
      "confidence_score": 66.7260143025459,
      "confidence_label": "Trung bình",
      "confidence_components": {
        "interval": 0.5693606755126659,
        "coverage": 0.005428226779252143,
        "disagreement": 0.08805790108564536,
        "seed": 0.48009650180940894,
        "drift": 0.4747996898423365
      },
      "confidence_component_sources": {
        "interval": "calibration interval-width percentile",
        "coverage": "calibration coverage (rolling history unavailable)",
        "disagreement": "calibration auxiliary-forecast disagreement percentile",
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
  ],
  "interpretation": [
    "Dự báo 5 phiên chịu ảnh hưởng lớn nhất từ chuyên gia ngắn hạn.",
    "Dự báo 20 phiên chịu ảnh hưởng lớn nhất từ chuyên gia biên độ–biến động.",
    "Dự báo 60 phiên chịu ảnh hưởng lớn nhất từ chuyên gia biên độ–biến động.",
    "Kịch bản bất lợi chứa mức sụt giảm đáng kể."
  ]
}
```
