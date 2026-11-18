# G-N: kết quả notebook 96 và xếp loại của Claude (16/11/2026)

- Notebook 96 chạy lúc 2026-11-16 08:05 UTC; 1449 bài sau gộp; 16 lỗi (9 tra bài + 7 truy vấn trên Semantic Scholar, chủ yếu do giới hạn tốc độ).
- File: `seeds.jsonl`, `candidates_dedup.jsonl`, `errors.jsonl`, `tom_tat.json` (chép từ `96_gn_tra_cuu.zip`). Không chép `candidates.jsonl` (trước khi gộp, trùng nội dung) và `raw/` (phản hồi gốc nén, khoảng 2 MB): hai thứ này còn trong zip gốc, nên giữ zip.
- `phan_loai.py` → `phan_loai_claude.csv`: loại của từng bài và lý do. Cách đọc mô tả trong đầu script và trong `docs/GN_TRA_CUU.md` §5.
- Kết luận: không bài nào trùng C1, C2, C3b. Chi tiết và giới hạn: `docs/GN_TRA_CUU.md`, sổ v0.8 §4.
