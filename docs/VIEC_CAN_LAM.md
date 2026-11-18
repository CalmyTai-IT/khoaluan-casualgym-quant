# VIEC_CAN_LAM.md — Việc cần làm sau phiên chat

> Phiên 16/11/2026 (lần 2). Viết theo QT-41. Thay bản 16/11 (lần 1).
> **Cách đọc:** làm lần lượt từ Bước 1 xuống. Mỗi bước có 5 mục: **Cần có**, **Làm**, **Xong khi**, **Nếu không**, **Ra**. Gặp chữ **DỪNG** thì không làm tiếp; mang những thứ được nêu ở đó vào phiên chat.
> Không có bước nào bắt bạn điền số vào sổ (QT-44). Claude không ghi gì lên Project; bạn tự tải theo bảng "Cho KB" ở cuối câu trả lời của Claude (QT-45).
> **Nhịp mới (D-18):** chậm lại. Bước 1–2 chỉ là lưu file. Bước 3–4 không gấp. Bước 5 là phiên tìm hiểu code và phương pháp; chưa viết SPEC C1.

## Đang ở đâu

- **G1r xong:** lỗi vị trí của repo gốc giải thích hết phần lệch ở `agr_sv_num_subj-relc`, nhưng không giải thích phần lệch của mean/PCA/k-means ở `cleft` (nhãn D-16 đặt trước: 6/12, "Không giải thích được"). G1 vẫn đạt; C1 không bị ảnh hưởng (DAS, vanilla khớp bài ở cả hai chế độ). Sổ v0.8 §10.
- **Phiếu TV-B 17/17 Khớp; G-N đạt** (1449 bài, không bài trùng); **thầy duyệt CausalGym**, MVP thu về RQ0 + C1 + C2, C3b thành mở rộng (D-17).
- **Notebook 97 chưa có kết quả** (chạy nhầm trên CPU, và lỗi numpy sau khi cài). Không gấp: chỉ cần trước khi viết SPEC C1.
- Hạn gần nhất: đề cương 23–30/11. G2 (C1 + C2): 28/02/2027.

## Tóm tắt thứ tự

| Bước | Ai | Việc | Hạn | Thời gian |
|---|---|---|---|---|
| 1 | TV-A | Giải nén zip phiên này vào repo, commit, push | 17/11 | 10 phút |
| 2 | TV-A | Cập nhật KB theo bảng "Cho KB"; sửa ô Instructions của Project | 17/11 | 10 phút |
| 3 | TV-A hoặc TV-B | (Không gấp) Chạy lại notebook 97: bật GPU T4, khởi động lại kernel sau ô 1 | Trước phiên viết SPEC C1 | 20 phút, khoảng 0,25 giờ GPU [PHỎNG ĐOÁN] |
| 4 | TV-A | (Tuỳ chọn) Tải PDF Varshney 2609.30275 lên Project | Trước đề cương | 2 phút |
| 5 | TV-A (+ TV-B nếu được) | **DỪNG**: mở phiên tìm hiểu với Claude | Khi sẵn sàng | 1 phiên |

Bước 3 và 4 làm lúc nào cũng được, trước hoặc sau Bước 5.

---

## Bước 1. Giải nén zip vào repo

**Cần có:** file `khoaluan_16_11_lan2.zip` từ phiên này. Commit `243e926` (zip phiên 16/11 lần 1) đã có trên GitHub.

**Làm:** giải nén `khoaluan_16_11_lan2.zip` vào **thư mục gốc** của repo, cho phép ghi đè. Rồi:
```bash
cd <thư mục repo>
git status
git add results docs configs
git commit -m "[G1r] ket qua G1r + D-16; G-N dat; phieu TV-B; nhan xet GVHD lan 3; so v0.8"
git push
```

**Xong khi:** trên GitHub, commit mới nhất là `[G1r] ket qua G1r ...`, và thấy:
- `results/20261116_0515_g1r/run_summary.json`;
- `results/20261116_gn_tra_cuu/phan_loai_claude.csv`;
- `docs/NHAN_XET_GVHD_LAN3.md`;
- dòng 3 của `docs/KHOALUAN_KE_HOACH_THEO_DOI.md` ghi `Version: v0.8`;
- `configs/kaggle_run.yaml` có `run_name: none` và mọi job `enabled: false`.

