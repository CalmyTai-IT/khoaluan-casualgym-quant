# KHOALUAN_KE_HOACH_THEO_DOI.md — Sổ dự án khoá luận

> Version: v0.3 · Ngày: 12/11/2026 · Nguồn sự thật của project. Đề xuất chi tiết: `DEXUAT_HUONG_B1_DAS.md` v0.5. Quy trình: `QUY_TRINH_LAM_VIEC.md`. Việc trước mắt: `VIEC_CAN_LAM.md`.
> Quy ước: [ĐCM] đã kiểm chứng · [GỢI Ý] bằng chứng chưa đủ · [PHỎNG ĐOÁN] chưa kiểm.

## 1. Thông tin chung

| Mục | Nội dung |
|---|---|
| Nhóm | TV-A Nguyễn Tấn Tài (DAS, C1, C3b); TV-B (lượng tử hoá, C2, thống kê). Hai người chéo kiểm code |
| GVHD | ThS. Tuân Nguyễn Hoài Đức |
| Bài gốc | Arora, Jurafsky, Potts (2024). CausalGym. ACL 2024 (SAC Award) |
| Câu hỏi | Cơ chế DAS 1D trên Pythia FP có còn khi lượng tử hoá trọng số không; hỏng ở đâu, theo thứ tự nào |
| MVP | RQ0 tái lập · C1 hồ sơ bảo toàn · C2 phân rã cấp biến · C3b QiD mức cơ chế qua checkpoint |
| Target | C3 LIFO · C4 so sánh RTN/GPTQ/AWQ/TaCQ |
| Đã bỏ | C5 bảo vệ có định hướng nhân quả (D-02) |
| Tài nguyên | Kaggle T4, khoảng 30 giờ/tuần mỗi tài khoản, phiên tối đa 12 giờ; Pythia 410M và 1B |

## 2. Trạng thái hiện tại (12/11/2026, tối)

- Đã có:
  - đề xuất v0.5;
  - khung repo và Kaggle runner chạy được;
  - **G0 full đã chạy** trên Pythia thật: run `20261112_1441_g0_full`, commit `1232ff0`. Kết quả ở §9.
- G0 **chưa đóng**: chưa có mức nén nào kéo hành vi về gần ngẫu nhiên, và ô chính phải chọn lại (D-08). Đã chuẩn bị G0b: notebook 00 bản 2 và `configs/kaggle_run.yaml` mới.
- Đang làm: G0b, G-N.
- Chưa gửi thầy.

## 3. Nhật ký quyết định

