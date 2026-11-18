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
| 1 | Khớp | `eval.py:42` `base_probs = F.log_softmax(base_logits[:, -1], dim=-1)` và `eval.py:72` `(base_probs[y_base] - base_probs[y_src]) + (interv_probs[y_src] - interv_probs[y_base])` | — | Các `p` là `log_softmax`; `odds` là trung bình trên mọi cặp (kể cả cặp đảo); hiệu hai `log_softmax` trong cùng phân phối bằng hiệu hai logit. |
| 2 | Khớp | `train.py:75` `loss = calculate_loss(interv_outputs.logits, batch.src_labels)` và `eval.py:12` `F.cross_entropy(logits[:, -1], labels)` | — | Nhãn trong loss là `src_labels`; chỉ tính ở token cuối `logits[:, -1]`. |
| 3 | Khớp | `data.py:175` `self.sentence = ["<\|endoftext\|>" + self.sentence[0]] + self.sentence[1:]` | — | Nối chuỗi `"<\|endoftext\|>"` vào trước phần tử đầu tiên của template. |
| 4 | Khớp | `data.py:301` `for _ in range(batch_size // 2):` và `data.py:335` `pairs += [x.swap() for x in pairs]` | — | Batch cỡ 4 gồm 2 cặp lấy mẫu gốc và 2 cặp đảo (`swap`) của chúng. |
| 5 | Khớp | `data.py:240` `random.choice(...)` và `data.py:257` `base_label = random.choice(self.labels[base_type])` | — | Hai lệnh `random.choice` không dùng chung chỉ số; nhãn `base` `" is"` có thể đi với `src` `" have"`. |
| 6 | Khớp | `data.py:305` `if ''.join(pair.base) in discard: continue` và `data.py:335` `pairs += [x.swap() for x in pairs]` | — | Chỉ kiểm `pair.base` trước khi thêm cặp đảo `swap()`, nên `pair.src` (thành `base` của cặp đảo) có thể trùng với tập train. |
| 7 | Khớp | `plot.py:322` `df['selectivity'] = df['odds'] - df['odds_control']` và `plot.py:328` `df.groupby(['model', 'dataset', 'method', 'layer']).max()` | — | Selectivity là `max` theo vị trí của `(odds − odds dog-give)` ở mỗi layer (tính hiệu ở dòng 322 rồi mới `.max()` ở dòng 328). |
| 8 | Khớp | `data.py:49` `tokens = tokenizer.tokenize(''.join(sentence))` và `data.py:63` `region_tokens = [tokenizer.tokenize(x) for x in sentence]` | **ô 5 (`diem8_tok_mismatch`):** Tokenizer `EleutherAI/pythia-70m` (`vocab=50277`): cả 4 tác vụ (`agr_sv_num_subj-relc`, `npi_any_subj-relc`, `filler_gap_subj`, `cleft`) đều có `n_cau = 200`, `n_lech = 0` (0/800 câu lệch). | Token hoá cả câu nhưng vị trí từng vùng tính từ `tokenizer.tokenize(vùng)`. |
| 9 | Khớp | `data.py:140` `ret = [rets_src, rets_base]` và `eval.py:30` `unit_locations={"sources->base": ([None, pos_interv[1]], [pos_interv[0], pos_interv[1]])}` | **ô 4 (`diem9_ty_le_lech`, `n_cap=100`):** `agr_sv_num_subj-relc`: `0.16` (mọi vùng 1..5 đều `0.16`); `cleft`: `0.08` (`2:{verb}`: `0.08`, `3:_was`: `0.08`); `npi_any_subj-relc`: `0.0` (vùng 1..8 đều `0.0`); `filler_gap_subj`: `0.0` (vùng 2..8 đều `0.0`). **ô 6 (`diem9_pyvene`):** `p_base = 3` (`['Ġcat']`), `p_src = 6` (`['Ġhipp', 'opot', 'am', 'uses']`); `repo_lech_voi_gt_p_base = 0.0`, `repo_lech_voi_gt_p_src = 0.8061596155166626`; `sua_lech_voi_gt_p_base = 0.8061596155166626`, `sua_lech_voi_gt_p_src = 0.0` (repo đọc source ở vị trí base; bản sửa đọc đúng vị trí src). | Trong `pyvene 0.1.6` (`intervenable_base.py:1669-1670`), tuple `"sources->base"` là `(vị trí ở source, vị trí ở base)`. DAS/vanilla (đơn vị 1) đọc `source` ở `pos_interv[1]` (vị trí `base`), ghi vào `base` ở `pos_interv[1]`; Collect (đơn vị 0) đọc `base` ở `pos_interv[0]` (vị trí `src`). Lỗi vô hại khi `base` và `src` cùng số token. |
| 10 | Khớp | `das.py:79` `eval_seed = 420 if hparam_non_das else 1` và `data.py:390-398` (train `seed=42`, dev `seed=420`, test `seed=1`) | **ô 3 (`diem10_so_hf`, `n_hf=100`):** Cả 4 tác vụ đều có `test_vs_seed1_n_trung = 100/100`, `validation_vs_seed420_n_trung = 100/100`, `validation_vs_seed1_n_trung = 0/100` (riêng `cleft` là `2/100`). Kết luận: `test` HF = tập eval `seed 1` của bài. | Khi không bật `--hparam_non_das`, `eval_seed = 1`; số batch và cỡ batch (`100 × 4` train, `25 × 4` eval) giống hàm xuất HF; mỗi tác vụ trong `syntaxgym.json` chỉ có 1 template nên không lệch nhau. |
| 11 | Khớp | `utils.py:31-32` `"EleutherAI/pythia-410m": torch.float32, "EleutherAI/pythia-1b": torch.bfloat16` | — | Khi chạy `test_all.py` trên GPU, `410m` nạp ở `float32`, `1b` nạp ở `bfloat16`. |
| 12 | Khớp | `diff_methods.py:59` `LogisticRegression(penalty="l2", solver="saga", C=c, max_iter=1000)` và `data.py:324` `if base_type == self.types[0]: base_label = " dog"` | — | `types[0]` (khoá đầu của `labels` trong `syntaxgym.json`): `agr_sv_num_subj-relc` là `"singular"`, `npi_any_subj-relc` là `"neg"`, `filler_gap_subj` là `"gap"` (khoá đầu), `cleft` là `"normal"`. |
| A | Khớp | `das.py:78-79` `for batch in trainset: for pair in batch.pairs: discard.add(''.join(pair.base))` | — | `batch.pairs` đã chứa cặp đảo nên `discard` gồm cả câu `base` và `src` của `trainset`; câu `base` của cặp eval gốc được kiểm với cả hai, câu `src` không được kiểm. |
| B | Khớp | `train.py:98` `"step": step` (DAS) / `"step": -1` (phương pháp khác) và `plot.py:146-149` | — | Bảng tổng hợp lọc theo bước eval cuối (`step == 99` khi `steps = 100`) cho DAS và `step == -1` cho vanilla cùng các phương pháp khác. |
| C | Khớp | `train.py:25-32` `Adam(..., lr=lr)` + `get_linear_schedule_with_warmup(..., int(0.1 * total_steps), total_steps)` và `test_all.py:80` `lr=5e-3` | — | Cùng lịch học với `notebook 01` của nhóm (Adam, `lr = 5e-3`, warmup tuyến tính 10% số bước rồi giảm tuyến tính về 0 qua 100 batch). |
| D | Khớp | `plot.py:316-331` (pivot/merge với control `dog-give` rồi gọi `.dropna()`) | — | Đúng; phương pháp nào thiếu lượt chạy `dog-give` sẽ bị `.dropna()` loại khỏi bảng tổng hợp, mất cả cột `odds`. |
| E | Khớp | `test_all.py:56` `WEIGHTS.get(model, torch.bfloat16)` và `das.py:62` `WEIGHTS.get(model, torch.float16)` | — | Mặc định fallback khác nhau giữa hai file nhưng không ảnh hưởng `410m` và `1b` vì cả hai đều có trong `WEIGHTS`. |

## 5. Nếu có điểm "Khác"

- Điểm 9 hoặc 10 khác với sổ: **DỪNG G1**, mang phiếu vào phiên chat. Tiêu chí G1 (sổ §4) dựa trên hai điểm này.
- Điểm khác: ghi vào phiếu, G1 vẫn chạy; Claude đánh giá ảnh hưởng ở phiên sau.