**Nếu không:**
- `git status` có thư mục lạ như `khoaluan_16_11_lan2/`: Windows đã giải nén lồng một cấp. Chuyển nội dung ra gốc repo rồi xoá thư mục rỗng.
- `docs/PHIEU_KIEM_REPO_GOC.md` đổi thành bản có cột TV-B đã điền: đúng ý, đó là bản cần lưu.
- File khác không có trong bảng file cuối trang: không liên quan, để nguyên.

**Ra:** commit mới trên GitHub. Bước 5 dùng (Claude đọc repo).

---

## Bước 2. Cập nhật KB và ô Instructions của Project

**Cần có:** các file trong thư mục `docs/` của zip.

**Làm:**
1. Làm theo bảng **"Cho KB"** ở cuối câu trả lời của Claude (thay, thêm, xoá từng file).
2. Mở ô **Instructions** của Project, sửa 3 chỗ:
   - Trong đoạn "MVP gồm:", **xoá** dòng `C3b QiD ở mức cơ chế qua các checkpoint Pythia.`
   - Dòng `Target: C3 "vào sau, ra trước" (LIFO), C4 so sánh bộ lượng tử hoá.` **thay bằng**:
     `Mở rộng (nếu còn thời gian, theo GVHD 16/11): C3b QiD ở mức cơ chế qua các checkpoint Pythia. Target: C3 "vào sau, ra trước" (LIFO), C4 so sánh bộ lượng tử hoá.`
   - Dòng `2. Nhắc cập nhật sổ dự án: ...` **thay** chữ `Nhắc cập nhật sổ dự án` bằng `Claude tự cập nhật sổ dự án (QT-44)`.

**Xong khi:** mục tài liệu của Project có sổ v0.8 và không còn `HUONG_DAN_VIEC_14_18_11.md`; ô Instructions không còn C3b trong MVP.

**Nếu không:** Project báo trùng tên khi tải: xoá bản cũ trước, rồi tải bản mới.

**Ra:** KB và Instructions khớp sổ v0.8. Bước 5 dùng.

---

## Bước 3. (Không gấp) Chạy lại notebook 97 trên GPU

**Vì sao:** D-15 (đường GPTQ cho C1) chờ kết quả này; chỉ cần có trước phiên viết SPEC C1.
**Lần trước (16/11) hỏng vì hai lý do:** session không có GPU (ô 1 in `gpu: CPU`, torch bản `+cpu`); và ô 2 báo `'numpy.ufunc' object has no attribute '__module__'`, do `pip install` ở ô 1 đổi numpy trên đĩa trong khi numpy cũ đã nằm trong bộ nhớ. Chi tiết: `results/20261116_nb97_loi/GHI_CHU.md`.

**Cần có:** commit từ Bước 1 (hoặc commit cũ, notebook 97 không đổi); tài khoản Kaggle còn quota GPU và không có version GPU nào đang chạy.

**Làm (từng ô — QT-11 trường hợp b: lỗi cài thư viện, có thể phải thử nhiều lần):**
1. Kaggle → New Notebook → File → Import `notebooks/97_kiem_gptqmodel.ipynb`.
2. Settings: Accelerator **GPU T4**, Internet **On**. Giữ tham số mặc định.
3. Chạy **ô 1**. Đọc dòng phiên bản: `gpu` phải là `Tesla T4`.
4. Nếu ô 1 in "CẢNH BÁO: cài GPT-QModel đã đổi torch": dừng, chụp ô 1, Stop session, mang ảnh vào phiên Claude kế tiếp.
5. **Khởi động lại kernel**: menu **Run → Restart** (hoặc nút khởi động lại kernel). **Không** bấm Stop session, vì sẽ mất thư viện vừa cài.
6. Chạy lại **ô 1** (lần này pip gần như không cài gì), rồi chạy lần lượt **ô 2 tới ô 8**.
7. Xong thì **Stop session**.

