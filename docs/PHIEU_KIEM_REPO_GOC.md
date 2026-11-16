# PHIEU_KIEM_REPO_GOC.md — Phiếu kiểm độc lập repo gốc CausalGym

> Bản 13/11/2026 (Claude soạn). Người kiểm: **TV-B**. Hạn: 16/11/2026.
> Repo: `aryamanarora/causalgym`, commit `0f3129ff3b6c5c8264892f30a25be25150ae9179` (`0f3129f`, 30/11/2024). Link trong phiếu đều ghim đúng commit này.
> Mục đích: kiểm lại 12 điểm Claude đọc (sổ §8) **mà không dựa vào lời Claude**. Kết quả là điều kiện để tin kết quả G1.

## 0. Cách làm (theo thứ tự)

1. **Đọc trước, chạy sau.** Mở từng link dưới đây, đọc đúng các dòng ghi trong phiếu, trả lời câu hỏi "Kiểm" bằng lời của mình. Ghi **Khớp** hoặc **Khác**, kèm số dòng và đoạn code (một dòng) làm bằng chứng. Chưa chắc thì ghi **Chưa rõ** và lý do.
2. Chỉ sau khi xong bước 1 mới chạy `notebooks/98_kiem_repo_goc.ipynb` (CPU, vài phút). Notebook cho số liệu thực nghiệm cho điểm 8, 9, 10. Ghi kết quả vào cột "Chạy thử".
3. Mục 3 có 5 điểm **mới** Claude thấy khi đọc lại ngày 13/11 (A–E). Kiểm luôn.
4. Gửi lại phiếu đã điền vào phiên chat. Claude cập nhật sổ (QT-44).

Quy ước: "base" là câu được can thiệp vào; "src" (source) là câu cho giá trị. pyvene nhận vị trí theo dạng `{"sources->base": (vị trí đọc ở source, vị trí ghi ở base)}`. **Đây cũng là một điều cần kiểm** (điểm 9b).

Gốc link: `https://github.com/aryamanarora/causalgym/blob/0f3129ff3b6c5c8264892f30a25be25150ae9179/`
(dưới đây viết tắt là `G/`; ghép vào là ra link đầy đủ, ví dụ `G/eval.py#L72`).

## 1. Hai điểm quan trọng nhất

### Điểm 9 — Vị trí can thiệp bị đảo

- **Sổ ghi:** `compute_pos` trả `[vị trí src, vị trí base]`. Lời gọi pyvene dùng `pos_interv[1]` (vị trí base) làm vị trí đọc source. Đơn vị Collect (dữ liệu cho probe/mean/PCA…) đọc base ở vị trí src. Chỉ có tác dụng khi base và src khác số token.
- **Mở:**
  - `G/data.py#L115-L142` (hàm `compute_pos`; chú ý dòng 138–140)
  - `G/eval.py#L27-L32` và `G/train.py#L58-L63` (lời gọi pyvene)
  - `G/interventions.py#L48-L63` (thứ tự đơn vị: đơn vị 0 là Collect, đơn vị 1 là DAS/vanilla)
  - `G/eval.py#L35-L38` (activation từ đơn vị Collect được gom làm dữ liệu cho các phương pháp khác)
- **Kiểm:**
  - 9a. `ret` ở dòng 140 xếp `rets_src` trước hay `rets_base` trước?
  - 9b. Trong pyvene 0.1.6, phần tử thứ nhất của tuple `"sources->base"` là vị trí ở source hay ở base? Tìm trong code hoặc tutorial của pyvene 0.1.6, ghi nơi tìm thấy.
  - 9c. Từ 9a, 9b: DAS đọc source ở vị trí nào? Ghi vào base ở vị trí nào? Collect đọc base ở vị trí nào?
  - 9d. Khi nào lỗi vô hại?
- **Chạy thử:** ô 4 của notebook 98 đếm tỉ lệ cặp bị lệch vị trí theo từng tác vụ và vùng. Ô 6 (môi trường cũ) xác nhận bằng chạy thật trên model ngẫu nhiên.

