# VIEC_CAN_LAM.md — Việc cần làm sau phiên chat

> Phiên 12/11/2026 (tối, lần 2). Viết theo QT-41 bản mới.
> **Cách đọc:** làm lần lượt từ Bước 1 xuống. Mỗi bước có 5 mục:
> - **Cần có:** những gì phải sẵn sàng trước khi làm (thường là đầu ra của bước trước).
> - **Làm:** thao tác hoặc lệnh, chép và dán được.
> - **Xong khi:** dấu hiệu tự kiểm được.
> - **Nếu không:** cách xử lý khi không ra như vậy.
> - **Ra:** đầu ra của bước, và bước nào sẽ dùng nó.
>
> Gặp chữ **DỪNG** thì không làm tiếp. Mang những thứ được nêu ở đó vào phiên chat.

## Đang ở đâu

- G0 full đã chạy xong: run `20261112_1441_g0_full`, commit `1232ff0`, 2 job đều `ok`. Kết quả đã phân tích trong phiên chat và ghi vào sổ §9 (v0.3).
- **G0 chưa đóng**, vì hai lý do:
  - chưa mức nén nào kéo hành vi về gần ngẫu nhiên (thấp nhất: 3 bit, accuracy 0,79);
  - ô chính bị chọn ở layer 0 tại token chủ ngữ, là ô gần như tầm thường.
- Việc tiếp theo là một lần chạy bổ sung **G0b**, ước 40–60 phút GPU.
- Hạn G0: 22/11/2026.

## Tóm tắt thứ tự

| Bước | Việc | Ước thời gian |
|---|---|---|
| 1 | Lưu kết quả G0 full vào repo (việc còn sót từ lần trước) | 5 phút |
| 2 | Cả nhóm xác nhận quy tắc chọn ô chính mới (D-08). **DỪNG** nếu không đồng ý | 10 phút |
| 3 | Chép 5 file mới vào repo, commit, push | 5 phút |
| 4 | Chạy G0b trên Kaggle bằng Save Version | 40–60 phút chờ, không cần ngồi canh |
| 5 | Tải kết quả, kiểm `run_summary.json` | 5 phút |
| 6 | Lưu kết quả G0b vào repo, ghi nhật ký GPU vào sổ | 10 phút |
| 7 | Mở phiên chat mới, đính kèm 2 file | — |

---

## Bước 1. Lưu kết quả G0 full vào repo

**Cần có:** file `20261112_1441_g0_full.zip` đã tải từ Kaggle (file bạn vừa gửi trong phiên chat).

**Làm:**
```bash
cd <thư mục repo trên máy>
mkdir -p results/20261112_1441_g0_full
unzip <đường dẫn tới>/20261112_1441_g0_full.zip -d results/20261112_1441_g0_full
```
Trên Windows không có `unzip`: tạo thư mục `results\20261112_1441_g0_full`, rồi giải nén zip **vào đúng thư mục đó** bằng trình giải nén bất kỳ.

**Xong khi:** trong `results/20261112_1441_g0_full/` có đúng:
- `run_summary.json` và `kaggle_run.yaml`, nằm ngay trong thư mục này;
- 2 thư mục `g0_full_410m/` và `g0_timing_1b/`, mỗi thư mục có `results.jsonl`, `executed.ipynb`, `summary_behavior.csv`, `summary_reuse.csv`.

**Nếu không:** nếu bị lồng thêm một cấp (ví dụ `results/20261112_1441_g0_full/20261112_1441_g0_full/run_summary.json`), chuyển mọi thứ lên một cấp rồi xoá thư mục rỗng.

**Commit:**
```bash
git add results/20261112_1441_g0_full
git commit -m "[G0] kết quả g0_full (commit 1232ff0)"
git push
```

**Ra:** kết quả G0 full đã nằm trong repo. Repo sạch để Bước 3 commit tiếp mà không lẫn file.

---

## Bước 2. Xác nhận quy tắc chọn ô chính mới (D-08)

**Cần có:** 10 phút để cả TV-A và TV-B đọc đoạn dưới.

**Làm:** đọc và trả lời "đồng ý" hoặc "không".