**Xong khi:** `outputs/97_kiem_gptqmodel/kiem_gptqmodel.jsonl` có dòng `ppl` với 4 giá trị fp, rtn, gptq, gptq_alpha_0.5.

**Nếu không:**
- Ô 1 vẫn in `gpu: CPU`: Accelerator chưa bật. Bật lại trong Settings (session sẽ khởi động lại), chạy lại từ ô 1.
- Ô 2 vẫn báo lỗi numpy sau khi đã khởi động lại kernel: chụp ô 1 (lần chạy sau khi khởi động lại) và traceback ô 2. Không tự sửa notebook.
- Ô 1 chạy rất lâu: chờ tối đa 20 phút; quá thì Stop session và ghi lại. [PHỎNG ĐOÁN: GPT-QModel 7.6.0 chỉ có bản mã nguồn, trên máy GPU có thể phải biên dịch]
- Lỗi ở `qm.save()` nhắc `lm_head.weight`: kiểm `offload_to_disk=False` có trong ô 5 chưa.
- Lỗi khác: chụp traceback.

**Ra:** `kiem_gptqmodel.jsonl` (tab Output) + ảnh ô 1 → mang vào phiên Claude kế tiếp; dùng để chốt D-15.

---

## Bước 4. (Tuỳ chọn) Tải PDF Varshney lên Project

**Vì sao:** bài lân cận gần nhất G-N tìm được (null đo ngay trong model đã lượng tử hoá, tức tiền lệ cho null hai phía của nhóm). Claude mới đọc tóm tắt. Nên đọc toàn văn trước khi viết phần "khác biệt với công trình liên quan" của đề cương.

**Cần có:** Internet.

**Làm:** tải `https://arxiv.org/pdf/2609.30275` và thêm vào mục Files của Project.

**Xong khi:** PDF hiện trong Files của Project.

**Nếu không:** arXiv không tải được: gửi link trang tóm tắt cho Claude và ghi lại lỗi.

**Ra:** PDF trong Project → Claude đọc ở phiên tìm hiểu hoặc khi viết đề cương.

---

## Bước 5. DỪNG: phiên tìm hiểu với Claude

**Cần có:** Bước 1 xong (repo có commit mới).

**Mang vào phiên:**

| Thứ cần mang | Ghi chú |
|---|---|
| `docs/VIEC_CAN_LAM.md` (file này) | Như mọi phiên |
| Quyền đọc code | Khi Claude xin gắn repo `CalmyTai-IT/khoaluan-amnesic` (chỉ đọc), chọn đồng ý. Hoặc đính kèm `notebooks/00_g0_pilot.ipynb`, `notebooks/01_tai_lap_causalgym.ipynb`, `notebooks/01b_phan_tich_g1.ipynb`. Phiên 16/11 lần 2 bạn đã từ chối gắn repo nên Claude chỉ làm từ sổ và file bạn gửi; phiên tìm hiểu thì cần code |
| Kết quả Bước 3 | Nếu đã chạy |
| Câu hỏi của bạn | Chỗ nào trong code hoặc trong sổ bạn chưa hiểu |

Nhắn một câu, ví dụ: "Phiên tìm hiểu; cho đọc repo; câu hỏi của tôi là …".

**Gợi ý chương trình** (đổi tuỳ ý):
1. Một cặp dữ liệu CausalGym thật: base, src, vùng, nhãn; odds đo cái gì.
2. DAS trong notebook 00/01: hướng 1D, phép can thiệp, hàm mất mát; vanilla khác DAS chỗ nào; vì sao DAS cao hơn vanilla khoảng 2 lần.
3. Các phương pháp còn lại (probe, mean, PCA, k-means, LDA) học từ dữ liệu nào; lỗi vị trí chạm vào chúng thế nào; đọc kết quả G1r.
4. G0b: T, R, T_rel, sàn step0, |cos| giữa seed nghĩa là gì; vì sao có D-11 và D-12.
5. Lượng tử hoá giả lập: RTN g = 128, α; GPTQ khác RTN chỗ nào (D-15).
6. C1 và C2 sẽ đo gì; ba nhãn; null hai phía; biên tương đương (nối với ý 3 của thầy).