### Điểm 10 — Tập eval của bài là split `test` của HF

- **Sổ ghi:** bài dùng `eval_seed = 1`. Dataset HF xuất train seed 42, dev seed 420, test seed 1, nên split `test` của HF chính là tập eval của bài. G0/G0b của nhóm dùng `validation` (dev).
- **Mở:**
  - `G/das.py#L72-L83` (sinh train, loại trùng, sinh eval)
  - `G/test_all.py#L24-L42` (tham số tác giả dùng khi chạy toàn bộ: `steps`, `batch_size`, `eval_steps`)
  - `G/data.py#L380-L417` (hàm xuất dữ liệu lên HF)
  - `G/data.py#L341-L347` (`sample_batches` đặt lại seed mỗi lần gọi)
- **Kiểm:**
  - 10a. Khi không bật `--hparam_non_das`, `eval_seed` bằng bao nhiêu?
  - 10b. Số batch và cỡ batch của train và eval trong `test_all.py` có giống trong hàm xuất HF không (train 100 × 4, eval 25 × 4)?
  - 10c. Hàm xuất HF đặt tên split `test` cho seed nào, `dev` cho seed nào?
  - 10d. Có gì khác giữa hai đường (ví dụ template chọn ngẫu nhiên ở `G/data.py#L175`, tokenizer khác) làm hai tập lệch nhau không? Gợi ý: đếm số template của mỗi tác vụ trong `data/templates/syntaxgym.json`.
- **Chạy thử:** ô 3 của notebook 98 sinh lại hai đường và so với HF (cần Internet).

## 2. Mười điểm còn lại

| # | Sổ ghi | Mở | Kiểm |
|---|---|---|---|
| 1 | Odds = (log p_base(y_base) − log p_base(y_src)) + (log p_int(y_src) − log p_int(y_base)), dùng log-softmax | `G/eval.py#L41-L46`, `G/eval.py#L72`; `G/plot.py#L118` (tính lại khi vẽ) | Các p là log-softmax hay xác suất? Odds là trung bình trên mọi cặp kể cả cặp đảo? Hiệu log-softmax trong cùng một phân phối có bằng hiệu logit không? |
| 2 | Loss học DAS = cross-entropy về nhãn src | `G/eval.py#L10-L15`, `G/train.py#L71-L76` | Nhãn trong loss là `src_labels` hay `base_labels`? Chỉ ở token cuối? |
| 3 | Template thêm `<\|endoftext\|>` ở đầu câu | `G/data.py#L175` | Chuỗi nào được nối vào trước template? |
| 4 | Mỗi batch gồm các cặp và cặp đảo của chúng | `G/data.py#L300-L338` | Batch 4 gồm mấy cặp lấy mẫu và mấy cặp đảo? |
| 5 | Chủ ngữ base/src chọn độc lập; nhãn chọn độc lập trong nhóm của từng loại | `G/data.py#L238-L243`, `G/data.py#L256-L261` | Hai `random.choice` có dùng chung chỉ số không? Ví dụ: base "is" có thể đi với src "have" không? |
| 6 | Loại trùng chỉ kiểm câu base của cặp vừa lấy mẫu, sau đó mới thêm cặp đảo, nên câu src có thể trùng train | `G/das.py#L76-L83`, `G/data.py#L301-L312`, `G/data.py#L333-L335` | Xem thêm mục 3, điểm A |
| 7 | Bảng tổng hợp: max theo vị trí ở mỗi layer → trung bình qua layer → trung bình qua tác vụ; selectivity = odds − odds dog-give, lấy max riêng | `G/plot.py#L307-L331`; dòng trung bình qua tác vụ ở `G/plot.py#L344-L345` | Selectivity là max theo vị trí của (odds − odds dog-give), hay (max odds) − (max odds dog-give)? Xem dòng 322 rồi 328 |
| 8 | Token hoá cả câu, căn vùng bằng token hoá từng vùng | `G/data.py#L42-L65` | Vị trí từng vùng tính từ `tokenizer.tokenize(vùng)` hay từ token hoá cả câu? Chạy thử: ô 5 notebook 98 |
| 11 | dtype: 410m fp32, 1b bfloat16 | `G/utils.py#L27-L42`, `G/test_all.py#L53-L57`, `G/das.py#L62` | Khi chạy `test_all.py` trên GPU, 1b nạp ở dtype nào? |
| 12 | Probe: LogisticRegression saga, L2, có bias, C = 1e-4/1e-5 (410m), 1e-5/1e-6 (1b); dog-give gán " dog" cho `types[0]` | `G/diff_methods.py#L56-L68`, `G/diff_methods.py#L94-L109`, `G/data.py#L178`, `G/data.py#L323-L326` | `types[0]` là khoá đầu của `labels` trong template. Với 4 tác vụ G1, khoá đầu là gì? (mở `data/templates/syntaxgym.json`) |