| Mã | Ngày | Quyết định | Lý do |
|---|---|---|---|
| D-01 | 12/11/2026 | Đổi đề tài sang hướng B1; bài gốc CausalGym; hướng phát triển là lượng tử hoá | GVHD: kết quả âm của đề tài cũ khó bảo vệ; cần bài gốc + hướng phát triển; không làm lại nghiên cứu tiếng Anh trên tiếng Việt |
| D-02 | 12/11/2026 | Bỏ C5 | CircuitKIT (arXiv 2607.19317, §11.6) đã thử lượng tử hoá hỗn hợp theo độ quan trọng mạch; Zhou et al. và ICLR 2026 cũng có bảo vệ layer |
| D-03 | 12/11/2026 | Đưa C3b (QiD mức cơ chế qua checkpoint 10K–143K) vào MVP; C3 LIFO chuyển sang Target | C3b nối thẳng Ouyang et al. và Armstrong 2026, có tiên nghiệm rõ; C3 bị nhiễu độ lớn hiệu ứng và thiếu lực kiểm định |
| D-04 | 12/11/2026 | Mốc FP = fp32; mọi lượng tử hoá là giả lập | T4 không có bf16 gốc; tránh nhiễu kernel; pipeline FP và Q giống hệt |
| D-05 | 12/11/2026 | C1 dùng ba nhãn Tương đương / Khác / Chưa kết luận; null hai phía; sàn step0 cho DAS học lại | δ = 2 điểm accuracy nhỏ hơn nhiễu (khoảng 100 câu test/tác vụ); DAS cho hiệu ứng cả ở model khởi tạo |
| D-06 | 12/11/2026 | Thêm nút vặn liên tục W(α) = W + α(Q(W) − W) | Lưới 8/6/4/3/2 bit có thể chỉ cho "Bảo toàn" hoặc "Sụp" |
| D-07 | 12/11/2026 | Quy trình: code trên GitHub; Kaggle runner + papermill; mặc định Save Version; thí nghiệm dạng notebook; file `VIEC_CAN_LAM.md` sau mỗi phiên | Tắt được Kaggle khi chạy; dễ comment và bắt lỗi từng ô; giữ được bối cảnh qua phiên. Chi tiết trong `QUY_TRINH_LAM_VIEC.md` |
| D-08 | 12/11/2026 | **Sau dữ liệu (G0 full).** Đổi quy tắc chọn ô chính. Cũ: ô có odds FP lớn nhất, trừ layer cuối. Mới (`MAIN_RULE = last_early`): chỉ xét vùng cuối (vị trí dự đoán), layer 1 đến L−2; chọn layer sớm nhất có odds FP ≥ 0,8 × odds lớn nhất của vùng cuối trên các layer đó. **Trạng thái: chờ cả nhóm xác nhận trước khi chạy G0b** (`VIEC_CAN_LAM.md`, Bước 2) | Quy tắc cũ chọn L0/vùng 1: residual ngay sau khối đầu, tại chính token chủ ngữ, nên can thiệp gần như thay token. C2 tách đoạn ở đó suy biến (phía mã hoá chỉ 1/24 layer). Ô ở vùng cuối đòi thông tin được chuyển qua attention, vượt tân ngữ |
| D-09 | 12/11/2026 | **Sau dữ liệu (G0 full).** Sửa cách đo (notebook 00 bản 2): (i) bootstrap theo cụm, mỗi cụm là cặp gốc + cặp đảo; (ii) hành vi tính trên câu không trùng; (iii) học lại trên Q với k seed, so \|cos\| theo cặp seed khác nhau; (iv) Spearman bản đồ tính trên ô có odds FP ≥ 1, thêm T theo từng ô; (v) lưới nén cho G0b dời xuống 3 và 2 bit kèm α. Riêng (v) là áp quy tắc G0 số 2, không đổi ngưỡng | (i) Repo gốc thêm cặp đảo vào mỗi batch, nên 100 cặp eval chỉ là 50 cặp độc lập. (iii) Cùng seed cho \|cos\| 0,999 ở 8 bit, trong khi giữa các seed FP chỉ 0,89, nên so trực tiếp sẽ sai. (iv) Spearman = 1,0 ở mọi mức, kể cả 3 bit (T = 0,75). (v) 8/6/4 bit và mọi α ở 4 bit đều giữ accuracy 0,97 |
| D-10 | 12/11/2026 | `VIEC_CAN_LAM.md` viết theo bước thời gian, mỗi bước có Cần có / Làm / Xong khi / Nếu không / Ra (QT-41 mới) | Bản trước gom theo mục, khó theo; bước lưu kết quả G0 vào repo bị bỏ sót |

## 4. Cổng quyết định

| Cổng | Hạn | Điều kiện đạt | Trạng thái | Nếu không đạt |
|---|---|---|---|---|
| G-N tính mới | 17/11/2026 | "Cited by" của CausalGym, Ouyang, Duan, Makarov; tìm thêm; không ai đã làm C1/C2/C3b | Đang làm | Bỏ hoặc đổi đóng góp bị trùng |
| G0 chạy được | 22/11/2026 | Chạy hết `notebooks/00_g0_pilot.ipynb` trên 410M; có t; có vùng chuyển tiếp; có sàn step0; đo t cho 1B | **Một phần (12/11).** Đạt: chạy hết, có t, có sàn step0 (ở ô cũ), có t cho 1B. Chưa đạt: vùng chuyển tiếp mới thấy giữa 4 và 3 bit, chưa có mức gần ngẫu nhiên. Ô chính phải chọn lại (D-08). Chờ G0b | Thu phạm vi theo t đo được |
| G1 tái lập | 31/12/2026 (có thể dời 15/01/2027) | Đúng thứ tự phương pháp và thứ tự xuất hiện vị trí; odds cùng bậc | Chưa | Dừng phát triển; sửa pipeline; hỏi tác giả |
| G2 MVP C1 + C2 | 28/02/2027 | Hồ sơ đầy đủ cho 2 model × 4 tác vụ | Chưa | Giảm tác vụ; chỉ 410M |
| G3 MVP C3b | 31/03/2027 | Đường QiD mức cơ chế qua ≥ 5 checkpoint cho ≥ 1 tác vụ | Chưa | Viết luận văn với C1 + C2 |