> **Quy tắc cũ** (bản 1): ô có odds FP lớn nhất, trừ layer cuối. Quy tắc này chọn **layer 0, vùng 1**, tức residual ngay sau khối đầu tiên, tại chính token chủ ngữ. Can thiệp ở đó gần như là thay token chủ ngữ. Phần "mã hoá" của C2 khi đó chỉ gồm 1 trên 24 layer.
>
> **Quy tắc mới:** chỉ xét **vùng cuối** (vùng 5: tân ngữ, là vị trí dự đoán động từ chính), layer 1 tới 22. Chọn **layer sớm nhất** có odds FP ≥ **0,8 ×** odds lớn nhất của vùng 5 trên các layer đó. Ý nghĩa: đây là layer đầu tiên mà phần lớn thông tin về số của chủ ngữ đã được chuyển tới vị trí dự đoán, vượt qua tân ngữ (có thể mang số khác).
>
> Quy tắc này được chốt **sau khi đã thấy** bản đồ thô của G0 (5 layer × 2 vùng), nên sổ ghi là "sau dữ liệu". Từ giờ tới khi có kết quả G0b, không đổi nữa.

**Xong khi:** cả hai đồng ý.

**Nếu không:** **DỪNG.** Không chạy Bước 3–4. Mở phiên chat, nói muốn quy tắc nào (ví dụ ngưỡng 0,5 thay 0,8, hoặc một ô cụ thể). Claude sẽ sửa `configs/kaggle_run.yaml`. Notebook không cần sửa: quy tắc là tham số `MAIN_RULE`, `MAIN_FRAC`, `MAIN_LAYER`.

**Ra:** quy tắc chọn ô chính được chốt trước khi chạy. Bước 3 dùng config đang mã hoá quy tắc này.

---

## Bước 3. Chép 5 file mới vào repo

**Cần có:**
- Bước 1 đã commit.
- Bước 2: cả nhóm đồng ý.
- File `khoaluan_G0b_files.zip` từ phiên chat này.

**Làm:** giải nén `khoaluan_G0b_files.zip` vào **thư mục gốc** của repo, cho phép ghi đè. Zip có sẵn đúng cấu trúc thư mục. Cả 5 file đều **THAY**:

| Đường dẫn | Loại | Đổi gì |
|---|---|---|
| `notebooks/00_g0_pilot.ipynb` | THAY | Bản 2: quy tắc chọn ô chính mới; odds từng cặp và khoảng tin cậy bootstrap theo cụm; học lại nhiều seed; ô kiểm dữ liệu (BOS, tách token, trùng lặp); cấu hình nén dạng `QCONFIGS`. Đã chạy TOY_TEST trên CPU |
| `configs/kaggle_run.yaml` | THAY | 2 job: `g0b_smoke_410m` (nhỏ) rồi `g0b_full_410m`. Bỏ 3 job cũ |
| `docs/VIEC_CAN_LAM.md` | THAY | File này |
| `docs/QUY_TRINH_LAM_VIEC.md` | THAY | QT-41 mới (định dạng file này), QT-30 và QT-31 rõ thứ tự |
| `docs/KHOALUAN_KE_HOACH_THEO_DOI.md` | THAY | Sổ v0.3: §9 điền kết quả G0, thêm D-08 đến D-10, nhật ký GPU, nguồn repo gốc |

Kiểm nhanh:
```bash
git status
```

**Xong khi:** `git status` chỉ báo đúng 5 file trên là `modified`.

**Nếu không:**
- Có file lạ (ví dụ thư mục `khoaluan_G0b/` mới): bạn đã giải nén lồng một cấp. Chuyển nội dung ra gốc repo.
- Có file `src/` hay `g0_pilot.py` cũ: không liên quan, để nguyên.

**Commit:**
```bash
git add notebooks/00_g0_pilot.ipynb configs/kaggle_run.yaml docs/
git commit -m "[G0b] notebook 00 bản 2 + config G0b + sổ v0.3"
git push
```

**Ra:** commit mới trên GitHub. Ở Bước 4, runner Kaggle sẽ clone đúng commit này.

---

## Bước 4. Chạy G0b trên Kaggle

**Cần có:** Bước 3 đã push. Mở GitHub, kiểm commit mới nhất là `[G0b] notebook 00 bản 2 ...`.

