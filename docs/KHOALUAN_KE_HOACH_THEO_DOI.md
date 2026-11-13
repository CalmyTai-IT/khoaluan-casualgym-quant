# KHOALUAN_KE_HOACH_THEO_DOI.md — Sổ dự án khoá luận

> Version: v0.4 · Ngày: 13/11/2026 · Nguồn sự thật của project. Đề xuất chi tiết: `DEXUAT_HUONG_B1_DAS.md` v0.6. Quy trình: `QUY_TRINH_LAM_VIEC.md` (bản 13/11). Việc trước mắt: `VIEC_CAN_LAM.md`.
> Quy ước: [ĐCM] đã kiểm chứng · [GỢI Ý] bằng chứng chưa đủ · [PHỎNG ĐOÁN] chưa kiểm.
> Từ v0.4, Claude tự cập nhật sổ từ file kết quả người dùng gửi (D-14, QT-44). Mọi số của G0b tái tạo được bằng `notebooks/00b_phan_tich_g0b.ipynb` (QT-32).

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
| Tác vụ | 4 tác vụ (D-13, chờ xác nhận): `agr_sv_num_subj-relc` (tác vụ phát triển, đã nhìn dữ liệu ở G0), `npi_any_subj-relc`, `filler_gap_subj`, `cleft` |

## 2. Trạng thái hiện tại (13/11/2026)