**Bài tập kiểm chứng trong phiên** (CPU, khoảng 10 phút, tự làm): chạy `notebooks/01b_phan_tich_g1.ipynb` trên máy cá nhân với thư mục `results/20261116_0515_g1r/`, xem nhãn D-16 có ra 6/12 như sổ §10 không. Claude chỉ tham số khi đã đọc notebook.

**Ra:** bạn nắm và tự kiểm được pipeline; nhóm quyết định khi nào viết SPEC C1.

---

## Việc không cần GPU, không chặn bước nào

| Ai | Hạn | Việc | Đầu ra dùng vào đâu |
|---|---|---|---|
| TV-A | 23–30/11 | Đề cương theo mẫu FIT; gửi thầy các câu hỏi còn lại ở sổ §7 (4, 5, 6) | Đề cương |
| Một người | Trước khi nộp đề cương | Chạy lại notebook 96 (Kaggle CPU, bật Internet, Run All, Stop session) để lấp phần Semantic Scholar bị giới hạn tốc độ lần này; mang `96_gn_tra_cuu.zip` vào chat | Cập nhật G-N cho đề cương |
| TV-A | Khi tiện | Giữ lại `96_gn_tra_cuu.zip` gốc (có thư mục `raw/`, không đưa vào repo) | Phân tích lại G-N nếu cần |
| TV-A | Khi tiện | Gửi sổ đề tài cũ nếu muốn Claude đóng lên v1.4 | Lưu trữ |

## File trong zip phiên này

| Đường dẫn | THAY/THÊM | Nội dung |
|---|---|---|
| `results/20261116_0515_g1r/` | THÊM | Kết quả G1r, đúng như zip Kaggle |
| `results/20261116_claude_cpu_d16/` | THÊM | Script Claude áp D-16 (`d16.py`), kết quả in ra, bảng số |
| `results/20261116_gn_tra_cuu/` | THÊM | Dữ liệu notebook 96 (trừ `raw/` và `candidates.jsonl`), `phan_loai.py`, `phan_loai_claude.csv` (loại và lý do cho 1449 bài) |
| `results/20261116_tvb_nb98/` | THÊM | `kiem_repo_goc.jsonl` của TV-B, kết quả ô 6 (`diem9_pyvene.json`) |
| `results/20261116_nb97_loi/` | THÊM | Ảnh ô 1, traceback ô 2, chẩn đoán |
| `docs/KHOALUAN_KE_HOACH_THEO_DOI.md` | THAY | Sổ v0.8 |
| `docs/VIEC_CAN_LAM.md` | THAY | File này |
| `docs/PHIEU_KIEM_REPO_GOC.md` | THAY | Bản TV-B đã điền (nguyên văn) |
| `docs/GN_TRA_CUU.md` | THAY | §5 đã điền; thêm §6 kết luận, §7 giới hạn |
| `docs/GHI_CHU_BAI_BAO.md` | THAY | §1–§3 cập nhật; §4 xác nhận Chang et al.; thêm §5 bài lân cận từ G-N |
| `docs/NHAN_XET_GVHD_LAN3.md` | THÊM | Nguyên văn ý kiến lần 3 của thầy và hệ quả cho kế hoạch |
| `configs/kaggle_run.yaml` | THAY | Tắt cả 3 job G1r (`enabled: false`), `run_name: none` |

Không có notebook nào thay đổi.
**`configs/kaggle_run.yaml`:** chỉ đổi `enabled: true` → `false` ở 3 job G1r và `run_name: g1r` → `none`, để lỡ bấm Save Version trên runner thì không chạy lại G1r (khoảng 1,5 giờ GPU). Job C1 sẽ thêm khi có SPEC C1.
**Giờ GPU dự kiến:** chỉ Bước 3, khoảng 0,25 giờ [PHỎNG ĐOÁN]. Đã dùng 7,10 giờ (sổ §6).
**Kết quả cần mang về:** Bước 3 (`kiem_gptqmodel.jsonl` + ảnh ô 1, nếu đã chạy); Bước 5 (câu hỏi của bạn).
