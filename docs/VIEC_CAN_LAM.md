# VIEC_CAN_LAM.md — Việc cần làm sau phiên chat

> Phiên 16/11/2026. Viết theo QT-41. **Bản này thay luôn `HUONG_DAN_VIEC_14_18_11.md`** (đã gộp hết vào đây; file đó không đưa vào repo và nên xoá khỏi Project).
> **Cách đọc:** làm lần lượt từ Bước 1 xuống. Mỗi bước có 5 mục:
> - **Cần có:** những gì phải sẵn sàng trước khi làm.
> - **Làm:** thao tác hoặc lệnh, chép và dán được.
> - **Xong khi:** dấu hiệu tự kiểm được.
> - **Nếu không:** cách xử lý khi không ra như vậy.
> - **Ra:** đầu ra của bước, và bước nào sẽ dùng nó.
>
> Gặp chữ **DỪNG** thì không làm tiếp; mang những thứ được nêu ở đó vào phiên chat.
> Không có bước nào bắt bạn điền số vào sổ. Claude tự cập nhật sổ, nhật ký GPU và bảng run từ file bạn gửi (QT-44). Claude không ghi gì lên Project; bạn tự tải theo bảng "Cho KB" ở cuối câu trả lời của Claude (QT-45).
> Bước 3 là ngoại lệ có chủ ý: phiếu kiểm do TV-B tự đọc code và tự điền, để độc lập với Claude.

## Đang ở đâu

- **G1 đạt (16/11)** cho cả 410M và 1B: τ_b = 1,00 và DAS đứng đầu; 4/4 tác vụ đúng thứ tự vị trí; 15/16 cặp cùng bậc; accuracy trùng bài. Run `20261113_0846_g1`, 5,06 giờ GPU. Chi tiết: sổ v0.7, §4 và §10.
- Hai tác vụ không bị lỗi vị trí của repo gốc khớp bài tới 2 chữ số; lệch chỉ có ở 2 tác vụ bị lỗi chạm. Bước 2 (G1r) kiểm xem lỗi đó có giải thích phần lệch không (quy tắc D-16 đã chốt trước).
- Tiếp theo: các việc của tuần 16–18/11 (kiểm repo gốc, G-N, PDF, GPT-QModel), rồi Claude viết SPEC C1/C2 và notebook 02.
- Hạn: G-N 17/11; các việc khác 18/11; G1 đã đóng (hạn cũ 31/12).

## Tóm tắt thứ tự

| Bước | Ai | Việc | Hạn | Thời gian |
|---|---|---|---|---|
| 1 | TV-A | Giải nén zip phiên này vào repo, commit, push | 16/11 | 10 phút |
| 2 | TV-A | Chạy G1r trên Kaggle bằng Save Version | 16/11 | khoảng 1,5 giờ chờ, không cần canh |
| 3 | TV-B | Đọc code repo gốc, điền phiếu kiểm 17 điểm | 16/11 | 1,5–2 giờ |
| 4 | TV-B | Chạy notebook 98 (CPU) | 16/11 | 10 phút |
| 5 | Một người | G-N: chạy notebook 96 (CPU, có Internet) | 17/11 | 15 phút |
| 6 | TV-A | Tải 2 PDF lên Project; dán lời duyệt/nhận xét của thầy vào chat | 18/11 | 10 phút |
| 7 | TV-A | Chạy notebook 97 trên Kaggle T4 (từng ô) | 18/11 | 15 phút, khoảng 0,25 giờ GPU [PHỎNG ĐOÁN] |
| 8 | Cả hai | **DỪNG**: mang kết quả vào phiên chat | 18/11 | — |

Bước 2 chạy nền trên Kaggle, nên Bước 3–6 làm song song được trong lúc chờ. Mang từng phần vào chat ngay khi có cũng được (ví dụ zip notebook 96 ngày 17/11 để đóng G-N đúng hạn).

---

## Bước 1. Giải nén zip vào repo

**Cần có:** file `khoaluan_16_11.zip` từ phiên chat này. **Không** cần zip phiên 13/11 lần 3 nữa: nội dung của nó đã nằm trong zip này.

