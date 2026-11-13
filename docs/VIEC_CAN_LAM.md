# VIEC_CAN_LAM.md — Việc cần làm sau phiên chat

> Phiên 13/11/2026. Viết theo QT-41 (bản 13/11).
> **Cách đọc:** làm lần lượt từ Bước 1 xuống. Mỗi bước có 5 mục:
> - **Cần có:** những gì phải sẵn sàng trước khi làm.
> - **Làm:** thao tác hoặc lệnh, chép và dán được.
> - **Xong khi:** dấu hiệu tự kiểm được.
> - **Nếu không:** cách xử lý khi không ra như vậy.
> - **Ra:** đầu ra của bước, và bước nào sẽ dùng nó.
>
> Gặp chữ **DỪNG** thì không làm tiếp; mang những thứ được nêu ở đó vào phiên chat.
> Từ phiên này, **không có bước nào bắt bạn điền số vào sổ.** Claude tự cập nhật sổ, nhật ký GPU và bảng run từ zip bạn gửi (QT-44).

## Đang ở đâu

- **G0 đạt (13/11).** Run G0b `20261113_0506_g0b`, commit `b22a2a4`. Claude đã điền kết quả và quyết định vào sổ v0.4 (§4, §6, §9).
- Tiếp theo là **G1: tái lập CausalGym** bằng notebook 01: 4 tác vụ × Pythia 410M và 1B, gói trong 1 version, khoảng 7 giờ GPU [PHỎNG ĐOÁN].
- Trước khi chạy, cả nhóm cần xác nhận D-13: chọn 4 tác vụ và 3 tiêu chí G1.
- Hạn: G-N 17/11; G1 31/12/2026.

## Tóm tắt thứ tự

| Bước | Việc | Ước thời gian |
|---|---|---|
| 1 | Cả nhóm xác nhận D-13 (4 tác vụ + 3 tiêu chí G1). **DỪNG** nếu không đồng ý | 10 phút |
| 2 | Giải nén zip vào repo, commit, push | 5 phút |
| 3 | Chạy G1 trên Kaggle bằng Save Version | khoảng 7 giờ chờ, không cần ngồi canh |
| 4 | Tải zip kết quả, mở phiên chat mới, đính kèm 2 file | 5 phút |

---

## Bước 1. Xác nhận D-13

**Cần có:** 10 phút để cả TV-A và TV-B đọc đoạn dưới (bản đầy đủ: sổ v0.4, D-13 và §4).

**Làm:** đọc và trả lời "đồng ý" hoặc "không".

> **4 tác vụ:**
> - `agr_sv_num_subj-relc` (agreement; đã dùng ở G0, là tác vụ phát triển);
> - `npi_any_subj-relc` (NPI; nghiên cứu trường hợp của bài);
> - `filler_gap_subj` (filler-gap; nghiên cứu trường hợp của bài);
> - `cleft`.
>
> Lý do chọn: 4 họ hiện tượng khác nhau; accuracy trong bài ≥ 0,89 ở cả 410m và 1b, nên còn chỗ để lượng tử hoá làm hỏng.
>
> **Cách chạy:**
> - Pythia 410M và 1B, fp32.
> - Eval trên split `test` của HF, là đúng tập bài gốc dùng.
> - 9 phương pháp: DAS, probe × 2, diff-in-means, PCA, k-means, LDA, ngẫu nhiên, vanilla; thêm tác vụ đối chứng dog-give.
> - Lấy biểu diễn source **đúng vị trí của source**. Code gốc lấy ở vị trí của base; đây là lỗi, sổ §8 điểm 9.
>
> **G1 đạt** khi mỗi model đạt cả 3 tiêu chí:
> 1. Thứ tự phương pháp: Kendall τ ≥ 0,7 so với bài, và DAS đứng đầu.
> 2. Ở ≥ 3/4 tác vụ, vùng khác nhau đầu tiên "xuất hiện" không muộn hơn vùng cuối.
> 3. ≥ 12/16 cặp (tác vụ × {DAS, probe, diff-in-means, vanilla}) có odds bằng 0,5–2 lần số của bài.

**Xong khi:** cả hai đồng ý.

**Nếu không:** **DỪNG.** Mở phiên chat, nói muốn đổi gì (ví dụ thay `cleft` bằng `garden_npz_obj`, hoặc nới tiêu chí). Claude gửi zip mới. Không làm Bước 2–3 với zip này.

**Ra:** thiết kế G1 được chốt trước khi chạy. Bước 3 dùng config đang mã hoá đúng thiết kế này.

---

## Bước 2. Giải nén zip vào repo

**Cần có:** Bước 1 đồng ý; file `khoaluan_G1_files.zip` từ phiên chat này.