- **G0 đạt (đóng 13/11).** Run G0b `20261113_0506_g0b`, commit `b22a2a4`, 2 job `ok`. Kết quả ở §9; áp quy tắc ở §4.
- Quy tắc chọn ô chính D-08 chọn L22/vùng 5, sát đầu ra; tách đoạn ở đó suy biến. Đề xuất bỏ "một ô chính", đo theo mọi layer (D-11).
- T gần như chỉ theo mức co biên độ đầu ra (tương quan 0,997). Đề xuất chuẩn hoá (D-12).
- Đã chuẩn bị G1: `notebooks/01_tai_lap_causalgym.ipynb` (đã chạy TOY_TEST trên CPU) và `configs/kaggle_run.yaml`. **Chờ nhóm xác nhận D-13** (4 tác vụ và tiêu chí G1) trước khi chạy.
- Đề xuất cập nhật lên v0.6 (Claude, 13/11).
- Đang làm: G1 (chờ xác nhận), G-N. Chưa gửi thầy.

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
| D-08 | 12/11/2026 | **Sau dữ liệu (G0 full).** Đổi quy tắc chọn ô chính sang `last_early`: chỉ xét vùng cuối, layer 1 đến L−2; chọn layer sớm nhất có odds FP ≥ 0,8 × odds lớn nhất của vùng cuối trên các layer đó. **Đã xác nhận và chạy ở G0b (13/11).** Quy tắc chọn **L22**/vùng 5; xem D-11 | Quy tắc cũ chọn L0/vùng 1: residual ngay sau khối đầu, tại chính token chủ ngữ, nên can thiệp gần như thay token. C2 tách đoạn ở đó suy biến (phía mã hoá chỉ 1/24 layer) |
| D-09 | 12/11/2026 | **Sau dữ liệu (G0 full).** Sửa cách đo (notebook 00 bản 2): (i) bootstrap theo cụm; (ii) hành vi trên câu không trùng; (iii) học lại trên Q với k seed, so \|cos\| theo cặp seed khác nhau; (iv) Spearman trên ô có odds FP ≥ 1, thêm T theo ô; (v) lưới G0b dời xuống 3 và 2 bit kèm α | Xem bản v0.3 |
| D-10 | 12/11/2026 | `VIEC_CAN_LAM.md` viết theo bước thời gian, mỗi bước có Cần có / Làm / Xong khi / Nếu không / Ra (QT-41) | Bản trước gom theo mục, khó theo |
| D-11 | 13/11/2026 | **Sau dữ liệu (G0b). Đề xuất, chốt trong SPEC C1 trước notebook 02.** Bỏ "một ô chính" làm căn cứ kết luận. C1 và C2 đo trên **mọi layer** ở hai vùng: vùng khác nhau đầu tiên và vùng cuối. Phần tốn kém (học lại k seed trên FP và Q, sàn step0) cũng chạy ở mọi layer của hai vùng này. Kết luận theo hồ sơ layer, hiệu chỉnh Benjamini–Hochberg như đề xuất §2.4. Ô D-08 (L22/vùng 5) chỉ dùng để báo cáo G0 | (1) Odds vùng 5 nhảy ở L22 (4,81 → 7,33), nên "layer sớm nhất đạt 0,8 × max" rơi đúng L22; ở L22 vùng 1–4 về ≈ 0. Tách đoạn ở L22 suy biến (phía sau chỉ còn L23), đối xứng với lỗi của quy tắc cũ ở L0. Đây là lỗi thiết kế của D-08 (Claude đề xuất), chỉ lộ ra khi có đủ 24 layer. (2) T khác rõ giữa các layer (vùng 5, 4 bit: L13–16 ≈ 0,96, L19–21 ≈ 0,85), nên một ô không đại diện. (3) Với t = 6,41 s, học lại (5 seed FP + 5 seed × 3 cấu hình Q + step0) ở mọi layer của 2 vùng tốn khoảng 1,6 giờ/tác vụ cho 410M, khoảng 12 giờ cho 4 tác vụ × 2 model [PHỎNG ĐOÁN], vẫn trong ngân sách; thiếu thì giảm còn 3 seed. (4) Tránh chọn ô sau khi thấy dữ liệu lần thứ ba |
| D-12 | 13/11/2026 | **Sau dữ liệu (G0b) + Wu et al. (2608.06564). Đề xuất, chốt trong SPEC C1.** Trục (b) báo cáo **T_rel = T / R**, với R = logit diff trung bình của Q chia của FP trên cùng câu eval; khoảng tin cậy lấy bằng bootstrap cụm trên cùng mẫu cho cả T và R. T thô giữ làm số phụ. Độ dốc c (hồi quy logit diff từng câu Q theo FP, cách của Wu et al.) báo cáo kèm. Chỉ tính T_rel khi R đủ xa 0 (ngưỡng chốt trong SPEC) | Qua 9 cấu hình, tương quan giữa R và T trung vị theo ô là 0,997. Ở 3–4 bit, T/R nằm trong 0,93–1,00. Không chuẩn hoá thì trục (a) và (b) gần trùng nhau, cây quyết định §2.4 của đề xuất gần như không bao giờ ra nhánh "Trôi cơ chế". Chọn R làm mẫu số chính vì R hẹp hơn c nhiều (3 bit: R 0,75 [0,68; 0,80], c 0,77 [0,45; 1,10]). **Giới hạn:** T_rel ≈ 1 không phân biệt "đầu ra co lại" với "biến bị mã hoá yếu đi"; muốn tách phải dùng C2 |
| D-13 | 13/11/2026 | **Chờ nhóm xác nhận trước khi chạy G1.** Tái lập G1: (i) 4 tác vụ `agr_sv_num_subj-relc`, `npi_any_subj-relc`, `filler_gap_subj`, `cleft`; Pythia 410M và 1B, fp32. (ii) Eval trên split `test` của HF, là tập seed 1 mà repo gốc dùng. (iii) Đủ 9 phương pháp của bài: DAS, probe × 2, diff-in-means, PCA, k-means, LDA, ngẫu nhiên, vanilla; thêm tác vụ đối chứng dog-give. (iv) Lấy biểu diễn source ở vị trí của source, không theo lỗi đảo vị trí của repo gốc (§8 điểm 9); `POS_MODE = "repo"` để so khi cần. (v) Tiêu chí G1 định lượng ở §4 | 4 họ hiện tượng khác nhau; gồm 2 tác vụ nghiên cứu trường hợp của bài (§6: `npi_any_subj-relc`, `filler_gap_subj`). Accuracy trong bài ≥ 0,89 ở cả 410m và 1b, nên còn chỗ cho nén làm hỏng. `agr_sv_num_subj-relc` đã dùng ở G0 nên là tác vụ phát triển; 3 tác vụ còn lại chưa nhìn dữ liệu. Tiêu chí G1 trong v0.3 chỉ định tính ("đúng thứ tự", "cùng bậc") |
| D-14 | 13/11/2026 | Claude tự cập nhật sổ, nhật ký GPU, bảng run, trạng thái cổng, đề xuất từ file kết quả người dùng gửi; người dùng không phải điền số. Kết quả run được Claude đưa vào zip trả về. Quy trình: QT-13, QT-30, QT-31, QT-32, QT-41, QT-42, QT-44 | Người dùng yêu cầu; điền tay mất thời gian và dễ sai (dòng G0b trong v0.3 ghi "0.5" và gộp hai job vào một ô) |

## 4. Cổng quyết định