**Quy tắc quyết định ở G0 (đặt trước khi chạy):**

1. **Thời gian.** Nếu t (học + đánh giá một ô) ≤ 60 giây cho 410M, giữ kế hoạch. Nếu > 60 giây, chỉ học lại ở ô chính và giảm số vị trí.
2. **Lưới nén.** Chọn 3–4 mức (bit hoặc α) sao cho accuracy giảm dần từ ≥ 95% của FP xuống gần mức ngẫu nhiên. Nếu 8 bit đã sụp, có lỗi code.
3. **Sàn step0.** Nếu odds step0 ≥ 50% odds FP ở ô chính, thì DAS học lại (b') không đủ thông tin. Khi đó C1 dựa chủ yếu vào (b) dùng lại hướng, và C3 cần ngưỡng khác.
4. **Seed.** Nếu |cos| giữa các seed < 0.9 ở ô chính, thì trục hình học (c) không dùng được; báo cáo như một kết quả về độ bất ổn của DAS.

**Kết quả áp quy tắc ở G0 full** (12/11/2026, ô chính cũ L0/vùng 1, 410M):

| Quy tắc | Số đo | Kết luận |
|---|---|---|
| 1 | t = 7,55 s | Giữ kế hoạch |
| 2 | 8 bit không sụp (0,97); thấp nhất 3 bit = 0,79; không mức nào gần 0,5 | Chưa chọn được lưới → G0b |
| 3 | Sàn = 3,4% odds FP | (b') có thông tin **ở ô cũ**; phải đo lại ở ô mới |
| 4 | \|cos\| min 0,891, TB 0,895 (k = 3) | Trục (c) không dùng được **ở ô cũ**. Không đổi ngưỡng 0,9; đo lại ở ô mới với k = 5 |

## 5. Việc cần làm

- [x] (TV-A, 12/11) Thiết lập repo và Kaggle runner; G0 full 410M + đo thời gian 1B
- [ ] (TV-A, 13/11) Lưu kết quả G0 full vào `results/` (bước còn sót)
- [ ] (Cả hai, 13/11) Xác nhận D-08 trước khi chạy G0b
- [ ] (TV-A, 13–14/11) Chạy G0b; lưu kết quả; ghi nhật ký GPU
- [ ] (TV-B, 16/11) Kiểm lại độc lập 8 điểm đọc từ repo gốc (§8); đọc `data_check` của G0b
- [ ] (Cả hai, 17/11) G-N: "Cited by" trên Google Scholar; đọc Makarov 2610.40055 và Duan 2606.03002
- [ ] (TV-A, 18/11) Kiểm GPT-QModel với `gpt_neox` trên Pythia-70M
- [ ] (Cả hai, 22/11) Chốt G0; cập nhật đề xuất lên v0.6 (dự toán tính toán mới, D-08, D-09)
- [ ] (TV-A, 23–30/11) Đề cương theo mẫu FIT; gửi thầy kèm 5 câu hỏi ở §7
- [ ] Ghi lần nhận xét thứ 3 vào `NHAN_XET_GVHD.md`; đóng sổ đề tài cũ lên v1.4
- [ ] Thêm `NHAN_XET_GVHD.md`, PDF CausalGym, PDF Makarov vào Claude Project

## 6. Nhật ký GPU

Kaggle tính quota theo thời gian phiên. Ghi mỗi lần chạy để biết còn bao nhiêu. Số phút lấy từ `run_summary.json` (chỉ tính thời gian job, chưa tính khởi động phiên).

| Ngày | Tài khoản | Việc | Model | Giờ GPU | Ghi chú |
|---|---|---|---|---|---|
| 12/11/2026 | TV-A | `20261112_1441_g0_full` (G0 full + timing 1B) | 410M, 1B | 0,09 | 2 job: 4,2 + 1,3 phút |

## 7. Câu hỏi gửi GVHD

1. CausalGym có đạt yêu cầu "bài báo gốc" không?
2. MVP (tái lập + C1 + C2 cấp biến + C3b; C3 và C4 là Target) có hợp lý không?
3. Kết quả "cơ chế được bảo toàn" có được tính là kết quả nếu quy tắc đã đăng ký trước không?
4. Có được dùng checkpoint GPTQ công khai của Ouyang et al. (Pythia deduped) không?
5. Hạn đề cương chính thức là ngày nào?

## 8. Sổ nguồn

| Nguồn | Trạng thái | Ghi chú |
|---|---|---|
| CausalGym, ACL 2024 (arXiv 2402.12560) | [ĐCM] đọc toàn văn | Pythia-1B: DAS 10.74, probe 3.66; selectivity 6.9B: DAS 2.48 < probe 3.79; checkpoint 1K/2K/3K/10K |
| Repo gốc `aryamanarora/causalgym`, commit `0f3129f` (30/11/2024) | [ĐCM] Claude đọc code 12/11/2026; **TV-B kiểm lại độc lập** | 8 điểm, xem bảng dưới |
| Ouyang et al., ACL 2025 (arXiv 2411.17691) | [ĐCM] trang ACL + arXiv | Checkpoint GPTQ Pythia deduped trên HF `Xu-Ouyang`; số checkpoint mỗi cỡ chưa xác minh |
| Zhou et al., Findings ACL 2026 (2026.findings-acl.1162) | [ĐCM] trang ACL | File `2026.findings-acl.642` nhóm tải là bài khác (speech LLM) |
| Duan, arXiv 2606.03002 | [ĐCM] trang arXiv | SAE + RTN, Pythia-70M, Gemma-2-2B |
| Makarov, arXiv 2610.40055 | [ĐCM] PDF | Steering OT theo cụm dưới INT8/NF4; kiểm định tương đương; so chuyển từ FP với học lại |
| Faumi & Sumanathilaka, arXiv 2610.37157 | [ĐCM] PDF | GPT-2 và DistilGPT-2; IOI sụp, Greater-Than được ánh xạ lại |
| Grant et al., ICLR 2026 Oral (arXiv 2511.04638) | [ĐCM] trang ICLR + slide | EMD đo độ lệch can thiệp |
| Kumon & Yanaka, ACL 2026 | [ĐCM] trang ACL | DAS dễ overfit; dùng activation patching |
| Sutter et al., NeurIPS 2025 | [ĐCM] trang arXiv | IIA cao cả trên model ngẫu nhiên |
| Catalan-Tatjer et al., ICLR 2026 (arXiv 2510.06213) | [ĐCM] trang | Động lực learning rate quyết định độ bền PTQ |
| Armstrong, arXiv 2604.15167 | [ĐCM] trang arXiv | Pythia-160m, 154 checkpoint, khoảng cách INT4 tăng 11% → 517% |
| Chang et al., EMNLP 2025 | [ĐCM] trang ACL | Cross-model activation patching; độ lớn residual dự báo lỗi |
| Chen et al., arXiv 2609.11716 | [ĐCM] trang arXiv | Lỗi mới triệt tiêu lỗi kế thừa |
| CircuitKIT, arXiv 2607.19317 | [ĐCM] trang arXiv | Lý do bỏ C5 |
| Boguraev et al., arXiv 2608.28924 | [GỢI Ý] | Tồn tại; đồng tác giả và mô hình hỗn hợp chưa kiểm |
| Repo `iamartyaa/quant-lens` | [CHƯA XÁC MINH] | Không tìm thấy |

**Repo gốc — 8 điểm đã đọc** (commit `0f3129f`; TV-B ghi "khớp" hoặc "khác" vào cột cuối):

| # | Điểm | File:dòng | So với notebook 00 | TV-B |
|---|---|---|---|---|
| 1 | Odds = (log p_base(y_base) − log p_base(y_src)) + (log p_int(y_src) − log p_int(y_base)), dùng log-softmax | `eval.py:72` | Trùng: hiệu log-softmax bằng hiệu logit | |
| 2 | Loss khi học DAS = cross-entropy về nhãn src | `eval.py:10`, `train.py:75` | Trùng | |
| 3 | Template thêm `<\|endoftext\|>` ở đầu câu | `data.py:175` | Phụ thuộc dữ liệu HF có giữ chuỗi này không; G0b kiểm bằng `data_check.first_token_is_eos` | |
| 4 | Mỗi batch gồm các cặp mẫu và cặp đảo của chúng | `data.py:335` | Khớp với số liệu G0: 100 câu không trùng, mỗi câu đúng một lần làm base và một lần làm src | |
| 5 | Chủ ngữ của base và src là hai danh từ chọn độc lập; nhãn chọn độc lập trong {is, was, has} / {are, were, have} | `data.py:240`, `data.py:257` | Logit diff trộn số với thì; giữ nguyên để tái lập | |
| 6 | Eval loại câu đã có trong train | `das.py:76–83` | Chưa biết với split HF; G0b kiểm bằng `data_check.eval_sentences_in_train` | |
| 7 | Bảng tổng hợp: max theo vị trí ở mỗi layer → trung bình qua layer → trung bình qua tác vụ; selectivity = odds − odds tác vụ đối chứng "dog-give" | `plot.py:322`, `plot.py:328–330` | G0 chưa so được (chỉ 5 layer × 2 vùng); G0b tính chỉ số này cho 1 tác vụ | |
| 8 | Token hoá cả câu, rồi căn vùng bằng token hoá từng vùng | `data.py:49`, `data.py:63` | Notebook nối token từng vùng; G0b kiểm bằng `data_check.tok_mismatch` | |

## 9. G0 — cách chạy và kết quả

**Cách chạy** (theo `QUY_TRINH_LAM_VIEC.md`):
- Notebook: `notebooks/00_g0_pilot.ipynb`.
  - Bản 1 (commit `1232ff0`) cho G0 full.
  - Bản 2 cho G0b (D-08, D-09), cấu hình nén dạng `QCONFIGS = [[bit, α], ...]`.
- Job G0b trong `configs/kaggle_run.yaml`: `g0b_smoke_410m` rồi `g0b_full_410m`, cùng một version. Các bước chi tiết nằm trong `VIEC_CAN_LAM.md`.
- Nếu tải dữ liệu lỗi, thêm `"datasets>=3"` vào mục `pip:` trong file cấu hình.

**Run đã chạy:**

| run_id | Commit | Job | Trạng thái | Phút |
|---|---|---|---|---|
| (smoke bản 1, chưa ghi) | | g0_smoke_410m | | |
| 20261112_1441_g0_full | 1232ff0 | g0_full_410m | ok | 4,2 |
| 20261112_1441_g0_full | 1232ff0 | g0_timing_1b | ok | 1,3 |

**Kết quả G0 full** (tác vụ `agr_sv_num_subj-relc`, split validation: 100 cặp = 50 cặp độc lập × 2 chiều; T4, fp32, torch 2.11, transformers 5.20.2):

| Chỉ số | 410M | 1B |
|---|---|---|
| t học + đánh giá một ô (giây) | 7,55 (học 6,8 + đánh giá 0,75; trung vị 15 lần học, 10 lần đánh giá) [ĐCM cho tác vụ này] | 9,21 (học 7,34 + đánh giá 1,87; chỉ 2 lần, 1 layer) [GỢI Ý] |
| Accuracy / logit diff FP | 0,97 / 3,29 (100 câu không trùng) | 0,99 / 3,96 |
| Odds FP theo ô đã đo (vùng 1 / vùng 5) | L0: 6,62 / 0,02 · L6: 4,81 / 0,15 · L12: 4,28 / 1,09 · L17: 5,25 / 4,91 · L23: 0,00 / 8,70 | L8: 5,36 / 1,31 |
| Odds FP cao nhất | 8,70 (L23, vùng 5: ô đầu ra, tầm thường); trừ layer cuối: 6,62 (L0, vùng 1) | — |
| Accuracy theo bit 8/6/4/3 | 0,97 / 0,97 / 0,97 / 0,79 | 4 bit: 0,99 |
| Sai số tương đối trọng số theo bit 8/6/4/3 | 0,006 / 0,023 / 0,098 / 0,210 | 4 bit: 0,102 |
| Accuracy theo α (4 bit) 0,25/0,5/0,75 | 0,97 / 0,97 / 0,97 | — |
| T dùng lại ở ô chính, bit 8/6/4/3 | 0,991 / 0,964 / 0,955 / 0,752 (chưa có khoảng tin cậy) | 4 bit: 1,003 |
| T theo α (4 bit) 0,25/0,5/0,75 | 1,011 / 0,999 / 0,980 | — |
| Spearman bản đồ dùng lại theo bit | 1,0 ở mọi mức (10 ô); không phân biệt được | — (2 ô) |
| Odds học lại trên Q 8/4/3 bit, \|cos\| với FP | 6,56 / 6,31 / 5,23; \|cos\| 0,999 / 0,945 / 0,754. Cùng seed 0 với FP, nên **không** so được với null theo seed | — |
| Tách đoạn 4 bit: odds pre / post / all | 6,54 / 6,46 / 6,32 (ô L0, nên "pre" chỉ gồm 1 layer) | 5,54 / 5,23 / 5,38 (L8) |
| Sàn step0 (odds) | 0,225 = 3,4% odds FP (L0, vùng 1) | — |
| \|cos\| giữa seed; khoảng odds | min 0,891, TB 0,895 (k = 3); odds 6,54–6,62 | — |
| Quyết định theo §4 | Xem bảng áp quy tắc ở §4. G0 một phần, chờ G0b | — |

**Ghi chú đo lường:**
- Vùng của tác vụ này (theo template repo gốc, khớp `n_regions = 6`, `diff_region = 1`): 0 `<|endoftext|>The`, 1 chủ ngữ, 2 ` that`, 3 động từ trong mệnh đề, 4 ` the`, 5 tân ngữ. Ví dụ cụ thể sẽ in ở `data_check` của G0b. [ĐCM template; ánh xạ sang dữ liệu HF: GỢI Ý]
- Ô biên đóng vai trò kiểm tra: L23/vùng 1 cho odds đúng 0, vì không còn đường tới token cuối, nên hook không rò [ĐCM]. L0/vùng 5 ≈ 0 vì thông tin chủ ngữ chưa tới [GỢI Ý].
- Chưa so được với con số của bài gốc (DAS 10,74 cho 1B), vì cách tổng hợp khác (§8, điểm 7).
- Dự toán tính toán trong đề xuất v0.5 §7 (t = 20–60 s) quá cao. Với t = 7,55 s: 3.000 lần ≈ 6,3 giờ; 10.000 lần ≈ 21 giờ GPU cho 410M [ĐCM cho tác vụ này; tác vụ câu dài hơn sẽ chậm hơn]. Cập nhật ở đề xuất v0.6.
- Các dấu hiệu dừng đặt trước (FP accuracy < 0,7; odds FP ≈ 0 ở mọi ô; 8 bit tụt mạnh) đều không xảy ra.

**Kết quả G0b:** (điền sau khi chạy)

## Changelog
- v0.3 (12/11/2026): điền §9 kết quả G0 full; áp 4 quy tắc G0 (§4: G0 một phần); thêm D-08 (ô chính mới, sau dữ liệu, chờ xác nhận), D-09 (sửa cách đo, sau dữ liệu), D-10 (định dạng VIEC_CAN_LAM); §6 dòng GPU đầu tiên; §8 thêm repo gốc và 8 điểm đối chiếu; §5 cập nhật việc cần làm.
- v0.2 (12/11/2026): thêm D-07 (quy trình GitHub → Kaggle runner, Save Version, notebook-first); thay script `g0_pilot.py` bằng notebook `00_g0_pilot.ipynb` chạy qua `configs/kaggle_run.yaml`; §9 thêm bảng run.
- v0.1 (12/11/2026): tạo sổ; ghi D-01 đến D-06; cổng G-N…G3; quy tắc G0; sổ nguồn; hướng dẫn chạy G0.