**Làm:** giải nén `khoaluan_16_11.zip` vào **thư mục gốc** của repo, cho phép ghi đè. Zip có sẵn đúng cấu trúc (bảng file ở cuối). Rồi:
```bash
cd <thư mục repo>
git status
git add results notebooks configs docs
git commit -m "[G1] ket qua G1 + nb01b; config G1r; file phien 13/11 lan 3 (nb96-98, phieu kiem); so v0.7"
git push
```

**Xong khi:** trên GitHub, commit mới nhất là `[G1] ket qua G1 ...`, và thấy:
- `results/20261113_0846_g1/run_summary.json`;
- `notebooks/01b_phan_tich_g1.ipynb`, `96_gn_tra_cuu_api.ipynb`, `97_kiem_gptqmodel.ipynb`, `98_kiem_repo_goc.ipynb`;
- dòng 3 của `docs/KHOALUAN_KE_HOACH_THEO_DOI.md` ghi `Version: v0.7`;
- `configs/kaggle_run.yaml` có `run_name: g1r`.

**Nếu không:**
- `git status` có thư mục lạ như `khoaluan_16_11/`: Windows đã giải nén lồng một cấp. Chuyển nội dung ra gốc repo rồi xoá thư mục rỗng.
- Lỡ giải nén thêm zip phiên 13/11 lần 3 sau zip này: sổ bị lùi về v0.6. Giải nén lại zip này là đủ.
- Repo có sẵn `docs/HUONG_DAN_VIEC_14_18_11.md` (nếu trước đây đã chép tay): `git rm docs/HUONG_DAN_VIEC_14_18_11.md` rồi commit, để khỏi có hai file việc.
- File `src/` hay `g0_pilot.py` cũ: không liên quan, để nguyên.

**Ra:** commit mới trên GitHub. Bước 2, 4, 5, 7 dùng commit này.

---

## Bước 2. Chạy G1r trên Kaggle (nên làm)

G1r chạy lại G1 ở chế độ `POS_MODE = "repo"` (tái hiện lỗi vị trí của repo gốc) cho 2 tác vụ bị lỗi chạm (`agr_sv_num_subj-relc`, `cleft`), cả 410M và 1B. Kết quả cho biết phần lệch so với bài có đúng là do lỗi đó không. Bỏ bước này thì G1 vẫn đạt và C1 vẫn làm được, nhưng chương tái lập chỉ ghi được "lệch có thể do lỗi vị trí" [GỢI Ý].

**Cần có:** Bước 1 đã push.

**Làm:**
1. Kaggle (tài khoản TV-A) → mở notebook `runner` (không sửa ô nào).
2. Kiểm Settings: Accelerator **GPU T4**, Internet **On**.
3. **Save Version → Save & Run All (Commit)** → Save.
4. Có thể tắt máy. Runner chạy 3 job:
   - `g1r_smoke_410m`: khoảng 2 phút;
   - `g1r_410m`: khoảng 40 phút;
   - `g1r_1b`: khoảng 45 phút.

   Smoke lỗi thì các job sau tự bỏ (`stop_on_error: true`).
5. (Tuỳ chọn) Khoảng 10 phút sau khi bấm Save, mở log của version: thấy `g1r_smoke_410m` báo `ok` là yên tâm.

**Xong khi:** trang Versions báo version mới **Complete**; tab Output có `<run_id>.zip` với `run_id` dạng `2026MMDD_HHMM_g1r`.

**Nếu không:**
- Version **Failed**, hoặc smoke lỗi: xem bảng "Gỡ lỗi nhanh" cuối file. Không tự sửa notebook; mang zip (có `executed.ipynb`) vào chat.
- Version bị dừng giữa chừng: vẫn tải zip; Claude xem job nào đã xong.

**Ra:** `<run_id>.zip` → Bước 8. Claude chạy notebook 01b với thư mục G1r và áp quy tắc D-16 (sổ §3).

---

## Bước 3. TV-B đọc code repo gốc, điền phiếu (đọc trước, chạy sau)

**Cần có:** `docs/PHIEU_KIEM_REPO_GOC.md` (từ Bước 1). Nên điền **trước khi** đọc §10 của sổ hay kết quả G1, để không bị dẫn dắt.