## 3. Điểm mới (Claude đọc lại 13/11/2026, chưa có trong sổ v0.4)

| # | Nhận xét của Claude | Mở | Kiểm |
|---|---|---|---|
| A | Tập loại trùng `discard` gồm **mọi** câu base trong `trainset[i].pairs`, mà `pairs` đã gồm cả cặp đảo. Vậy `discard` chứa cả câu base và câu src của train. Câu base của cặp eval được kiểm với cả hai; câu src của cặp eval không được kiểm. Điểm 6 vẫn đúng, chỉ chính xác hơn | `G/das.py#L76-L79`, `G/data.py#L333-L338` | Có đúng `batch.pairs` chứa cặp đảo không? |
| B | Điểm DAS trong bảng tổng hợp lấy ở bước eval cuối (bước 99 khi `steps = 100`); vanilla và các phương pháp khác có `step = -1` | `G/plot.py#L146-L149`, `G/train.py#L97-L104` | Có lọc theo bước cuối không? |
| C | Lịch học DAS: Adam, lr 5e-3, warmup tuyến tính 10% số bước rồi giảm tuyến tính về 0; 1 lượt qua 100 batch | `G/train.py#L18-L38`, `G/test_all.py#L24-L42`, `G/test_all.py#L80` | So với notebook 01 của nhóm: có cùng lịch học không? (Tanyel & Ayvaz dùng lr hằng, nêu đây là điểm khác) |
| D | Bảng tổng hợp bỏ dòng có NaN sau khi pivot, nên phương pháp nào thiếu lượt chạy dog-give sẽ mất khỏi bảng, kể cả cột odds | `G/plot.py#L316-L331` | Đúng không? Hệ quả khi nhóm tự tổng hợp |
| E | Mặc định dtype khác nhau giữa hai file: `test_all.py` dùng bfloat16 cho model không có trong `WEIGHTS`, `das.py` dùng float16. Không ảnh hưởng 410m/1b vì cả hai có trong `WEIGHTS` | `G/test_all.py#L56`, `G/das.py#L62` | Chỉ cần xác nhận |

## 4. Bảng điền (TV-B)

| # | Khớp / Khác / Chưa rõ | Bằng chứng (file:dòng, trích một dòng) | Chạy thử (notebook 98) | Ghi chú |
|---|---|---|---|---|
| 1 | | | — | |
| 2 | | | — | |
| 3 | | | — | |
| 4 | | | — | |
| 5 | | | — | |
| 6 | | | — | |
| 7 | | | — | |
| 8 | | | ô 5 | |
| 9 | | | ô 4, ô 6 | |
| 10 | | | ô 3 | |
| 11 | | | — | |
| 12 | | | — | |
| A | | | — | |
| B | | | — | |
| C | | | — | |
| D | | | — | |
| E | | | — | |

## 5. Nếu có điểm "Khác"

- Điểm 9 hoặc 10 khác với sổ: **DỪNG G1**, mang phiếu vào phiên chat. Tiêu chí G1 (sổ §4) dựa trên hai điểm này.
- Điểm khác: ghi vào phiếu, G1 vẫn chạy; Claude đánh giá ảnh hưởng ở phiên sau.