| Cổng | Hạn | Điều kiện đạt | Trạng thái | Nếu không đạt |
|---|---|---|---|---|
| G-N tính mới | 17/11/2026 | "Cited by" của CausalGym, Ouyang, Duan, Makarov; tìm thêm; không ai đã làm C1/C2/C3b | Đang làm. Đã thêm 4 bài lân cận (§8): Tanyel & Ayvaz, Wu et al., Yao et al., Bhandari & Wade. Chưa thấy bài nào đo DAS/DII dưới lượng tử hoá trên CausalGym [GỢI Ý] | Bỏ hoặc đổi đóng góp bị trùng |
| G0 chạy được | 22/11/2026 | Chạy hết `notebooks/00_g0_pilot.ipynb` trên 410M; có t; có vùng chuyển tiếp; có sàn step0; đo t cho 1B | **Đạt (13/11/2026).** Xem bảng áp quy tắc ở G0b dưới đây | — |
| G1 tái lập | 31/12/2026 (có thể dời 15/01/2027) | Tiêu chí D-13, xét riêng cho từng model (410M, 1B), đạt cả ba:<br>(1) **Thứ tự phương pháp:** Kendall τ_b ≥ 0,7 giữa odds trung bình 4 tác vụ của mình và của bài gốc (9 phương pháp), và DAS đứng đầu.<br>(2) **Thứ tự vị trí** (tiêu chí tối thiểu): layer xuất hiện của vùng khác nhau đầu tiên ≤ layer xuất hiện của vùng cuối ở ≥ 3/4 tác vụ. Layer xuất hiện = layer đầu tiên có odds DAS ≥ 0,5 × max của vùng đó.<br>(3) **Cùng bậc:** ≥ 12/16 cặp (tác vụ × {DAS, probe tốt hơn, diff-in-means, vanilla}) có tỉ lệ mình/bài gốc trong [0,5; 2].<br>Kiểm tra phụ: accuracy tác vụ lệch ≤ 0,05 | Chưa chạy. Notebook 01 in sẵn ba tiêu chí (`g1_check.json`) | Dừng phát triển; sửa pipeline; chạy `POS_MODE = "repo"` để xem lệch có do lỗi vị trí của repo gốc không; hỏi tác giả |
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
| 3 | Sàn = 3,4% odds FP | (b') có thông tin **ở ô cũ** |
| 4 | \|cos\| min 0,891, TB 0,895 (k = 3) | Trục (c) không dùng được **ở ô cũ** |

**Kết quả áp quy tắc ở G0b** (13/11/2026, ô D-08 = L22/vùng 5, 410M, `agr_sv_num_subj-relc`):

| Quy tắc | Số đo | Kết luận |
|---|---|---|
| 1 | t = 6,41 s (học 5,66 + đánh giá 0,74; trung vị 135 lần học) | Giữ kế hoạch |
| 2 | Lưới {4 bit; 3 bit; 2 bit α0,5; 2 bit α0,75}: accuracy 0,97 → 0,79 → 0,64 → 0,52; logit diff 3,14 → 2,46 → 0,62 → 0,005. 8 bit = 0,97 (không sụp) | **Đạt.** 8 bit giữ làm mức kiểm tra. Ưu tiên mức bit thật (α = 1); chỉ dùng α ở dải không có mức bit nào. 2 bit α1,0 (0,62) không đơn điệu so với α0,75 (0,52) nên không dùng |
| 3 | Sàn step0 = 0,39 = 5,3% odds FP | (b') có thông tin **ở ô này**. Ô sát đầu ra nên sàn thấp là dễ hiểu; đo lại theo layer (D-11) |
| 4 | \|cos\| giữa seed min 0,967, TB 0,976 (k = 5) | Trục (c) dùng được **ở ô này**. Ở L0/vùng 1 là 0,891, nên độ ổn định phụ thuộc ô; đo theo layer (D-11) |

**Kết luận G0:** đạt mọi điều kiện của cổng (chạy hết, có t, có vùng chuyển tiếp, có sàn step0, có t cho 1B). Hai vấn đề thiết kế chuyển sang SPEC C1, không chặn G1: chọn ô (D-11) và chuẩn hoá T (D-12).

## 5. Việc cần làm

- [x] (TV-A, 12/11) Thiết lập repo và Kaggle runner; G0 full 410M + đo thời gian 1B
- [x] (TV-A, 13/11) Lưu kết quả G0 full vào `results/` (làm trước commit `b22a2a4`)
- [x] (Cả hai, 13/11) Xác nhận D-08; chạy G0b
- [x] (Claude, 13/11) Phân tích G0b; chốt G0; viết notebook 01 và 00b; cập nhật đề xuất v0.6, sổ v0.4, quy trình
- [ ] (Cả hai, 14/11) Xác nhận D-13 (4 tác vụ + tiêu chí G1), rồi chạy G1 (`VIEC_CAN_LAM.md`)
- [ ] (TV-B, 16/11) Kiểm lại độc lập 12 điểm đọc từ repo gốc (§8), nhất là điểm 9 (đảo vị trí) và 10 (split eval)
- [ ] (Cả hai, 17/11) G-N: "Cited by" trên Google Scholar; đọc Makarov 2610.40055, Duan 2606.03002, Tanyel & Ayvaz 2611.05033, Wu et al. 2608.06564
- [ ] (TV-A, 18/11) Đọc toàn văn Tanyel & Ayvaz, Phụ lục E.1 (dựng lại bản đồ CausalGym). Claude chưa đọc được toàn văn (trang HTML bị giới hạn truy cập trong phiên 13/11)
- [ ] (TV-A, 18/11) Kiểm GPT-QModel với `gpt_neox` trên Pythia-70M
- [ ] (Claude, sau G1) SPEC C1/C2 (chốt D-11, D-12, biên tương đương, ngưỡng R) và notebook 02
- [ ] (TV-A, 23–30/11) Đề cương theo mẫu FIT; gửi thầy kèm các câu hỏi ở §7
- [ ] Ghi lần nhận xét thứ 3 vào `NHAN_XET_GVHD.md`; đóng sổ đề tài cũ lên v1.4
- [ ] Thêm `NHAN_XET_GVHD.md`, PDF Makarov vào Claude Project

## 6. Nhật ký GPU

Kaggle tính quota theo thời gian phiên. Số phút lấy từ `run_summary.json` (chỉ tính thời gian job, chưa tính khởi động phiên). Claude ghi bảng này (QT-13).

| Ngày | Tài khoản | Việc | Model | Giờ GPU | Ghi chú |
|---|---|---|---|---|---|
| 12/11/2026 | TV-A | `20261112_1441_g0_full` (G0 full + timing 1B) | 410M, 1B | 0,09 | 2 job: 4,2 + 1,3 phút |
| 13/11/2026 | TV-B | `20261113_0506_g0b` (G0b) | 410M | 0,51 | 2 job: 1,7 + 28,7 phút |

Tổng đã dùng: 0,60 giờ. G1 dự kiến khoảng 6,5–7 giờ [PHỎNG ĐOÁN].

## 7. Câu hỏi gửi GVHD

1. CausalGym có đạt yêu cầu "bài báo gốc" không?
2. MVP (tái lập + C1 + C2 cấp biến + C3b; C3 và C4 là Target) có hợp lý không?
3. Kết quả "cơ chế được bảo toàn" có được tính là kết quả nếu quy tắc đã đăng ký trước không?
4. Có được dùng checkpoint GPTQ công khai của Ouyang et al. (Pythia deduped) không?
5. Hạn đề cương chính thức là ngày nào?
6. Code gốc của CausalGym lấy biểu diễn source ở vị trí của base (§8 điểm 9). Tái lập theo đúng công thức của bài (nhóm đang làm), có báo cáo kèm bản theo code gốc, có được không?

## 8. Sổ nguồn

| Nguồn | Trạng thái | Ghi chú |
|---|---|---|
| CausalGym, ACL 2024 (arXiv 2402.12560) | [ĐCM] đọc toàn văn | Pythia-1B: DAS 10.74, probe 3.66; selectivity 6.9B: DAS 2.48 < probe 3.79; checkpoint 1K/2K/3K/10K. Số theo tác vụ: Table 11 (410m), Table 13 (1b). Phụ lục B: ≤ 410m chạy fp32, 1b bfloat16; eval 50 cặp + cặp đảo, "không trùng train" |
| Repo gốc `aryamanarora/causalgym`, commit `0f3129f` (30/11/2024) | [ĐCM] Claude đọc code 12/11 và 13/11/2026 (clone lại 13/11); **TV-B kiểm lại độc lập** | 12 điểm, bảng dưới |
| Dataset HF `aryaman/causalgym` | [ĐCM] trang HF | 3 split: train 11,6k, validation 2,9k, test 2,9k dòng; README: "exactly as used in the experiments in the paper"; file gốc `train.json`, `dev.json`, `test.json` |
| Ouyang et al., ACL 2025 (arXiv 2411.17691) | [ĐCM] trang ACL + arXiv | Checkpoint GPTQ trên HF `Xu-Ouyang`, dạng `pythia-<cỡ>-deduped-int{2,3,4,8}-step<k>-GPTQ-wikitext2` [ĐCM trang HF]. Là Pythia **deduped**: nếu dùng phải chạy cả FP deduped |
| Zhou et al., Findings ACL 2026 (2026.findings-acl.1162; arXiv 2604.19884) | [ĐCM] trang ACL + arXiv | "From Signal Degradation to Computation Collapse: Uncovering the Two Failure Modes of LLM Quantization", tr. 23204–23222. 4 bit: tín hiệu yếu đi, mẫu tính toán còn; 2 bit: thành phần then chốt hỏng, tín hiệu mất từ layer sớm. File `2026.findings-acl.642` nhóm tải là bài khác |
| Tanyel & Ayvaz, arXiv 2611.05033 (3/11/2026) | [ĐCM] trang tóm tắt arXiv + đoạn HTML qua tìm kiếm; **chưa đọc toàn văn** | "Whose Effect Is It? How Objectives Inflate Learned Subspace Interventions". Phần DAS vượt patch cả trạng thái (vanilla) trên CausalGym chủ yếu đến từ hàm mục tiêu, không phải vùng tốt hơn; đổi mục tiêu thì phần vượt mất phần lớn. Phụ lục E.1 chỉ ra code CausalGym truyền vị trí base/source đảo thứ tự (điểm 9, Claude tự xác nhận trong code). Chi tiết "chứng minh Lean" do Gemini nêu: chưa kiểm |
| Wu, Dhiman, Koshiyama, arXiv 2608.06564 (8/2026) | [ĐCM] trang tóm tắt | "Which Decisions Low-Bit Quantization Breaks, and How to Predict Them". 16 model, RTN/AWQ/GPTQ/GGUF, 8 xuống 2 bit: biên quyết định bị **nhân** với hệ số co (trung vị 0,86 ở 4 bit, 0,33 ở 3 bit, 0,00 ở 2 bit), gọi là *margin shrinkage*. Cơ sở cho D-12. Câu trích §6.1 do Gemini nêu: chưa kiểm |
| Yao, Boguraev, Pimentel, Mahowald, EMNLP 2026 (arXiv 2610.33299) | [ĐCM] trang arXiv + ACL Anthology | "The Emergence and Sparsification of a Syntactic Circuit". Mạch subject–verb agreement trên pythia-1b và 10 seed pythia-410m qua checkpoint: học sớm, ban đầu phân tán; sau khi hành vi ổn định, mạch vẫn tổ chức lại và thu nhỏ; mạch cuối của 1b rất thưa. Tiên nghiệm cho C3b. Chi tiết "18 neuron + 1 head" do Gemini nêu: chưa kiểm |
| Bhandari & Wade, arXiv 2609.06473 (9/2026) | [ĐCM] trang tóm tắt | "Steering Under Compression: Dose-Response, Capability Cost, and Failure Asymmetry in Quantized LLMs". INT8/NF4, 4 model 7–9B; quy tắc ba nhãn đặt trước; cos vector steering với FP16: 0,989–0,998 (INT8), 0,945–0,990 (NF4). Mẫu cho D-05 |
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
| Boguraev et al., arXiv 2608.28924 | [ĐCM] tiêu đề | "Causal Interventions Reveal Typologically Organized Syntactic Mechanisms in Multilingual Language Models" (Boguraev và 3 tác giả). DII/DAS đa ngữ, không về nén. Danh sách đồng tác giả chưa kiểm hết |
| Repo `iamartyaa/quant-lens` | [ĐCM] Claude clone 13/11/2026 | Có tồn tại. SAE + TransformerLens/SAELens trên GPT-2 small (Gemma 2 2B dự định); không dùng Pythia, CausalGym hay DAS. Không trùng |
| Wilam, arXiv 2611.09204 | [CHƯA XÁC MINH] | Gemini nêu ("representational drift in a code model"); tìm không thấy |
| "Perturbation Ladder for SAE", Zenodo 22700831 | [CHƯA XÁC MINH] | Gemini nêu; chưa tìm |

**Repo gốc — 12 điểm đã đọc** (commit `0f3129f`; TV-B ghi "khớp" hoặc "khác" vào cột cuối):

| # | Điểm | File:dòng | So với notebook của nhóm | TV-B |
|---|---|---|---|---|
| 1 | Odds = (log p_base(y_base) − log p_base(y_src)) + (log p_int(y_src) − log p_int(y_base)), dùng log-softmax | `eval.py:72` | Trùng: hiệu log-softmax bằng hiệu logit | |
| 2 | Loss khi học DAS = cross-entropy về nhãn src | `eval.py:10`, `train.py:75` | Trùng | |
| 3 | Template thêm `<\|endoftext\|>` ở đầu câu | `data.py:175` | G0b: `first_token_is_eos` = 1,0 [ĐCM] | |
| 4 | Mỗi batch gồm các cặp mẫu và cặp đảo của chúng | `data.py:335` | G0b: `eval_swap_frac` = 1,0; 100 cặp = 50 cụm [ĐCM] | |
| 5 | Chủ ngữ của base và src chọn độc lập; nhãn chọn độc lập trong {is, was, has} / {are, were, have} | `data.py:240`, `data.py:257` | Ví dụ G0b: base "are", src "has". Logit diff trộn số với thì; giữ nguyên để tái lập | |
| 6 | Loại trùng: chỉ kiểm câu **base** của cặp vừa lấy mẫu với tập train, rồi mới thêm cặp đảo, nên câu src (thành base của cặp đảo) có thể trùng train | `das.py:76–83`, `data.py:305`, `data.py:335` | G0b: 2/100 câu eval có trong train, khớp cách làm này (bài viết ở Phụ lục B là "không trùng"). Giữ nguyên để tái lập | |
| 7 | Bảng tổng hợp: max theo vị trí ở mỗi layer → trung bình qua layer → trung bình qua tác vụ; selectivity = odds − odds dog-give, lấy max riêng | `plot.py:322`, `plot.py:328–330` | Notebook 01 tính cả odds và selectivity đúng như vậy; notebook 00 chỉ có odds. G0b: 5,24 so với 4,97 của bài | |
| 8 | Token hoá cả câu, rồi căn vùng bằng token hoá từng vùng | `data.py:49`, `data.py:63` | Notebook nối token từng vùng. G0b: `tok_mismatch` = 0/500 [ĐCM cho tác vụ này]; notebook 01 kiểm từng tác vụ | |
| 9 | **Vị trí can thiệp bị đảo:** `compute_pos` trả [vị trí src, vị trí base]; lời gọi pyvene dùng `pos_interv[1]` (vị trí base) làm vị trí lấy source, và đơn vị Collect (dữ liệu cho probe/mean/PCA) lấy base ở vị trí src. Chỉ có tác dụng khi base và src khác độ dài token | `data.py:138–140`, `train.py:58–62`, `eval.py:27–31` | Notebook 00/01 lấy source ở vị trí của source. Notebook 01 có `POS_MODE = "repo"` để tái hiện. Tanyel & Ayvaz (Phụ lục E.1) nêu cùng lỗi | |
| 10 | Tập eval của bài là seed 1 (`eval_seed = 1`); dataset HF xuất train seed 42, dev seed 420, test seed 1 | `das.py:82–83`, `data.py:390–398` | G0/G0b dùng split `validation` (dev). G1 dùng `test` (D-13) | |
| 11 | dtype: 410m fp32, 1b bfloat16 | `utils.py:27–37` | Nhóm luôn fp32 (D-04); ghi khác biệt khi so 1b | |
| 12 | Probe: LogisticRegression saga, L2, có bias, C = 1e-4 và 1e-5 (410m), 1e-5 và 1e-6 (1b); dog-give gán " dog" cho `types[0]` = khoá đầu của `labels` trong template | `diff_methods.py:56–126`, `data.py:178`, `data.py:323–326` | Notebook 01 giống; thứ tự loại của 4 tác vụ ghi sẵn trong notebook | |

## 9. G0 — cách chạy và kết quả

**Cách chạy** (theo `QUY_TRINH_LAM_VIEC.md`):
- Notebook: `notebooks/00_g0_pilot.ipynb`. Bản 1 (commit `1232ff0`) cho G0 full; bản 2 (commit `b22a2a4`) cho G0b.
- Phân tích lại G0b trên CPU: `notebooks/00b_phan_tich_g0b.ipynb` (tái tạo mọi số dưới đây).

**Run đã chạy:**

| run_id | Commit | Job | Trạng thái | Phút |
|---|---|---|---|---|
| (smoke bản 1) | — | g0_smoke_410m | không còn số liệu | — |
| 20261112_1441_g0_full | 1232ff0 | g0_full_410m | ok | 4,2 |
| 20261112_1441_g0_full | 1232ff0 | g0_timing_1b | ok | 1,3 |
| 20261113_0506_g0b | b22a2a4 | g0b_smoke_410m | ok | 1,7 |
| 20261113_0506_g0b | b22a2a4 | g0b_full_410m | ok | 28,7 |

**Kết quả G0 full** (tác vụ `agr_sv_num_subj-relc`, split validation: 100 cặp = 50 cặp độc lập × 2 chiều; T4, fp32, torch 2.11, transformers 5.20.2):

| Chỉ số | 410M | 1B |
|---|---|---|
| t học + đánh giá một ô (giây) | 7,55 (học 6,8 + đánh giá 0,75) [ĐCM cho tác vụ này] | 9,21 (học 7,34 + đánh giá 1,87; chỉ 2 lần, 1 layer) [GỢI Ý] |
| Accuracy / logit diff FP | 0,97 / 3,29 (100 câu không trùng) | 0,99 / 3,96 |
| Accuracy theo bit 8/6/4/3 | 0,97 / 0,97 / 0,97 / 0,79 | 4 bit: 0,99 |
| Sai số tương đối trọng số theo bit 8/6/4/3 | 0,006 / 0,023 / 0,098 / 0,210 | 4 bit: 0,102 |
| Sàn step0 (L0/vùng 1) | 0,225 = 3,4% odds FP | — |
| \|cos\| giữa seed (L0/vùng 1) | min 0,891, TB 0,895 (k = 3) | — |

(Các dòng khác của G0 full xem bản v0.3; phần lớn được thay bằng số G0b đầy đủ hơn.)

**Kết quả G0b** (13/11/2026; cùng tác vụ, split, máy và thư viện; 24 layer × 5 vùng = 116 ô; nén RTN bất đối xứng g = 128 trên 4 ma trận Linear mỗi khối):

| Chỉ số | Giá trị |
|---|---|
| Kiểm dữ liệu | `first_token_is_eos` 1,0; `tok_mismatch` 0/500; `eval_sentences_in_train` 2/100 (khớp cách loại trùng của repo gốc, §8 điểm 6); `eval_swap_frac` 1,0; ví dụ: `<\|endoftext\|>The · managers · that · injured · the · pilot` → "are" / "has" |
| Accuracy / logit diff FP | 0,97 / 3,29 (bài gốc: accuracy 0,97) |
| Bản đồ FP | Vùng 1 (chủ ngữ): 3,96–6,62 ở L0–L21. Vùng 2 (` that`): tăng từ L2, 3,3–3,7 ở L5–L12, rơi còn 1,34 ở L13. Vùng 5 (vị trí dự đoán): ≤ 1,1 tới L12, **nhảy lên 3,35 ở L13**, 3,3–4,9 ở L13–L21, 7,33 ở L22, 8,70 ở L23. Ở L22, vùng 1–4 về ≈ 0,03–0,06 [ĐCM, 1 seed/ô] |
| Odds kiểu bài gốc | **5,24**; bài gốc **4,97** (Table 11; tỉ lệ 1,05). Khác: split (validation so với test), vị trí source |
| Ô chính D-08 | L22/vùng 5, odds 7,33 (5 seed: 7,33–7,48) |
| Hành vi theo (bit, α): accuracy / logit diff / sai số tương đối trọng số | (8, 1): 0,97 / 3,26 / 0,006 · (4, 1): 0,97 / 3,14 / 0,098 · (3, 0,5): 0,96 / 3,03 / 0,105 · (3, 0,75): 0,92 / 2,75 / 0,158 · (3, 1): 0,79 / 2,46 / 0,210 · (2, 0,25): 0,88 / 1,83 / 0,122 · (2, 0,5): 0,64 / 0,62 / 0,244 · (2, 0,75): 0,52 / 0,005 / 0,366 · (2, 1): 0,62 / 0,31 / 0,488 |
| T ở L22 [KTC 95% theo cụm] | 8 bit 0,990 [0,988; 0,992] · 4 bit 0,918 [0,893; 0,945] · 3 bit 0,693 [0,642; 0,745] · 2 bit α0,5 0,222 [0,187; 0,260] · 2 bit α0,75 −0,02 [−0,11; 0,06] |
| Spearman bản đồ (57 ô có odds FP ≥ 1) | 8 bit 1,00 · 4 bit 0,99 · 3 bit 0,97 · 2 bit α0,25 0,75 · α0,5 0,58 · α0,75 −0,43 |
| Học lại trên Q ở L22 (k = 5) | 4 bit: odds 0,93 × FP; \|cos\| chéo FP–Q 0,953 (trong FP 0,976, trong Q 0,977) · 3 bit: 0,85 ×; chéo 0,865 (trong Q 0,989) · 2 bit α0,5: 0,49 ×; chéo 0,767. Ở cả 3 mức, mọi \|cos\| chéo < mọi \|cos\| trong FP [ĐCM ở ô này] |
| Tách đoạn ở L22 | 4 bit: pre (L0–22) T 0,94, post (L23) 0,97, all 0,92. 3 bit: pre 0,74, post 0,95, all 0,69. **Suy biến, không dùng** (D-11) |
| Sàn step0 (L22/vùng 5) | 0,39 = 5,3% odds FP |
| Thời gian | 6,41 s/ô → 3.000 lần ≈ 5,3 giờ; 10.000 lần ≈ 17,8 giờ GPU cho 410M |

**T và mức co biên độ** (R = logit diff Q / FP; c = độ dốc hồi quy từng câu; KTC 95% bootstrap cụm):

| Cấu hình | R [KTC] | c [KTC] | T ở L22 | T trung vị vùng 5 | T(L22) / R | T trung vị vùng 5 / R |
|---|---|---|---|---|---|---|
| 8 bit | 0,99 [0,99; 0,99] | 0,99 [0,99; 1,00] | 0,99 | 0,99 | 1,00 | 1,00 |
| 4 bit | 0,95 [0,93; 0,98] | 0,88 [0,80; 0,97] | 0,92 | 0,95 | 0,96 | 1,00 |
| 3 bit α0,5 | 0,92 [0,88; 0,96] | 0,92 [0,75; 1,10] | 0,89 | 0,90 | 0,97 | 0,98 |
| 3 bit α0,75 | 0,83 [0,79; 0,88] | 0,85 [0,60; 1,11] | 0,80 | 0,81 | 0,96 | 0,97 |
| 3 bit | 0,75 [0,68; 0,80] | 0,77 [0,45; 1,10] | 0,69 | 0,70 | 0,93 | 0,94 |
| 2 bit α0,25 | 0,56 [0,51; 0,60] | 0,82 [0,68; 0,96] | 0,60 | 0,85 | 1,07 | 1,52 |
| 2 bit α0,5 | 0,19 [0,14; 0,24] | 0,55 [0,32; 0,82] | 0,22 | 0,38 | 1,19 | 2,00 |

Tương quan qua 9 cấu hình: R với T trung vị theo ô 0,997; R với T ở L22 0,996.

**Ghi chú G0b:**
- **Co biên độ chi phối T** [ĐCM cho tác vụ này]: ở họ 3–4 bit, T/R ≈ 0,93–1,00, tức không gian con DAS vẫn điều khiển gần như cùng tỉ lệ của biên quyết định. Cơ sở của D-12.
- **Họ 2 bit khác họ 3–4 bit** [GỢI Ý]: ở 2 bit α0,25 và α0,5, T trung vị vùng 5 cao hơn hẳn R (0,85 so với 0,56; 0,38 so với 0,19), cao nhất ở L13–L18 (0,86–0,88; 0,42–0,45), còn ở L22 thì T ≈ R (0,60; 0,22). Hành vi hỏng nhanh hơn khả năng điều khiển của hướng ở layer giữa. Hợp với nhận định của Zhou et al. rằng 2 bit hỏng kiểu khác 4 bit. Chỉ 1 tác vụ, 1 seed mỗi ô, và các mức α là cấu hình nội suy.
- **DAS vượt trần tráo trung thực** [ĐCM]: ở FP, 2 × logit diff = 6,59, nhưng odds L22 = 7,33 và L23 = 8,70. Ở L0/vùng 1 odds 6,62 ≈ trần. Hợp với Tanyel & Ayvaz (phần vượt do hàm mục tiêu). G1 đo vanilla để so.
- **T không đều theo ô** [GỢI Ý, 1 seed/ô]: vùng 5 ở 4 bit: L13–L16 ≈ 0,96, L19–L21 ≈ 0,85. Vùng 2 ở 3 bit: L3–L12 0,66–0,79, L13–L21 0,23–0,48. Vùng 1 đều (≈ 0,71–0,81 ở 3 bit).
- **Sai số tương đối của trọng số không đủ để dự báo** [GỢI Ý]: 2 bit α0,25 (0,122) làm hỏng hành vi hơn 3 bit α0,75 (0,158).
- **Học lại phục hồi nhiều hơn dùng lại** (3 bit: 0,85 so với 0,69; 2 bit α0,5: 0,49 so với 0,22), và hướng học lại lệch khỏi hướng FP vượt dao động seed. Chưa gọi là "mã hoá lại": chưa có tác vụ đối chứng, chưa có biên tương đương (D-05), và ô sát đầu ra.
- Các dấu hiệu dừng đặt trước (FP accuracy < 0,7; odds FP ≈ 0 ở mọi ô; 8 bit tụt mạnh) đều không xảy ra.

## Changelog
- v0.4 (13/11/2026, Claude): G0 đạt; §4 thêm bảng áp quy tắc G0b và tiêu chí G1 định lượng; §9 điền kết quả G0b, bảng co biên độ, sửa bảng run (mỗi job một dòng); §6 sửa dòng G0b (0,51 giờ), thêm tổng; thêm D-11 (bỏ ô chính, đo theo layer), D-12 (chuẩn hoá T theo R), D-13 (thiết kế G1, chờ xác nhận), D-14 (Claude tự cập nhật sổ); §8 thêm 7 nguồn (Tanyel & Ayvaz, Wu et al., Yao et al., Bhandari & Wade, dataset HF, quant-lens, checkpoint Xu-Ouyang), cập nhật Zhou và Boguraev, ghi 2 nguồn chưa xác minh; repo gốc thêm điểm 9–12, sửa điểm 6; §7 thêm câu hỏi 6; §5 cập nhật việc.
- v0.3 (12/11/2026): điền §9 kết quả G0 full; áp 4 quy tắc G0 (§4: G0 một phần); thêm D-08, D-09, D-10; §6 dòng GPU đầu tiên; §8 thêm repo gốc và 8 điểm đối chiếu; §5 cập nhật việc cần làm.
- v0.2 (12/11/2026): thêm D-07; thay script `g0_pilot.py` bằng notebook `00_g0_pilot.ipynb` chạy qua `configs/kaggle_run.yaml`; §9 thêm bảng run.
- v0.1 (12/11/2026): tạo sổ; ghi D-01 đến D-06; cổng G-N…G3; quy tắc G0; sổ nguồn; hướng dẫn chạy G0.