**Làm:** mở từng link (đã ghim commit `0f3129f`); trả lời câu "Kiểm" bằng lời của mình; điền bảng §4 của phiếu (17 dòng: 12 điểm cũ + A–E). Với điểm 9b, xem `pyvene/models/intervenable_base.py` của **pyvene 0.1.6** (bản cài từ PyPI): dòng 1669–1670 đọc `unit_locations["sources->base"][0]` cho source và `[1]` cho base. Tự mở để xác nhận, đừng chép lời Claude.

**Xong khi:** 17 dòng đều có Khớp / Khác / Chưa rõ kèm bằng chứng (file:dòng, trích một dòng).

**Nếu không:** điểm 9 hoặc 10 ra "Khác": **DỪNG**, mang phiếu vào chat ngay (§5 của phiếu ghi "DỪNG G1"; G1 đã chạy xong, nên hiểu là kết luận G1 phải xem lại). Điểm khác ra "Khác": cứ ghi vào phiếu, làm tiếp.

**Ra:** phiếu đã điền → Bước 4 và Bước 8.

---

## Bước 4. TV-B chạy notebook 98 (CPU)

**Cần có:** phiếu đã điền (Bước 3); commit từ Bước 1.

**Làm (Kaggle, từng ô — QT-11 trường hợp d: việc dưới 5 phút):** tạo notebook mới, File → Import `notebooks/98_kiem_repo_goc.ipynb`; Accelerator **None**; bật **Internet**. Ô parameters giữ mặc định (`COMPARE_HF = True`, `RUN_PYVENE_TEST = False`). Run All. **Xong thì Stop session.**
- Muốn chạy luôn ô 6 (pyvene): làm trong một session khác; ô đầu tiên chạy `!pip install -q "transformers==4.46.2" "pyvene==0.1.6"`, restart kernel, đặt `RUN_PYVENE_TEST = True`. Ô này dựng model ngẫu nhiên nên không tải trọng số.

**Xong khi:** `outputs/98_kiem_repo_goc/kiem_repo_goc.jsonl` có 4 dòng `diem10_so_hf` với `ket_luan`.

**Nếu không:** `load_dataset` lỗi thì đặt `COMPARE_HF = False`, ghi lại lỗi; các ô khác vẫn chạy được.

**Ra:** `kiem_repo_goc.jsonl` (tải ở tab Output) → Bước 8. Số của TV-B phải trùng số Claude đã có (sổ §8 điểm 9, 10).

---

## Bước 5. G-N: chạy notebook 96 (một người)

**Cần có:** commit từ Bước 1.

**Làm:** Kaggle → New Notebook → File → Import `notebooks/96_gn_tra_cuu_api.ipynb`; Accelerator **None**; bật **Internet**; Run All (QT-11 trường hợp d, dưới 10 phút). Giữ tham số mặc định. **Xong thì Stop session.** Chạy trên máy cá nhân cũng được (`pip install requests`).

**Xong khi:** ô 8 in "file mang về: …/96_gn_tra_cuu.zip".

**Nếu không:** ô 8 báo trên 20 lỗi thì chờ khoảng 10 phút, chạy lại cả notebook. Ít lỗi hơn thì cứ mang zip về.

**Ra:** `96_gn_tra_cuu.zip` → Bước 8 (mang vào chat ngày 17/11 để kịp hạn G-N). Claude đọc mọi bài, xếp loại theo `GN_TRA_CUU.md` §1, điền bảng và sổ; bạn không phải đọc hay điền gì.

---

## Bước 6. TV-A tải tài liệu lên Project, gửi lời thầy

**Cần có:** Internet.

**Làm:**
1. Tải và thêm vào Claude Project:
   - Tanyel & Ayvaz: `https://arxiv.org/pdf/2611.05033`
   - Makarov: `https://arxiv.org/pdf/2610.40055`

   (Zhou et al. đúng bài `2026.findings-acl.1162.pdf` đã có trong Project từ 14/11.)
2. Lời duyệt và nhận xét lần 3 của thầy: dán nguyên văn (hoặc ảnh chụp) vào phiên chat. Claude viết `NHAN_XET_GVHD.md` để bạn tải lên.

**Xong khi:** 2 PDF hiện trong mục Files của Project; lời thầy đã nằm trong chat.