**Làm:**
1. Kaggle → mở notebook `runner` (không sửa ô nào; ô CẤU HÌNH giữ như lần trước).
2. Kiểm Settings: Accelerator **GPU T4**, Internet **On**.
3. **Save Version → Save & Run All (Commit)** → Save.
4. Có thể tắt máy. Runner chạy 2 job theo thứ tự:
   - `g0b_smoke_410m`: khoảng 2–3 phút;
   - `g0b_full_410m`: khoảng 35–50 phút.
   Nếu smoke lỗi, job full tự bỏ qua (`stop_on_error: true`).

Ước tổng thời gian phiên: 40–60 phút GPU [PHỎNG ĐOÁN, suy từ t = 7,55 giây/lần học DAS đo ở G0; job full có khoảng 116 ô bản đồ, 9 cấu hình nén, 3 × 5 lần học lại].

**Xong khi:** trang Versions báo version mới **Complete**.

**Nếu không:** version **Failed** (khác với job lỗi bên trong) thường do clone hoặc môi trường. Xem bảng "Gỡ lỗi nhanh" ở cuối file. Sửa xong thì làm lại Bước 4.

**Ra:** tab Output của version có thư mục `outputs/<run_id>/` và file `<run_id>.zip`, với `run_id` dạng `2026MMDD_HHMM_g0b`. Bước 5 dùng file zip này.

---

## Bước 5. Tải kết quả và kiểm `run_summary.json`

**Cần có:** version Complete ở Bước 4.

**Làm:**
1. Tab Output → tải `<run_id>.zip` về máy.
2. Mở `run_summary.json` trong zip, xem trường `status` của 2 job.

**Xong khi:** `g0b_smoke_410m` và `g0b_full_410m` đều `ok`.

**Nếu không:** có job `error`.
- Vẫn làm Bước 6 (lưu vào repo) để giữ dấu vết.
- Ở Bước 7, nói rõ job nào lỗi. Claude sẽ đọc `executed.ipynb` của job đó trong zip.
- Chỉ chuyển sang chạy từng ô (QT-11) khi Claude yêu cầu.

**Ra:** file zip của G0b và trạng thái 2 job. Bước 6 và Bước 7 dùng zip này.

---

## Bước 6. Lưu kết quả G0b vào repo và ghi sổ

**Cần có:** zip từ Bước 5; biết `run_id` (tên zip, bỏ đuôi `.zip`).

**Làm:**
1. Lưu kết quả, giống Bước 1:
   ```bash
   cd <thư mục repo>
   mkdir -p results/<run_id>
   unzip <đường dẫn tới>/<run_id>.zip -d results/<run_id>
   ```
2. Mở `docs/KHOALUAN_KE_HOACH_THEO_DOI.md`, thêm hai dòng.
   - §6 Nhật ký GPU:
     `| <ngày> | <tài khoản> | <run_id> (G0b) | 410M | <tổng phút / 60> | 2 job: <phút smoke> + <phút full> phút |`
   - Bảng "Run đã chạy" ở §9:
     `| <run_id> | <7 ký tự đầu của commit trong run_summary.json> | g0b_smoke_410m / g0b_full_410m | <status> | <phút> |`

   Số phút lấy ở trường `minutes` của mỗi job trong `run_summary.json`.
3. Nếu trước đây bạn đã chạy smoke G0 bản 1 ở một version riêng: thêm dòng cho version đó vào §6, nếu còn số liệu. Không nhớ thì bỏ qua.
4. Commit:
   ```bash
   git add results/<run_id> docs/KHOALUAN_KE_HOACH_THEO_DOI.md
   git commit -m "[G0b] kết quả + nhật ký GPU"
   git push
   ```

**Xong khi:** `results/<run_id>/run_summary.json` có trên GitHub.

**Nếu không:** bị lồng thư mục thì xử lý như Bước 1.

**Ra:** kết quả G0b đã nằm trong repo; sổ có dòng GPU mới. Bước 7 mang zip vào phiên chat.

---

## Bước 7. Mở phiên chat mới

**Cần có:** Bước 6 xong.

**Làm:** mở phiên chat mới trong Project "Khóa Luận", đính kèm 2 file:
1. `docs/VIEC_CAN_LAM.md`, tức file này;
2. `<run_id>.zip` của G0b.

Nhắn một câu, ví dụ: "G0b xong, 2 job ok". Nếu có lỗi, nói job nào lỗi.