**Làm:** giải nén `khoaluan_G1_files.zip` vào **thư mục gốc** của repo, cho phép ghi đè. Zip có sẵn đúng cấu trúc:

| Đường dẫn | Loại | Nội dung |
|---|---|---|
| `results/20261113_0506_g0b/` | THÊM | Kết quả G0b, đúng như zip Kaggle. Nếu repo đã có thì ghi đè, nội dung giống |
| `notebooks/01_tai_lap_causalgym.ipynb` | THÊM | Notebook G1. Đã chạy TOY_TEST trên CPU ở cả hai chế độ vị trí, và kiểm 3 điểm: biểu diễn tính trước khớp cách bắt trực tiếp; vanilla ở layer cuối bằng thay cả câu; DAS giảm loss |
| `notebooks/00b_phan_tich_g0b.ipynb` | THÊM | Phân tích lại G0b trên CPU; tái tạo mọi số G0b trong sổ |
| `configs/kaggle_run.yaml` | THAY | 3 job: `g1_smoke_410m`, `g1_410m`, `g1_1b` |
| `docs/KHOALUAN_KE_HOACH_THEO_DOI.md` | THAY | Sổ v0.4 |
| `docs/DEXUAT_HUONG_B1_DAS.md` | THAY (repo chưa có thì là THÊM) | Đề xuất v0.6 |
| `docs/QUY_TRINH_LAM_VIEC.md` | THAY | Quy trình bản 13/11 (QT-44: Claude tự cập nhật) |
| `docs/VIEC_CAN_LAM.md` | THAY | File này |

Rồi:
```bash
cd <thư mục repo>
git status
git add results/20261113_0506_g0b notebooks configs docs
git commit -m "[G1] notebook 01 + config G1; kết quả G0b; sổ v0.4, đề xuất v0.6"
git push
```

**Xong khi:** `git push` thành công, và trên GitHub commit mới nhất là `[G1] notebook 01 ...`.

**Nếu không:**
- `git status` có thư mục lạ như `khoaluan_G1_files/`: bạn đã giải nén lồng một cấp. Chuyển nội dung ra gốc repo rồi xoá thư mục rỗng.
- File `src/` hay `g0_pilot.py` cũ: không liên quan, để nguyên.

**Ra:** commit mới trên GitHub. Bước 3 clone đúng commit này.

---

## Bước 3. Chạy G1 trên Kaggle

**Cần có:** Bước 2 đã push.

**Làm:**
1. Kaggle → mở notebook `runner` (không sửa ô nào; ô CẤU HÌNH giữ như lần trước).
2. Kiểm Settings: Accelerator **GPU T4**, Internet **On**.
3. **Save Version → Save & Run All (Commit)** → Save.
4. Có thể tắt máy. Runner chạy 3 job theo thứ tự:
   - `g1_smoke_410m`: khoảng 3 phút, cả 4 tác vụ với dữ liệu rất nhỏ;
   - `g1_410m`: khoảng 3 giờ;
   - `g1_1b`: khoảng 3,5–4 giờ.

   Smoke lỗi thì các job sau tự bỏ (`stop_on_error: true`).
5. (Tuỳ chọn) Khoảng 10 phút sau khi bấm Save, mở log của version: thấy `g1_smoke_410m` báo `ok` là yên tâm.

Mỗi job có `MAX_HOURS` (410M: 4 giờ, 1B: 4,5 giờ). Quá giờ thì job dừng trước tác vụ kế tiếp; các tác vụ đã xong vẫn giữ kết quả. Ước tổng khoảng 7 giờ GPU [PHỎNG ĐOÁN, suy từ t của G0/G0b; tác vụ câu dài chưa đo].

**Xong khi:** trang Versions báo version mới **Complete**.

**Nếu không:**
- Version **Failed** (khác với job lỗi bên trong): xem bảng "Gỡ lỗi nhanh" cuối file, sửa xong làm lại Bước 3.
- Version bị dừng ở 12 giờ: vẫn sang Bước 4; Claude xem tác vụ nào đã xong.

**Ra:** tab Output có `<run_id>.zip`, với `run_id` dạng `2026MMDD_HHMM_g1`. Bước 4 dùng file này.

---

## Bước 4. Mở phiên chat mới

**Cần có:** version Complete (hoặc bị dừng) ở Bước 3.

**Làm:**
1. Tab Output → tải `<run_id>.zip`. **Không cần giải nén vào repo:** Claude sẽ đưa `results/<run_id>/` vào zip trả về (QT-30).
2. Mở phiên chat mới trong Project "Khóa Luận", đính kèm:
   - `docs/VIEC_CAN_LAM.md` (file này);
   - `<run_id>.zip`.