**Nếu không:** arXiv không tải được thì gửi link trang tóm tắt cho Claude và ghi lại lỗi.

**Ra:** Bước 8: Claude đọc toàn văn (§7.1 và Phụ lục E.1 của Tanyel; cách đặt biên tương đương của Makarov) để viết SPEC C1. TV-A chỉ cần kiểm lại 3–5 số Claude trích.

---

## Bước 7. TV-A chạy notebook 97 trên Kaggle (GPT-QModel)

**Cần có:** commit từ Bước 1.

**Làm (từng ô — QT-11 trường hợp b: cài thư viện có thể phải thử nhiều lần):** import `notebooks/97_kiem_gptqmodel.ipynb`, bật **GPU T4** và Internet. Giữ tham số mặc định. Chạy **từng ô**, dừng sau ô 1 để đọc dòng phiên bản:
- nếu in "CẢNH BÁO: cài GPT-QModel đã đổi torch" thì dừng, chụp ô 1, sang Bước 8;
- nếu không thì chạy tiếp tới ô 8.

**Xong thì Stop session.**

**Xong khi:** `outputs/97_kiem_gptqmodel/kiem_gptqmodel.jsonl` có dòng `ppl` với 4 giá trị fp, rtn, gptq, gptq_alpha_0.5.

**Nếu không:**
- Kaggle không cho mở phiên GPU vì version G1r (Bước 2) đang chạy: đợi version xong, hoặc chạy bằng tài khoản TV-B.
- Lỗi ở `qm.save()` nhắc `lm_head.weight`: kiểm `offload_to_disk=False` có trong ô 5 chưa.
- Lỗi khác: chụp traceback.

**Ra:** `kiem_gptqmodel.jsonl` (+ ảnh ô 1) → Bước 8; dùng để chốt D-15 (đường GPTQ cho C1).

---

## Bước 8. DỪNG: mang kết quả vào phiên chat

**Mang (có phần nào mang phần đó, không cần đợi đủ):**

| Từ bước | Thứ cần mang |
|---|---|
| 2 | `<run_id>.zip` của G1r |
| 3 | `PHIEU_KIEM_REPO_GOC.md` đã điền |
| 4 | `kiem_repo_goc.jsonl` |
| 5 | `96_gn_tra_cuu.zip` |
| 6 | Lời duyệt và nhận xét của thầy (dán vào chat) |
| 7 | `kiem_gptqmodel.jsonl` + ảnh ô 1 |
| — | `docs/VIEC_CAN_LAM.md` (file này) |

Nhắn một câu, ví dụ: "G1r xong, tài khoản TV-A; phiếu đây". Nếu chạy bằng tài khoản khác ghi trong file này, nói rõ (để ghi nhật ký GPU).

**Claude sẽ làm, theo thứ tự:**
1. G-N: đọc kết quả notebook 96, xếp loại, kết luận cổng G-N.
2. G1r: chạy notebook 01b với thư mục G1r, áp D-16, ghi vào sổ §10 và §8 điểm 9.
3. Phiếu TV-B và notebook 98: điền cột TV-B ở sổ §8; nếu có "Khác" ở điểm 9/10 thì xem lại G1.
4. Notebook 97: chốt D-15.
5. Viết **SPEC C1/C2** (chốt D-11, D-12, D-15, biên tương đương, ngưỡng R, cách dùng `cleft`, ngân sách GPU), rồi notebook 02 và `kaggle_run.yaml` cho smoke C1.

---

## Việc không cần GPU, không chặn bước nào

| Ai | Hạn | Việc | Đầu ra dùng vào đâu |
|---|---|---|---|
| TV-A | 23–30/11 | Đề cương theo mẫu FIT; gửi thầy kèm câu hỏi ở sổ §7 (câu 6 đã cập nhật theo G1) | Đề cương |
| TV-A | khi rảnh, 1 phút | (Tuỳ chọn) Ô "Instructions" của Project còn ghi "sổ dự án v0.2" và "Nhắc cập nhật sổ dự án". Sửa thành "sổ dự án v0.7" và "Tự cập nhật sổ dự án (QT-44)" | Khớp quy trình |

## File trong zip phiên này

