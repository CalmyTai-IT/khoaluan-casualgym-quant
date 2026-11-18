# Áp quy tắc D-16 cho G1r (Claude, CPU, 16/11/2026)

- Chạy: `python3 d16.py results/20261116_0515_g1r` (Python 3, không cần thư viện ngoài). Kết quả in ra: `d16_output.txt`; bảng số: `g1r_tables.json`.
- Script tính lại odds và selectivity kiểu bài gốc (max theo vùng ở mỗi layer → trung bình qua layer; selectivity = max theo vùng của odds − odds dog-give) từ các dòng `site` trong `results.jsonl`, và kiểm trùng `summary_methods.csv` của notebook 01 (sai lệch < 1e-9 ở mọi ô).
- Số của bài (Table 11–14) và số G1 (`correct`) chép từ sổ v0.7 §10 (2 chữ số); nhãn D-16 chỉ dùng số G1r và số của bài.
- Phiên này Claude không truy cập repo, nên chưa chạy `notebooks/01b_phan_tich_g1.ipynb` với thư mục G1r (QT-32). Đối chiếu bằng notebook 01b để ở phiên tìm hiểu.
