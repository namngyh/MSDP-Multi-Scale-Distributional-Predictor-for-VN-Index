# MSDP — Dự báo phân phối đa thang đo cho VN-Index

MSDP là pipeline nghiên cứu dự báo xác suất trực tiếp cho 5, 20 và 60 phiên. Mô hình tạo phân vị lợi suất và drawdown, xác suất lợi suất dương, biến động thực hiện và trọng số bốn chuyên gia theo từng horizon. Đây không phải khuyến nghị đầu tư.

## Cài đặt và chạy trên Windows

```powershell
conda create -n msdp python=3.11 -y
conda activate msdp
pip install -r requirements.txt
python scripts/inspect_data.py --data data/raw/VNINDEX_Daily.csv
pytest -q
python scripts/run_all.py --config configs/quick.yaml --data data/raw/VNINDEX_Daily.csv
python scripts/run_all.py --config configs/default.yaml --data data/raw/VNINDEX_Daily.csv
python scripts/predict_latest.py --config configs/default.yaml --data data/raw/VNINDEX_Daily.csv --model artifacts/models/production_model.pt
```

File đầu vào bắt buộc có `Date`, `Close > 0`; OHLCV còn lại là tùy chọn. Loader không thêm ngày nghỉ, không forward-fill giá và không sửa file gốc. File dữ liệu kèm theo bị thiếu quote quanh dấu phẩy hàng nghìn; parser phục hồi theo ràng buộc OHLC.

## Chống rò rỉ dữ liệu

Feature tại ngày `t` chỉ dùng thông tin đến `t`. Development, calibration và final test được chia theo thời gian, có purge 60 phiên. Median điền thiếu và RobustScaler chỉ fit trên development. Early stopping dùng phần đuôi development đã purge; conformal chỉ fit calibration; test không dùng để chọn mô hình.

Kết quả nằm tại `artifacts/predictions`, metric tại `reports/tables`, hình tại `reports/figures`, báo cáo tại `reports/MSDP_Report_VI.md`. Ba dự báo horizon là hồ sơ dự báo theo kỳ hạn, không phải đường giá tương lai. Coverage conformal chỉ là coverage thực nghiệm cho chuỗi thời gian, không có bảo đảm iid. Chỉ kết luận vượt baseline khi khoảng tin cậy moving-block bootstrap của chênh lệch không chứa 0.

Nếu lệnh `python` mở Microsoft Store, hãy cài Miniconda/Python 3.11 rồi mở lại terminal. `quick.yaml` dùng để smoke test; `default.yaml` tốn nhiều thời gian CPU hơn.