**Claude sẽ làm, theo thứ tự:**
1. Đọc `data_check`: BOS, tách token, trùng train/eval, cặp đảo.
2. Áp 4 quy tắc G0 (sổ §4) ở ô chính mới.
3. Chọn lưới nén 3–4 mức theo quy tắc 2, có khoảng tin cậy của T.
4. Kết luận G0 đóng hay chưa, rồi điền sổ §9.
5. Nếu G0 đóng: viết `notebooks/01_tai_lap_causalgym.ipynb` (RQ0) và `VIEC_CAN_LAM.md` mới.

**Ra:** quyết định G0 và kế hoạch chạy tiếp.

---

## Việc song song (không cần GPU)

Làm xen kẽ được, không chặn các bước trên trừ khi có ghi chú.

| Ai | Hạn | Việc | Đầu ra dùng vào đâu |
|---|---|---|---|
| TV-B | 16/11 | Kiểm lại độc lập 8 điểm Claude đã đọc trong repo gốc `aryamanarora/causalgym`, commit `0f3129f` (sổ §8, mục "Repo gốc"). Mở đúng file và dòng ghi ở đó. Ghi "khớp" hoặc "khác" vào sổ §8 | Điều kiện để tin số của notebook 01 (G1) |
| TV-B | sau Bước 6 | Trong `results/<run_id>/g0b_full_410m/results.jsonl`, tìm dòng `"exp": "data_check"`. Kỳ vọng: `first_token_is_eos` = 1.0, `tok_mismatch` = 0, `eval_sentences_in_train` = 0, `eval_swap_frac` = 1.0. Khác thì ghi vào sổ §9 | Bước 7 và notebook 01 |
| Cả hai | 17/11 | G-N: "Cited by" của CausalGym, Ouyang et al., Duan, Makarov trên Google Scholar; tìm "quantization causal abstraction", "quantized distributed alignment search". Ghi trạng thái G-N vào sổ §4 | Cổng G-N |
| TV-A | 18/11 | Đọc Makarov (2610.40055), phần kiểm định tương đương: cách đặt biên tương đương | Chốt biên tương đương của C1 trong SPEC sau G0 |
| TV-A | 18/11 | Tải đúng bài Zhou et al. `2026.findings-acl.1162` (không phải `.642`) | Sổ nguồn §8 |
| TV-A | 18/11 | Kiểm GPT-QModel với `gpt_neox` trên Pythia-70M | C1 (GPTQ 4 bit) |
| TV-A | khi rảnh | Ghi nhận xét GVHD lần 3 vào `NHAN_XET_GVHD.md` | Đề cương |
| TV-A | khi rảnh | Project "Khóa Luận" hiện chỉ có 3 tài liệu. Thêm `NHAN_XET_GVHD.md`, PDF CausalGym, PDF Makarov. Không thêm file này vì nó đổi mỗi phiên | Claude đọc được trong các phiên sau |

## Gỡ lỗi nhanh khi chạy runner

| Triệu chứng | Nguyên nhân hay gặp | Cách xử lý |
|---|---|---|
| `Clone lỗi` với 401/403/404 | Token sai quyền; sai `GITHUB_USER`/`REPO_NAME`; Secret chưa bật cho notebook | Kiểm lại ba thứ đó; token cần quyền Contents: Read-only cho đúng repo |
| Job lỗi `ValueError: Tham số bản 1 không còn dùng` | Đang dùng `kaggle_run.yaml` cũ với notebook bản 2 | Kiểm Bước 3 đã push đúng `configs/kaggle_run.yaml` mới |
| Job lỗi `Không có ô ứng viên ở vùng cuối` | `LAYERS` thiếu layer giữa | Giữ `LAYERS: "all"` cho job full |
| `No such kernel named python3` | Kaggle đổi tên kernel | Thêm ô `!jupyter kernelspec list` vào runner, sửa `kernel_name` |
| Lỗi khi `load_dataset` | Phiên bản `datasets` cũ | Thêm `"datasets>=3"` vào mục `pip:` trong `kaggle_run.yaml`, commit, chạy lại |
| `CUDA out of memory` | Batch đánh giá lớn | Thêm `EVAL_BS: 8` vào `params` của job |
| Không có GPU trong log | Version chạy không có Accelerator | Settings → Accelerator → GPU T4, chạy lại |
