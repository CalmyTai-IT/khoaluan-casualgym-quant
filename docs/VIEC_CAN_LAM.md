# VIEC_CAN_LAM.md — Việc cần làm sau phiên chat

> Phiên: 12/11/2026 (tối). Claude viết lại file này cuối mỗi phiên (QT-41). Người dùng tick `[x]` khi xong, và có thể thêm hoặc xoá dòng.
> Mục tiêu hiện tại: **qua cổng G0 trước 22/11/2026.**

## 1. Thiết lập repo (một lần)

- [ ] Tạo repo GitHub **private**, ví dụ `khoaluan-causalgym-quant`.
- [ ] Giải nén `khoaluan-causalgym-quant.zip` vào thư mục repo trên máy. Tất cả là file **THÊM**:
  - `README.md`, `.gitignore`
  - `kaggle/runner.ipynb`
  - `configs/kaggle_run.yaml`
  - `notebooks/00_g0_pilot.ipynb`
  - `results/.gitkeep`
  - `docs/QUY_TRINH_LAM_VIEC.md`, `docs/VIEC_CAN_LAM.md`, `docs/KHOALUAN_KE_HOACH_THEO_DOI.md`, `docs/DEXUAT_HUONG_B1_DAS.md`, `docs/PROJECT_INSTRUCTIONS.md`
- [ ] Bỏ file `g0_pilot.py` của lượt trước nếu đã lưu. Notebook `00_g0_pilot.ipynb` thay thế nó.
- [ ] Commit `[setup] khung repo + G0 notebook`, push.

## 2. Thiết lập Kaggle (một lần)

- [ ] GitHub → Settings → Developer settings → Fine-grained tokens → token chỉ cho repo này, quyền **Contents: Read-only**. Copy token.
- [ ] Kaggle → New Notebook → File → Import Notebook → chọn `kaggle/runner.ipynb` trên máy.
- [ ] Settings: Accelerator **GPU T4** (×1); Internet **On**.
- [ ] Add-ons → Secrets → Add `GITHUB_TOKEN` = token, rồi bật cho notebook này.
- [ ] Sửa ô CẤU HÌNH: `GITHUB_USER`, `REPO_NAME`. Quick save.

## 3. Smoke test (đã bật sẵn trong `kaggle_run.yaml`)

- [ ] Kaggle runner → **Save Version → Save & Run All**. Ước khoảng 5–20 phút, gồm cả tải model [PHỎNG ĐOÁN].
- [ ] Tab Output → `outputs/<run_id>/run_summary.json`: job `g0_smoke_410m` phải là `ok`.
- [ ] Nếu `error`: mở `executed.ipynb` của job để xem ô lỗi, rồi mang về phiên chat. Nếu là lỗi môi trường (cài gói, CUDA, RAM), chuyển sang chạy từng ô theo QT-11.

> Dấu hiệu cần dừng lại hỏi trước khi chạy tiếp: accuracy FP dưới khoảng 0.7 (ngưỡng ước lượng; bài gốc báo accuracy trung bình 0.86 cho 410M); odds FP gần 0 ở mọi ô; 8 bit đã làm accuracy tụt mạnh. Các dấu hiệu này thường là lỗi tokenize hoặc lỗi nhãn, không phải kết quả.

## 4. G0 đầy đủ

- [ ] Sửa `configs/kaggle_run.yaml`:
  - `run_name: g0_full`;
  - job `g0_smoke_410m`: `enabled: false`;
  - job `g0_full_410m` và `g0_timing_1b`: `enabled: true`.
- [ ] Commit `[G0] full 410M + timing 1B`, push, rồi Save Version. Ước dưới khoảng 1 giờ GPU [PHỎNG ĐOÁN; smoke sẽ cho số thật].
- [ ] Ghi nhật ký GPU (sổ §6).

## 5. Mang kết quả về

- [ ] Tải `.zip`, giải nén vào `results/<run_id>/`, commit `[G0] kết quả`.
- [ ] Phiên chat mới: đính kèm `run_summary.json`, các `results.jsonl`, `summary_*.csv` và file này. Claude sẽ:
  - điền §9 của sổ;
  - áp 4 quy tắc G0 (sổ §4);
  - đề xuất lưới bit/α;
  - viết notebook tiếp theo (`01_tai_lap_causalgym.ipynb`).

## 6. Song song, không cần GPU

- [ ] (TV-B) Đối chiếu repo `aryamanarora/causalgym`: có BOS không; cách tách token theo vùng; hàm loss DAS; công thức odds. Ghi khác biệt vào sổ.
- [ ] (Cả hai) G-N trước 17/11: "Cited by" của CausalGym, Ouyang et al., Duan, Makarov.
- [ ] Đọc Makarov (2610.40055) phần kiểm định tương đương; tải đúng bài Zhou et al. (`2026.findings-acl.1162`, không phải `.642`).
- [ ] Ghi nhận xét GVHD lần 3 vào `NHAN_XET_GVHD.md`.

## Gỡ lỗi nhanh khi chạy runner

| Triệu chứng | Nguyên nhân hay gặp | Cách xử lý |
|---|---|---|
| `Clone lỗi` với 401/403/404 | Token sai quyền; sai `GITHUB_USER`/`REPO_NAME`; Secret chưa bật cho notebook | Kiểm lại ba thứ đó; token cần quyền Contents: Read-only cho đúng repo |
| `No such kernel named python3` | Kaggle đổi tên kernel | Chạy từng ô (QT-11 d): thêm ô `!jupyter kernelspec list`, rồi sửa `kernel_name` trong runner |
| Lỗi khi `load_dataset` | Phiên bản `datasets` cũ | Thêm `"datasets>=3"` vào mục `pip:` trong `kaggle_run.yaml` |
| Job lỗi `CUDA out of memory` ở 1B | Batch đánh giá quá lớn | Thêm `EVAL_BS: 8` vào `params` của job |
| Không có GPU trong log | Version chạy không có Accelerator | Settings → Accelerator → GPU T4, rồi chạy lại |

## 7. Tạo Claude Project

- [ ] Dán `docs/PROJECT_INSTRUCTIONS.md` vào ô Instructions.
- [ ] Knowledge base:
  - `docs/QUY_TRINH_LAM_VIEC.md`, `docs/KHOALUAN_KE_HOACH_THEO_DOI.md`, `docs/DEXUAT_HUONG_B1_DAS.md`;
  - `NHAN_XET_GVHD.md`;
  - PDF CausalGym và Makarov.
- [ ] Không đưa `VIEC_CAN_LAM.md` vào knowledge base, vì nó đổi mỗi phiên; đính kèm khi mở phiên.