| Đường dẫn | THAY/THÊM | Nội dung |
|---|---|---|
| `results/20261113_0846_g1/` | THÊM | Kết quả G1, đúng như zip Kaggle |
| `results/20261116_claude_cpu_nb01b/` | THÊM | Bản chạy CPU của Claude cho notebook 01b (in mọi số G1 trong sổ) |
| `notebooks/01b_phan_tich_g1.ipynb` | THÊM | Phân tích lại G1 trên CPU: kiểm dữ liệu, 3 tiêu chí tính độc lập, tách lệch theo lỗi vị trí, áp D-16 khi có G1r. Đã chạy cả `TOY_TEST` và dữ liệu thật |
| `configs/kaggle_run.yaml` | THAY | 3 job G1r: `g1r_smoke_410m`, `g1r_410m`, `g1r_1b` (`POS_MODE: "repo"`, 2 tác vụ) |
| `docs/KHOALUAN_KE_HOACH_THEO_DOI.md` | THAY | Sổ v0.7 |
| `docs/VIEC_CAN_LAM.md` | THAY | File này |
| `docs/QUY_TRINH_LAM_VIEC.md` | THAY | Bản 13/11 lần 2 (có QT-45), chép từ Project để repo khớp; nội dung không đổi |
| `docs/PHIEU_KIEM_REPO_GOC.md`, `docs/GN_TRA_CUU.md`, `docs/GHI_CHU_BAI_BAO.md` | THÊM | Từ phiên 13/11 lần 3, không đổi |
| `notebooks/96_gn_tra_cuu_api.ipynb`, `97_kiem_gptqmodel.ipynb`, `98_kiem_repo_goc.ipynb` | THÊM | Từ phiên 13/11 lần 3, không đổi |
| `results/20261113_claude_cpu_nb98/`, `results/20261113_claude_cpu_nb97_toy/` | THÊM | Từ phiên 13/11 lần 3; `nb98/GHI_CHU.md` sửa 1 dòng trỏ sang file này |

Không có trong zip: `docs/HUONG_DAN_VIEC_14_18_11.md` (đã gộp vào file này).

**`configs/kaggle_run.yaml`:** đổi từ G1 (4 tác vụ, `POS_MODE` mặc định `correct`) sang G1r (2 tác vụ, `POS_MODE: "repo"`, `SAVE_DIRS: false`, `MAX_HOURS` 0,5 / 1,5 / 2,0). Cấu hình G1 cũ nằm ở commit `d755410`.
**Giờ GPU dự kiến:** G1r khoảng 1,5 giờ (suy từ phút từng tác vụ của G1); notebook 97 khoảng 0,25 giờ [PHỎNG ĐOÁN]. Đã dùng 5,66 giờ.
**Kết quả cần mang về:** xem bảng ở Bước 8.

## Gỡ lỗi nhanh khi chạy runner

| Triệu chứng | Nguyên nhân hay gặp | Cách xử lý |
|---|---|---|
| `Clone lỗi` với 401/403/404 | Token sai quyền; sai `GITHUB_USER`/`REPO_NAME`; Secret chưa bật cho notebook | Kiểm lại ba thứ đó; token cần quyền Contents: Read-only cho đúng repo |
| Log có "Không tải được split 'test' ... Dùng 'validation'" | Thư viện `datasets` không thấy split test | Job vẫn chạy trên validation; báo Claude ở Bước 8 (kết quả G1r khi đó không so được với G1) |
| Log có "Thứ tự loại của ... không khớp" | Tên loại trong dữ liệu khác template gốc | Không chặn job; báo Claude ở Bước 8 |
| Lỗi khi `load_dataset` | Phiên bản `datasets` cũ | Thêm `"datasets>=3"` vào mục `pip:` trong `kaggle_run.yaml`, commit, chạy lại |
| `CUDA out of memory` | Batch lớn ở 1B | Thêm `EVAL_BS: 16` và `CAP_BS: 16` vào `params` của job, commit, chạy lại |
| `No such kernel named python3` | Kaggle đổi tên kernel | Thêm ô `!jupyter kernelspec list` vào runner, sửa `kernel_name` |
| Không có GPU trong log | Version chạy không có Accelerator | Settings → Accelerator → GPU T4, chạy lại |