3. Nhắn một câu, ví dụ: "G1 xong, chạy bằng tài khoản TV-A". Nếu thấy job lỗi, nói job nào.

**Claude sẽ làm, theo thứ tự:**
1. Kiểm `run_summary.json` và `data_check` từng tác vụ: split `test`, tỉ lệ cặp lệch vị trí (`pos_mismatch_frac`), `tok_mismatch`.
2. Áp 3 tiêu chí G1 cho từng model; kết luận G1 đạt hay chưa.
3. Tự điền sổ (§4, §6, §9), cập nhật đề xuất nếu cần.
4. Nếu G1 đạt: viết SPEC C1/C2 (chốt D-11, D-12, biên tương đương) và notebook 02. Nếu chưa: chẩn đoán, có thể chạy thêm chế độ `POS_MODE: "repo"`.

**Ra:** quyết định G1 và kế hoạch C1.

---

## Việc song song (không cần GPU)

Làm xen kẽ được, không chặn các bước trên. Có kết quả thì **nói trong phiên chat**, Claude ghi vào sổ.

| Ai | Hạn | Việc | Đầu ra dùng vào đâu |
|---|---|---|---|
| TV-B | 16/11 | Kiểm lại độc lập 12 điểm Claude đọc trong repo gốc `aryamanarora/causalgym`, commit `0f3129f` (sổ §8). Quan trọng nhất là điểm 9 (vị trí source bị đảo) và điểm 10 (tập eval = split test). Mở đúng file:dòng ghi trong sổ; báo "khớp" hoặc "khác" cho từng điểm | Điều kiện để tin kết quả G1 |
| Cả hai | 17/11 | G-N: "Cited by" của CausalGym, Ouyang et al., Duan, Makarov, Tanyel & Ayvaz (2611.05033) trên Google Scholar. Tìm thêm "quantization causal abstraction", "quantized distributed alignment search" | Cổng G-N |
| TV-A | 18/11 | Đọc toàn văn Tanyel & Ayvaz (arXiv 2611.05033), nhất là §7.1 và Phụ lục E.1. Claude chưa đọc được toàn văn vì trang bị giới hạn truy cập. Tải PDF lên Project, hoặc gửi trong chat | Đối chiếu G1; cơ sở cho C2 §3.3 |
| TV-A | 18/11 | Đọc Makarov (2610.40055), phần kiểm định tương đương: cách đặt biên tương đương | SPEC C1 |
| TV-A | 18/11 | Tải đúng bài Zhou et al. (Findings ACL 2026, `2026.findings-acl.1162`, arXiv 2604.19884) | Sổ nguồn; C2 |
| TV-A | 18/11 | Kiểm GPT-QModel với `gpt_neox` trên Pythia-70M | C1 (GPTQ 4 bit) |
| TV-A | khi rảnh | Ghi nhận xét GVHD lần 3 vào `NHAN_XET_GVHD.md`; thêm file này và PDF Makarov vào Project | Đề cương; Claude đọc được |
| TV-A | tuỳ chọn, 1 phút | Ô "Instructions" của Project còn ghi "sổ dự án v0.2" và "Nhắc cập nhật sổ dự án". Nếu muốn, sửa thành "sổ dự án v0.4" và "Tự cập nhật sổ dự án (QT-44)" | Khớp quy trình mới |

## Gỡ lỗi nhanh khi chạy runner

| Triệu chứng | Nguyên nhân hay gặp | Cách xử lý |
|---|---|---|
| `Clone lỗi` với 401/403/404 | Token sai quyền; sai `GITHUB_USER`/`REPO_NAME`; Secret chưa bật cho notebook | Kiểm lại ba thứ đó; token cần quyền Contents: Read-only cho đúng repo |
| Log có "Không tải được split 'test' ... Dùng 'validation'" | Thư viện `datasets` không thấy split test | Không cần làm gì ngay; job vẫn chạy trên validation. Báo Claude ở Bước 4 |
| Log có "Thứ tự loại của ... không khớp" | Tên loại trong dữ liệu khác template gốc | Không chặn job; báo Claude ở Bước 4 (ảnh hưởng nhãn dog-give) |
| Lỗi khi `load_dataset` | Phiên bản `datasets` cũ | Thêm `"datasets>=3"` vào mục `pip:` trong `kaggle_run.yaml`, commit, chạy lại |
| `CUDA out of memory` | Batch lớn ở 1B | Thêm `EVAL_BS: 16` và `CAP_BS: 16` vào `params` của job, commit, chạy lại |
| `No such kernel named python3` | Kaggle đổi tên kernel | Thêm ô `!jupyter kernelspec list` vào runner, sửa `kernel_name` |
| Không có GPU trong log | Version chạy không có Accelerator | Settings → Accelerator → GPU T4, chạy lại |
