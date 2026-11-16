# KHOALUAN_KE_HOACH_THEO_DOI.md — Sổ dự án khoá luận

> Version: v0.7 · Ngày: 16/11/2026 · Nguồn sự thật của project. Đề xuất chi tiết: `DEXUAT_HUONG_B1_DAS.md` v0.6. Quy trình: `QUY_TRINH_LAM_VIEC.md` (bản 13/11 lần 2). Việc trước mắt: `VIEC_CAN_LAM.md` bản 16/11 (đã gộp `HUONG_DAN_VIEC_14_18_11.md`; file đó không còn dùng).
> Quy ước: [ĐCM] đã kiểm chứng · [GỢI Ý] bằng chứng chưa đủ · [PHỎNG ĐOÁN] chưa kiểm.
> Từ v0.4, Claude tự cập nhật sổ từ file kết quả người dùng gửi (D-14, QT-44). Mọi số của G0b tái tạo được bằng `notebooks/00b_phan_tich_g0b.ipynb` (QT-32). Số về repo gốc ở §8 tái tạo được bằng `notebooks/98_kiem_repo_goc.ipynb`. Mọi số G1 (§4, §10) tái tạo được bằng `notebooks/01b_phan_tich_g1.ipynb` từ `results/20261113_0846_g1/`.

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
| Tác vụ | 4 tác vụ (D-13, đã xác nhận; G1 chạy 13/11): `agr_sv_num_subj-relc` (tác vụ phát triển, đã nhìn dữ liệu ở G0), `npi_any_subj-relc`, `filler_gap_subj`, `cleft` |

## 2. Trạng thái hiện tại (16/11/2026)

- **G1 đạt (16/11)** cho cả 410M và 1B, theo đúng 3 tiêu chí D-13 đặt trước khi chạy. Run `20261113_0846_g1`, commit `d755410`, 3 job `ok`, 5,06 giờ GPU. Claude tính lại độc lập từ `results.jsonl` (notebook 01b): trùng `g1_check.json` của notebook 01. Bảng áp tiêu chí ở §4, chi tiết ở §10.
- Ở 2 tác vụ không có cặp lệch vị trí (`npi_any_subj-relc`, `filler_gap_subj`), 6 phương pháp tất định (probe × 2, mean, PCA, k-means, vanilla) khớp bảng của bài tới 2 chữ số thập phân, cả odds lẫn selectivity, ở cả hai model [ĐCM]. Chênh lệch lớn dồn vào 2 tác vụ có cặp lệch vị trí (`agr_sv_num_subj-relc`, `cleft`), chủ yếu ở mean, PCA, k-means [ĐCM]. Giải thích bằng lỗi vị trí của repo gốc (§8 điểm 9) mới là [GỢI Ý]; kiểm bằng G1r theo quy tắc D-16 (đặt 16/11, trước khi chạy).
- G0 đạt (13/11). D-11, D-12, D-15 chờ SPEC C1.
- Đang làm (theo `VIEC_CAN_LAM.md` 16/11): đưa file vào repo (gồm file phiên 13/11 lần 3, chưa push); G1r (khoảng 1,5 giờ GPU); phiếu kiểm repo gốc và notebook 98 (TV-B); G-N bằng notebook 96 (hạn 17/11); tải PDF Tanyel & Ayvaz, Makarov; notebook 97 (GPT-QModel trên Kaggle). Sau đó Claude viết SPEC C1/C2 và notebook 02.
- Người dùng nhắc "lời duyệt của GVHD" ở phiên 16/11 nhưng nội dung chưa có trong phiên; chờ dán vào chat để ghi `NHAN_XET_GVHD.md`.

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
| D-13 | 13/11/2026 | **Đã xác nhận: nhóm chạy G1 13/11; G1 đạt 16/11 (§4, §10).** Tái lập G1: (i) 4 tác vụ `agr_sv_num_subj-relc`, `npi_any_subj-relc`, `filler_gap_subj`, `cleft`; Pythia 410M và 1B, fp32. (ii) Eval trên split `test` của HF, là tập seed 1 mà repo gốc dùng. (iii) Đủ 9 phương pháp của bài: DAS, probe × 2, diff-in-means, PCA, k-means, LDA, ngẫu nhiên, vanilla; thêm tác vụ đối chứng dog-give. (iv) Lấy biểu diễn source ở vị trí của source, không theo lỗi đảo vị trí của repo gốc (§8 điểm 9); `POS_MODE = "repo"` để so khi cần. (v) Tiêu chí G1 định lượng ở §4. **Ghi chú 13/11 lần 2 (Claude):** (a) lỗi điểm 9 chỉ chạm `agr_sv_num_subj-relc` (16% cặp eval) và `cleft` (8%), nên `POS_MODE` chỉ có thể làm khác 2 tác vụ này; (b) ở `cleft`, 50% câu eval có trong train vì loại pseudo-cleft chỉ có 29 câu khác nhau (§8 điểm F). Bài gốc cũng vậy nên vẫn tái lập được; nhóm quyết định giữ `cleft` (báo cáo kèm) hay đổi tác vụ khi xác nhận D-13 | 4 họ hiện tượng khác nhau; gồm 2 tác vụ nghiên cứu trường hợp của bài (§6: `npi_any_subj-relc`, `filler_gap_subj`). Accuracy trong bài ≥ 0,89 ở cả 410m và 1b, nên còn chỗ cho nén làm hỏng. `agr_sv_num_subj-relc` đã dùng ở G0 nên là tác vụ phát triển; 3 tác vụ còn lại chưa nhìn dữ liệu. Tiêu chí G1 trong v0.3 chỉ định tính ("đúng thứ tự", "cùng bậc") |
| D-14 | 13/11/2026 | Claude tự cập nhật sổ, nhật ký GPU, bảng run, trạng thái cổng, đề xuất từ file kết quả người dùng gửi; người dùng không phải điền số. Kết quả run được Claude đưa vào zip trả về. Quy trình: QT-13, QT-30, QT-31, QT-32, QT-41, QT-42, QT-44 | Người dùng yêu cầu; điền tay mất thời gian và dễ sai (dòng G0b trong v0.3 ghi "0.5" và gộp hai job vào một ô) |
| D-15 | 13/11/2026 | **Đề xuất, chờ kết quả notebook 97 trên Kaggle; chốt trong SPEC C1.** Đường GPTQ cho C1: (i) GPT-QModel ghim **7.6.0** (bản ≥ 7.7.0 đòi torch ≥ 2.14.1); (ii) đặt rõ `sym=False` (khớp RTN G0b), `act_group_aware=False`, `desc_act=False`, `damp_percent=0,05`, g = 128; (iii) `offload_to_disk=False`; (iv) lấy Q(W) bằng `dequantize_weight()` từng module rồi đổi fp32, không dùng `dequantize_model()`; (v) chạy lượng tử hoá ở job riêng, lưu Q(W) hoặc Q(W) − W, notebook phân tích chỉ nạp lại, để tránh xung đột thư viện. Phương án dự phòng: tự cài GPTQ ở fp32 và đối chiếu với GPT-QModel trên Pythia-70M | Claude chạy GPT-QModel 7.6.0 trên CPU (model ngẫu nhiên cỡ Pythia-70M, transformers 5.22.2): chạy được; nhưng (1) transformers 5.22.2 đặt tên đầu ra `lm_head`, GPT-QModel gọi `embed_out`, `save()` lỗi khi bật offload; (2) mặc định `sym=True` và bật `act_group_aware`, khác GPTQ chuẩn và khác RTN của nhóm; (3) `dequantize_model()` ép trọng số về float16, `scales` lưu bfloat16 trên CPU; (4) bản 7.6.0 ghim numpy 2.2.6 [ĐCM trên CPU] |
| D-16 | 16/11/2026 | **Đặt trước khi chạy G1r.** Chạy lại G1 ở `POS_MODE = "repo"` cho `agr_sv_num_subj-relc` và `cleft`, 410M và 1B; mọi thứ khác giống G1 (`configs/kaggle_run.yaml` bản 16/11). Kiểm 12 ô {mean, PCA, k-means} × 2 tác vụ × 2 model; ở G1 (`correct`) có 2/12 ô có tỉ lệ mình/bài trong [0,5; 2]. Ở G1r: **≥ 10/12** ô trong [0,5; 2] → *Xác nhận* lệch do lỗi vị trí; **7–9** → *Giải thích một phần*; **≤ 6** → *Không giải thích được*; thiếu ô → *Chưa đủ dữ liệu*. In thêm (không dùng để kết luận): số ô trong [0,9; 1,1], tỉ lệ của DAS, vanilla, probe, LDA. Kết quả chính của RQ0 vẫn theo `correct` (D-13 iv); G1r là bản "theo code gốc" (§7 câu 6). Notebook 01b áp quy tắc này | Ở 2 tác vụ 0% cặp lệch, phương pháp tất định khớp bài tới 2 chữ số, nên pipeline của nhóm trùng pipeline của bài ở mọi chỗ trừ vị trí; lệch lớn chỉ ở 2 tác vụ có cặp lệch, và ở các phương pháp học từ biểu diễn base do đơn vị Collect gom (điểm 9). Nếu giả thuyết đúng, chế độ `repo` phải đưa các ô này về gần 1. Chi phí khoảng 1,5 giờ GPU. Lợi ích: (1) biến giải thích [GỢI Ý] thành kết luận có kiểm cho chương tái lập; (2) lượng hoá ảnh hưởng của lỗi lên số baseline đã công bố. Tanyel & Ayvaz (Phụ lục E.1) nêu lỗi này; có lượng hoá hay không thì chưa rõ vì chưa đọc toàn văn |

## 4. Cổng quyết định

| Cổng | Hạn | Điều kiện đạt | Trạng thái | Nếu không đạt |
|---|---|---|---|---|
| G-N tính mới | 17/11/2026 | Danh sách bài trích dẫn của CausalGym, Ouyang, Duan, Makarov, Tanyel & Ayvaz, Geiger et al. (DAS), Zhou et al. (+ 4 bài lân cận) từ Semantic Scholar và OpenAlex, cùng 17 truy vấn từ khoá (S2, OpenAlex, arXiv), lấy bằng `notebooks/96_gn_tra_cuu_api.ipynb`; Claude đọc mọi bài và xếp loại; không ai đã làm C1/C2/C3b (định nghĩa "trùng" ở `GN_TRA_CUU.md` §1). **Đổi 13/11 lần 3, trước khi có dữ liệu:** bỏ Google Scholar (không có API, không tự động được); giới hạn ghi ở `GN_TRA_CUU.md` §4 | Đang làm. Đã thêm 4 bài lân cận (§8): Tanyel & Ayvaz, Wu et al., Yao et al., Bhandari & Wade. 13/11 lần 2: Claude tra web 7 nhóm truy vấn, thêm 5 bài lân cận, chưa thấy bài nào đo DAS/DII dưới lượng tử hoá trên CausalGym [GỢI Ý]. Chờ zip notebook 96 | Bỏ hoặc đổi đóng góp bị trùng |
| G0 chạy được | 22/11/2026 | Chạy hết `notebooks/00_g0_pilot.ipynb` trên 410M; có t; có vùng chuyển tiếp; có sàn step0; đo t cho 1B | **Đạt (13/11/2026).** Xem bảng áp quy tắc ở G0b dưới đây | — |
| G1 tái lập | 31/12/2026 (có thể dời 15/01/2027) | Tiêu chí D-13, xét riêng cho từng model (410M, 1B), đạt cả ba:<br>(1) **Thứ tự phương pháp:** Kendall τ_b ≥ 0,7 giữa odds trung bình 4 tác vụ của mình và của bài gốc (9 phương pháp), và DAS đứng đầu.<br>(2) **Thứ tự vị trí** (tiêu chí tối thiểu): layer xuất hiện của vùng khác nhau đầu tiên ≤ layer xuất hiện của vùng cuối ở ≥ 3/4 tác vụ. Layer xuất hiện = layer đầu tiên có odds DAS ≥ 0,5 × max của vùng đó.<br>(3) **Cùng bậc:** ≥ 12/16 cặp (tác vụ × {DAS, probe tốt hơn, diff-in-means, vanilla}) có tỉ lệ mình/bài gốc trong [0,5; 2].<br>Kiểm tra phụ: accuracy tác vụ lệch ≤ 0,05 | **Đạt (16/11/2026)** cho cả hai model; bảng áp tiêu chí ngay dưới bảng G0b. Điều kiện để tin kết quả còn treo: phiếu kiểm của TV-B (điểm 9, 10); nếu một trong hai ra "Khác" thì mở lại cổng | Dừng phát triển; sửa pipeline; chạy `POS_MODE = "repo"` để xem lệch có do lỗi vị trí của repo gốc không (chỉ có thể ở `agr_sv_num_subj-relc` và `cleft`); hỏi tác giả |
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

**Kết quả áp tiêu chí G1** (16/11/2026; run `20261113_0846_g1`; split test; `POS_MODE = "correct"`; tính lại bằng `notebooks/01b_phan_tich_g1.ipynb`, trùng `g1_check.json`):

| Tiêu chí | 410M | 1B | Kết luận |
|---|---|---|---|
| (1) Kendall τ_b (9 phương pháp, trung bình 4 tác vụ); DAS đứng đầu | τ_b = 1,00; có (DAS 9,86, bài 10,01) | τ_b = 1,00; có (DAS 11,03, bài 11,13) | Đạt |
| (2) Layer xuất hiện: vùng khác nhau đầu ≤ vùng cuối | 4/4 (vùng đầu L0 ở cả 4; vùng cuối L17, L13, L15, L6) | 4/4 (vùng đầu L0; vùng cuối L13, L9, L12, L3) | Đạt |
| (3) Cặp có tỉ lệ mình/bài trong [0,5; 2] | 15/16 (ngoài: `cleft` × mean, 3,08) | 15/16 (ngoài: `cleft` × mean, 3,57) | Đạt |
| Kiểm phụ: accuracy lệch ≤ 0,05 | 0,00 ở cả 4 tác vụ | 0,00 ở cả 4 tác vụ | Đạt |

**Kết luận G1:** đạt cho cả hai model. Tỉ lệ DAS mình/bài: 410M 0,92–1,12; 1B 0,93–1,06 (1 seed).

## 5. Việc cần làm

- [x] (TV-A, 12/11) Thiết lập repo và Kaggle runner; G0 full 410M + đo thời gian 1B
- [x] (TV-A, 13/11) Lưu kết quả G0 full vào `results/` (làm trước commit `b22a2a4`)
- [x] (Cả hai, 13/11) Xác nhận D-08; chạy G0b
- [x] (Claude, 13/11) Phân tích G0b; chốt G0; viết notebook 01 và 00b; cập nhật đề xuất v0.6, sổ v0.4, quy trình
- [x] (Claude, 13/11 lần 2) Phiếu kiểm repo gốc + notebook 98 (chạy CPU); tra G-N bằng web; ghi chú Zhou, Tanyel & Ayvaz, Makarov (`GHI_CHU_BAI_BAO.md`); chạy thử GPT-QModel trên CPU + notebook 97; sổ v0.5
- [x] (Cả hai, 13/11) Chạy G1; run `20261113_0846_g1`, 3 job `ok`
- [x] (Claude, 16/11) Phân tích G1, áp tiêu chí §4 (đạt cả hai model); notebook 01b; đặt D-16; sổ v0.7; gộp `HUONG_DAN_VIEC_14_18_11.md` vào `VIEC_CAN_LAM.md`
- [ ] (TV-A, 16/11) Giải nén zip phiên 16/11 vào repo (đã gồm file phiên 13/11 lần 3 và kết quả G1), commit, push (`VIEC_CAN_LAM.md` Bước 1)
- [ ] (TV-A, 16/11) Chạy G1r bằng Save Version (khoảng 1,5 giờ GPU), mang zip về
- [ ] (Claude, khi có zip G1r) Áp D-16; cập nhật §10 và §8 điểm 9
- [ ] (TV-B, 16/11) Điền `PHIEU_KIEM_REPO_GOC.md` (17 điểm), rồi chạy notebook 98 có so HF
- [ ] (Một người, 17/11) Chạy notebook 96 (CPU, có Internet), mang `96_gn_tra_cuu.zip` về
- [ ] (Claude, khi có zip) Đọc mọi bài, xếp loại, điền bảng G-N, cập nhật §4 và §8
- [ ] (TV-A, 18/11) Tải PDF Tanyel & Ayvaz (2611.05033), Makarov (2610.40055) lên Project; Zhou et al. đúng bài (`2026.findings-acl.1162`) đã có trong Project từ 14/11. Claude đọc toàn văn ở phiên sau, TV-A kiểm lại vài số
- [ ] (TV-A, 18/11) Chạy notebook 97 trên Kaggle T4 (từng ô), mang `kiem_gptqmodel.jsonl` về; chốt D-15
- [ ] (Claude, sau notebook 97 và PDF Makarov) SPEC C1/C2 (chốt D-11, D-12, D-15, biên tương đương, ngưỡng R; cách dùng `cleft` trong C1, §10 ghi chú 4; ngân sách GPU tính lại theo thời gian G1) và notebook 02
- [ ] (TV-A, 23–30/11) Đề cương theo mẫu FIT; gửi thầy kèm các câu hỏi ở §7
- [ ] (TV-A dán nhận xét/lời duyệt vào chat; Claude viết file) Nhận xét lần 3 và lời duyệt của thầy vào `NHAN_XET_GVHD.md`; đóng sổ đề tài cũ lên v1.4
- [ ] (Tuỳ chọn) Sửa ô Instructions của Project: "sổ dự án v0.7", "Tự cập nhật sổ dự án (QT-44)"

## 6. Nhật ký GPU

Kaggle tính quota theo thời gian phiên. Số phút lấy từ `run_summary.json` (chỉ tính thời gian job, chưa tính khởi động phiên). Claude ghi bảng này (QT-13).

| Ngày | Tài khoản | Việc | Model | Giờ GPU | Ghi chú |
|---|---|---|---|---|---|
| 12/11/2026 | TV-A | `20261112_1441_g0_full` (G0 full + timing 1B) | 410M, 1B | 0,09 | 2 job: 4,2 + 1,3 phút |
| 13/11/2026 | TV-B | `20261113_0506_g0b` (G0b) | 410M | 0,51 | 2 job: 1,7 + 28,7 phút |
| 13/11/2026 | TV-B (mặc định theo QT-13: người dùng không báo khác lần trước) | `20261113_0846_g1` (G1) | 410M, 1B | 5,06 | 3 job: 1,9 + 129,1 + 172,6 phút. Dự kiến 6,5–7 giờ |

Tổng đã dùng: 5,66 giờ. G1r dự kiến khoảng 1,5 giờ (suy từ phút từng tác vụ của G1). Notebook 97 dự kiến khoảng 0,25 giờ [PHỎNG ĐOÁN]. Các phiên của Claude chỉ dùng CPU.

## 7. Câu hỏi gửi GVHD

1. CausalGym có đạt yêu cầu "bài báo gốc" không?
2. MVP (tái lập + C1 + C2 cấp biến + C3b; C3 và C4 là Target) có hợp lý không?
3. Kết quả "cơ chế được bảo toàn" có được tính là kết quả nếu quy tắc đã đăng ký trước không?
4. Có được dùng checkpoint GPTQ công khai của Ouyang et al. (Pythia deduped) không?
5. Hạn đề cương chính thức là ngày nào?
6. Code gốc của CausalGym lấy biểu diễn source ở vị trí của base (§8 điểm 9). Nhóm tái lập theo đúng công thức của bài (G1 đạt 16/11) và chạy kèm bản theo code gốc cho 2 tác vụ bị ảnh hưởng (G1r, D-16). Báo cáo cả hai trong chương tái lập có được không?

## 8. Sổ nguồn

| Nguồn | Trạng thái | Ghi chú |
|---|---|---|
| CausalGym, ACL 2024 (arXiv 2402.12560) | [ĐCM] đọc toàn văn | Pythia-1B: DAS 10.74, probe 3.66; selectivity 6.9B: DAS 2.48 < probe 3.79; checkpoint 1K/2K/3K/10K. Số theo tác vụ: Table 11 (410m), Table 13 (1b). Phụ lục B: ≤ 410m chạy fp32, 1b bfloat16; train 200 cặp, nhân đôi thành 400 bằng cặp đảo; eval 50 cặp + cặp đảo, "không trùng train". **16/11:** Table 11–14 (odds và selectivity, 410m và 1b) đối chiếu với PDF cho 4 tác vụ G1; số trong notebook 01 và 01b khớp [ĐCM] |
| Repo gốc `aryamanarora/causalgym`, commit `0f3129f` (30/11/2024) | [ĐCM] Claude đọc code 12/11 và 13/11/2026 (clone lại 13/11 hai lần); điểm 8, 9, 10 kiểm thêm bằng chạy code (notebook 98); **TV-B kiểm lại độc lập** theo `PHIEU_KIEM_REPO_GOC.md` | 12 điểm + 5 điểm mới (A–E) + điểm F, bảng dưới |
| Dataset HF `aryaman/causalgym` | [ĐCM] trang HF | 3 split: train 11,6k, validation 2,9k, test 2,9k dòng; README: "exactly as used in the experiments in the paper"; file gốc `train.json`, `dev.json`, `test.json`. So từng dòng với tập sinh lại: chờ TV-B (notebook 98, ô 3) |
| pyvene 0.1.6 (PyPI, phiên bản repo gốc ghim) | [ĐCM] Claude đọc mã gói 13/11 | `unit_locations["sources->base"]` = (vị trí ở source, vị trí ở base): `pyvene/models/intervenable_base.py` dòng 1669–1670 (cũng 911–912). Đòi `transformers>=4.45.1`, không giới hạn trên |
| GPT-QModel (PyPI; GitHub `ModelCloud/GPTQModel`, HEAD `0450476` ngày 13/11/2026) | [ĐCM] PyPI + mã nguồn + chạy CPU | Có định nghĩa `gpt_neox` (`lm_head = "embed_out"`). 7.7.0–7.10.0 đòi torch ≥ 2.14.1, transformers ≥ 5.20.2; 7.6.0 đòi torch ≥ 2.8.0, transformers ≥ 5.14.0, numpy 2.2.6; chỉ có sdist. Mặc định GPTQ: `sym=True`, `act_group_aware` bật, `damp_percent` 0,05. `dequantize_model()` ép float16. Chi tiết D-15 |
| Ouyang et al., ACL 2025 (arXiv 2411.17691) | [ĐCM] trang ACL + arXiv | Checkpoint GPTQ trên HF `Xu-Ouyang`, dạng `pythia-<cỡ>-deduped-int{2,3,4,8}-step<k>-GPTQ-wikitext2` [ĐCM trang HF]. Là Pythia **deduped**: nếu dùng phải chạy cả FP deduped |
| Zhou et al., Findings ACL 2026 (2026.findings-acl.1162; arXiv 2604.19884) | [ĐCM] trang ACL + arXiv; PDF ACL đọc qua công cụ trích 13/11 (số phải đối chiếu PDF); PDF đúng bài có trong Project từ 14/11, chưa đối chiếu lại | "From Signal Degradation to Computation Collapse: Uncovering the Two Failure Modes of LLM Quantization", tr. 23204–23222. Llama-3.1-8B (chính), Qwen3-8B, Mistral-7B, Gemma-2-9B; GPTQ (GPTQModel, g = 128, hiệu chỉnh C4 128 × 2048), AWQ để kiểm; ParaRel. 4 bit: tín hiệu yếu đi, mẫu tính toán còn, patch FP phục hồi được; 2 bit: thành phần then chốt hỏng, tín hiệu mất từ layer sớm. Domino 2 bit (Bảng 2), sửa 4 bit (Bảng 1), MMLU/GSM8K (Bảng 6): xem `GHI_CHU_BAI_BAO.md` §1. File `2026.findings-acl.642` nhóm tải là bài khác |
| Tanyel & Ayvaz, arXiv 2611.05033 (3/11/2026) | [ĐCM] trang tóm tắt arXiv + đoạn HTML qua tìm kiếm; **chưa đọc toàn văn** (trang HTML giới hạn truy cập cả 13/11 lần 1 và lần 2) | "Whose Effect Is It? How Objectives Inflate Learned Subspace Interventions". Trên CausalGym, điểm DAS trung vị gấp 2–3 lần patch cả trạng thái; trong bản đồ dựng lại, DAS > vanilla ở mọi bản đồ, trung vị gấp 2,04 (tứ phân vị 1,46–2,71); đổi hàm mục tiêu thì phần vượt mất phần lớn. Phụ lục E.1: code CausalGym truyền vị trí base/source đảo thứ tự (Hình 13) (điểm 9). Dựng lại với lr hằng (CausalGym có lịch). Bảng §7.1 chưa rõ nghĩa. Chi tiết "chứng minh Lean" do Gemini nêu: chưa kiểm |
| Wu, Dhiman, Koshiyama, arXiv 2608.06564 (8/2026) | [ĐCM] trang tóm tắt | "Which Decisions Low-Bit Quantization Breaks, and How to Predict Them". 16 model, RTN/AWQ/GPTQ/GGUF, 8 xuống 2 bit: biên quyết định bị **nhân** với hệ số co (trung vị 0,86 ở 4 bit, 0,33 ở 3 bit, 0,00 ở 2 bit), gọi là *margin shrinkage*. Cơ sở cho D-12. Câu trích §6.1 do Gemini nêu: chưa kiểm |
| Yao, Boguraev, Pimentel, Mahowald, EMNLP 2026 (arXiv 2610.33299) | [ĐCM] trang arXiv + ACL Anthology | "The Emergence and Sparsification of a Syntactic Circuit". Mạch subject–verb agreement trên pythia-1b và 10 seed pythia-410m qua checkpoint: học sớm, ban đầu phân tán; sau khi hành vi ổn định, mạch vẫn tổ chức lại và thu nhỏ; mạch cuối của 1b rất thưa. Tiên nghiệm cho C3b. Chi tiết "18 neuron + 1 head" do Gemini nêu: chưa kiểm |
| Bhandari & Wade, arXiv 2609.06473 (9/2026) | [ĐCM] trang tóm tắt | "Steering Under Compression: Dose-Response, Capability Cost, and Failure Asymmetry in Quantized LLMs". INT8/NF4, 4 model 7–9B; quy tắc ba nhãn đặt trước; INT8 pooled −0,010 (KTC 90% [−0,026; +0,007]) "Equivalent", NF4 "Inconclusive"; cos vector steering với FP16: 0,989–0,998 (INT8), 0,945–0,990 (NF4). Mẫu cho D-05 |
| Duan, arXiv 2606.03002 | [ĐCM] trang arXiv | "Perplexity Can Miss SAE Feature Damage Under Quantization". SAE + RTN, Pythia-70M, Gemma-2-2B; INT6: 62,4% feature sống (Pythia-70M), 51,3% (Gemma-2-2B); dự báo sống AUC 0,92 / 0,97 |
| Makarov, arXiv 2610.40055 (29/10/2026) | [ĐCM] trang tóm tắt + đoạn HTML (13/11 lần 2); PDF đọc ở phiên trước nhưng chưa có trong Project | "One Vector or Many? Clustered Optimal-Transport Steering under Quantization". Gemma-2-2B, Granite-3.1-2B, độc tính; INT8/NF4. Tương đương = TOST dạng khoảng: KTC bootstrap ghép cặp 90% của **tỉ số trung bình** nằm trong biên cố định trước; 8 phép kiểm đều phải đạt nên không hiệu chỉnh đa phép kiểm. Chuyển từ FP sang NF4 thay vì học lại không tăng độc tính có ý nghĩa sau hiệu chỉnh. **Giá trị biên chưa thấy** |
| Faumi & Sumanathilaka, arXiv 2610.37157 | [ĐCM] PDF | GPT-2 và DistilGPT-2; IOI sụp, Greater-Than được ánh xạ lại |
| Grant et al., ICLR 2026 Oral (arXiv 2511.04638) | [ĐCM] trang ICLR + slide | EMD đo độ lệch can thiệp |
| Kumon & Yanaka, ACL 2026 | [ĐCM] trang ACL | DAS dễ overfit; dùng activation patching |
| Sutter et al., NeurIPS 2025 | [ĐCM] trang arXiv | IIA cao cả trên model ngẫu nhiên |
| Catalan-Tatjer et al., ICLR 2026 (arXiv 2510.06213) | [ĐCM] trang | Động lực learning rate quyết định độ bền PTQ |
| Armstrong, arXiv 2604.15167 | [ĐCM] trang arXiv | Pythia-160m, 154 checkpoint, khoảng cách INT4 tăng 11% → 517% |
| Chang et al., EMNLP 2025 | [ĐCM] trang ACL | Cross-model activation patching; độ lớn residual dự báo lỗi. Có thể là arXiv 2506.12044 (repo `terarachang/QError`): chưa đối chiếu |
| Chen et al., arXiv 2609.11716 | [ĐCM] trang arXiv | Lỗi mới triệt tiêu lỗi kế thừa |
| CircuitKIT, arXiv 2607.19317 | [ĐCM] trang arXiv | Lý do bỏ C5 |
| Boguraev et al., arXiv 2608.28924 | [ĐCM] tiêu đề | "Causal Interventions Reveal Typologically Organized Syntactic Mechanisms in Multilingual Language Models" (Boguraev và 3 tác giả). DII/DAS đa ngữ, không về nén. Danh sách đồng tác giả chưa kiểm hết |
| Nwaiwu, Jongsawat, Tungkasthan, arXiv 2512.13725 | [ĐCM] trang arXiv | Lượng tử hoá (BF16/INT8/NF4) và lập luận nhân quả trên CLadder, Llama-3-8B. Đo hành vi; không trùng |
| Wang et al., arXiv 2510.23264 (PAHQ) | [ĐCM] trang arXiv | Lượng tử hoá hỗn hợp để tăng tốc tìm mạch ACDC. Không trùng |
| arXiv 2606.06267 (UKPLab) | [ĐCM] trang arXiv | 75 mạch trên Pythia 70M–1.4B, nhiều mạch khác cấu trúc cùng một phép tính. Không về nén; cảnh báo "cơ chế không duy nhất" |
| Repo `iamartyaa/quant-lens` | [ĐCM] Claude clone 13/11/2026 | Có tồn tại. SAE + TransformerLens/SAELens trên GPT-2 small (Gemma 2 2B dự định); không dùng Pythia, CausalGym hay DAS. Không trùng |
| Tokenizer GPT-NeoX-20B, bản sao `BlinkDL/RWKV-LM` (`RWKV-v4/20B_tokenizer.json`, sha256 `56ac4821…`) | [GỢI Ý] cùng tokenizer với Pythia | Claude dùng để chạy notebook 98 vì không vào được HF. TV-B chạy lại bằng tokenizer HF `EleutherAI/pythia-70m` |
| Wilam, arXiv 2611.09204 | [CHƯA XÁC MINH] | Gemini nêu ("representational drift in a code model"); tìm không thấy |
| "Perturbation Ladder for SAE", Zenodo 22700831 | [CHƯA XÁC MINH] | Gemini nêu; chưa tìm |

**Repo gốc — các điểm đã đọc** (commit `0f3129f`; TV-B ghi "khớp" hoặc "khác" vào cột cuối; cách kiểm ở `PHIEU_KIEM_REPO_GOC.md`):

| # | Điểm | File:dòng | So với notebook của nhóm | TV-B |
|---|---|---|---|---|
| 1 | Odds = (log p_base(y_base) − log p_base(y_src)) + (log p_int(y_src) − log p_int(y_base)), dùng log-softmax | `eval.py:72` | Trùng: hiệu log-softmax bằng hiệu logit | |
| 2 | Loss khi học DAS = cross-entropy về nhãn src | `eval.py:10`, `train.py:75` | Trùng | |
| 3 | Template thêm `<\|endoftext\|>` ở đầu câu | `data.py:175` | G0b: `first_token_is_eos` = 1,0 [ĐCM] | |
| 4 | Mỗi batch gồm các cặp mẫu và cặp đảo của chúng | `data.py:335` | G0b: `eval_swap_frac` = 1,0; 100 cặp = 50 cụm [ĐCM] | |
| 5 | Chủ ngữ của base và src chọn độc lập; nhãn chọn độc lập trong {is, was, has} / {are, were, have} | `data.py:240`, `data.py:257` | Ví dụ G0b: base "are", src "has". Logit diff trộn số với thì; giữ nguyên để tái lập | |
| 6 | Loại trùng: chỉ kiểm câu **base** của cặp vừa lấy mẫu với tập train, rồi mới thêm cặp đảo, nên câu src (thành base của cặp đảo) có thể trùng train | `das.py:76–83`, `data.py:305`, `data.py:335` | G0b (validation): 2/100 câu eval có trong train. Split test (notebook 98, 13/11): `agr_sv_num_subj-relc` 4/100, `npi_any_subj-relc` 0, `filler_gap_subj` 0, `cleft` 50/100 (xem F) [ĐCM]. G1 (data_check, đếm câu khác nhau): 4/99, 0/100, 0/100, 21/70 [ĐCM]. Giữ nguyên để tái lập | |
| 7 | Bảng tổng hợp: max theo vị trí ở mỗi layer → trung bình qua layer → trung bình qua tác vụ; selectivity = odds − odds dog-give, lấy max riêng | `plot.py:322`, `plot.py:328–330` | Notebook 01 tính cả odds và selectivity đúng như vậy; notebook 00 chỉ có odds. G0b: 5,24 so với 4,97 của bài | |
| 8 | Token hoá cả câu, rồi căn vùng bằng token hoá từng vùng | `data.py:49`, `data.py:63` | Notebook nối token từng vùng. G0b: `tok_mismatch` = 0/500. Notebook 98 (split test, 4 tác vụ, 200 câu mỗi tác vụ): 0 câu lệch [ĐCM với tokenizer bản sao] | |
| 9 | **Vị trí can thiệp bị đảo:** `compute_pos` trả [vị trí src, vị trí base]; lời gọi pyvene dùng `pos_interv[1]` (vị trí base) làm vị trí lấy source, và đơn vị Collect (dữ liệu cho probe/mean/PCA) lấy base ở vị trí src. Chỉ có tác dụng khi base và src khác độ dài token | `data.py:138–140`, `train.py:58–62`, `eval.py:27–31` | Notebook 00/01 lấy source ở vị trí của source. Notebook 01 có `POS_MODE = "repo"` để tái hiện. Tanyel & Ayvaz (Phụ lục E.1) nêu cùng lỗi. **13/11 lần 2:** xác nhận bằng chạy (notebook 98 ô 6, pyvene 0.1.6, model ngẫu nhiên): logits của lời gọi gốc trùng chuẩn "đọc source ở vị trí base" (lệch 0,0), lệch chuẩn "vị trí src" 0,81; bản sửa ngược lại [ĐCM]. Tỉ lệ cặp eval (split test) bị lệch vị trí: `agr_sv_num_subj-relc` 16% (vùng 1–5), `cleft` 8% (vùng `{verb}`, ` was`), `npi_any_subj-relc` 0%, `filler_gap_subj` 0% [ĐCM với tokenizer bản sao]. **16/11 (G1):** `pos_mismatch_frac` của G1 (tokenizer HF thật) trùng các số này; ở 2 tác vụ 0% lệch, phương pháp tất định khớp bài tới 2 chữ số, lệch dồn vào 2 tác vụ còn lại (§10) [ĐCM]; quan hệ nhân quả kiểm bằng G1r (D-16) | |
| 10 | Tập eval của bài là seed 1 (`eval_seed = 1`); dataset HF xuất train seed 42, dev seed 420, test seed 1 | `das.py:82–83`, `data.py:390–398` | G0/G0b dùng split `validation` (dev). G1 dùng `test` (D-13). **13/11 lần 2:** sinh lại bằng hàm xuất HF và bằng `das.py` với tham số `test_all.py:24–31` (100 × 4 train, 25 × 4 eval) cho cùng 100 cặp ở cả 4 tác vụ [ĐCM]; mỗi tác vụ chỉ có 1 template nên lựa chọn template ngẫu nhiên ở `data.py:175` không gây lệch. So với file HF: chờ TV-B. **16/11 (G1):** trên split test, accuracy trùng bài ở cả 8 (model, tác vụ) và phương pháp tất định trùng tới 2 chữ số ở 2 tác vụ không lệch vị trí: bằng chứng gián tiếp mạnh rằng split test là tập eval của bài [ĐCM gián tiếp] | |
| 11 | dtype: 410m fp32, 1b bfloat16 | `utils.py:27–37` | Nhóm luôn fp32 (D-04); ghi khác biệt khi so 1b | |
| 12 | Probe: LogisticRegression saga, L2, có bias, C = 1e-4 và 1e-5 (410m), 1e-5 và 1e-6 (1b); dog-give gán " dog" cho `types[0]` = khoá đầu của `labels` trong template | `diff_methods.py:56–126`, `data.py:178`, `data.py:323–326` | Notebook 01 giống; thứ tự loại của 4 tác vụ ghi sẵn trong notebook | |
| A | Tập `discard` gồm mọi câu base trong `batch.pairs` của train, mà `pairs` đã gồm cặp đảo, nên chứa cả câu base và src của train. Câu base của cặp eval được kiểm với cả hai | `das.py:76–79`, `data.py:333–338` | Làm chính xác điểm 6; không đổi kết luận | |
| B | Điểm DAS trong bảng tổng hợp lấy ở bước eval cuối (bước 99 khi `steps = 100`); vanilla và phương pháp khác có `step = -1` | `plot.py:146–149`, `train.py:97–104` | So với notebook 01 | |
| C | Lịch học DAS: Adam, lr 5e-3, warmup tuyến tính 10% rồi giảm tuyến tính về 0; 1 lượt qua 100 batch × 4 | `train.py:18–38`, `test_all.py:24–42`, `test_all.py:80` | So với notebook 01 (Tanyel & Ayvaz dùng lr hằng) | |
| D | Bảng tổng hợp bỏ dòng NaN sau pivot, nên phương pháp thiếu lượt dog-give mất khỏi bảng, kể cả cột odds | `plot.py:316–331` | Lưu ý khi tự tổng hợp | |
| E | `test_all.py` mặc định bfloat16, `das.py` mặc định float16 cho model ngoài `WEIGHTS`; không ảnh hưởng 410m/1b | `test_all.py:56`, `das.py:62` | Chỉ xác nhận | |
| F | `cleft`: loại `pseudo-cleft` chỉ có 1 động từ ("did"), nên chỉ 29 câu khác nhau; train (400 câu) chứa hết. Mọi cặp lấy mẫu ở eval có base loại `normal`, 50/50 câu src có trong train; 50% câu eval có trong train. Không có cảnh báo "hết 20 lần thử" | `data/templates/syntaxgym.json` (mục `cleft`), `data.py:301–312` | Ghi chú D-13. Bài gốc cũng vậy [ĐCM bằng chạy code]. G1: 21/70 câu eval khác nhau có trong train, đều là câu pseudo-cleft (§10 ghi chú 4) | |

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

## 10. G1 — cách chạy và kết quả

**Cách chạy:**
- Notebook `notebooks/01_tai_lap_causalgym.ipynb` (commit `d755410`), `configs/kaggle_run.yaml` bản 13/11; T4, fp32, torch 2.11.0+cu130, transformers 5.20.2.
- Split test của HF (100 cặp = 50 cặp × 2 chiều), train 400; 9 phương pháp + tác vụ đối chứng dog-give; DAS 1 seed (SEED 0), lr 5e-3, bs 4, 1 lượt; `POS_MODE = "correct"`.
- Phân tích lại trên CPU: `notebooks/01b_phan_tich_g1.ipynb`; bản chạy của Claude ở `results/20261116_claude_cpu_nb01b/`.

**Run đã chạy:**

| run_id | Commit | Job | Trạng thái | Phút |
|---|---|---|---|---|
| 20261113_0846_g1 | d755410 | g1_smoke_410m | ok | 1,9 |
| 20261113_0846_g1 | d755410 | g1_410m | ok | 129,1 |
| 20261113_0846_g1 | d755410 | g1_1b | ok | 172,6 |

**Kiểm dữ liệu** (mọi tác vụ: `first_token_is_eos` 1,0; `eval_swap_frac` 1,0; nhãn nhiều token 0; `tok_mismatch` 0/1000; không có cảnh báo split hay thứ tự loại):

| Tác vụ | Vùng (khác nhau đầu → cuối) | Số ô 410M / 1B | Câu eval trùng train (câu khác nhau) | Cặp lệch vị trí | Accuracy 410M / 1B (bài) | Logit diff 410M / 1B |
|---|---|---|---|---|---|---|
| `agr_sv_num_subj-relc` | 1 → 5 | 116 / 76 | 4/99 | 16% | 0,97 / 1,00 (0,97 / 1,00) | 3,67 / 4,38 |
| `npi_any_subj-relc` | 1 → 8 | 185 / 121 | 0/100 | 0% | 0,95 / 0,97 (0,95 / 0,97) | 3,09 / 3,40 |
| `filler_gap_subj` | 2 → 8 | 162 / 106 | 0/100 | 0% | 0,89 / 0,89 (0,89 / 0,89) | 4,00 / 4,16 |
| `cleft` | 2 → 3 | 47 / 31 | 21/70 | 8% | 0,95 / 0,97 (0,95 / 0,97) | 3,30 / 3,21 |

**Bảng kiểu bài gốc** (trung bình qua layer của max theo vùng; số trong ngoặc là Table 11–14 của bài):

410M, odds, mình (bài):

| Tác vụ | DAS | Probe0 | Probe1 | Mean | PCA | k-means | LDA | Rand. | Vanilla |
|---|---|---|---|---|---|---|---|---|---|
| `agr_sv_num_subj-relc` | 5,55 (4,97) | 4,63 (4,32) | 4,59 (4,19) | 4,58 (3,72) | 0,98 (0,29) | 1,02 (0,28) | 0,16 (1,88) | 0,00 (0,03) | 4,75 (4,42) |
| `npi_any_subj-relc` | 8,07 (8,76) | 4,01 (4,01) | 4,00 (4,00) | 3,99 (3,99) | 2,28 (2,28) | 2,34 (2,34) | 0,15 (0,15) | 0,00 (0,01) | 4,08 (4,08) |
| `filler_gap_subj` | 11,51 (11,84) | 6,53 (6,53) | 6,44 (6,44) | 6,41 (6,41) | 4,87 (4,87) | 4,98 (4,98) | 0,18 (0,14) | 0,01 (0,01) | 6,34 (6,34) |
| `cleft` | 14,29 (14,46) | 5,52 (5,53) | 5,49 (4,84) | 5,48 (1,78) | 5,34 (0,86) | 5,48 (0,92) | 0,17 (0,05) | 0,01 (0,02) | 5,93 (5,79) |

410M, selectivity, mình (bài):

| Tác vụ | DAS | Probe0 | Probe1 | Mean | PCA | k-means | LDA | Rand. | Vanilla |
|---|---|---|---|---|---|---|---|---|---|
| `agr_sv_num_subj-relc` | 4,03 (3,64) | 6,08 (5,63) | 6,02 (5,45) | 6,01 (4,84) | 1,31 (0,40) | 1,39 (0,38) | 0,22 (2,43) | 0,01 (0,03) | 6,09 (5,52) |
| `npi_any_subj-relc` | 2,59 (2,13) | 4,13 (4,13) | 4,12 (4,12) | 4,12 (4,12) | 2,31 (2,31) | 2,39 (2,39) | 0,14 (0,14) | 0,00 (0,01) | 4,26 (4,26) |
| `filler_gap_subj` | 4,59 (4,23) | 6,28 (6,28) | 6,04 (6,04) | 5,98 (5,98) | 4,05 (4,05) | 4,18 (4,18) | 0,18 (0,15) | 0,01 (0,01) | 5,81 (5,81) |
| `cleft` | 6,50 (6,91) | 12,27 (12,09) | 12,22 (10,55) | 12,20 (3,99) | 11,94 (2,02) | 12,20 (2,13) | 0,30 (0,08) | 0,01 (0,02) | 13,27 (12,91) |

1B, odds, mình (bài):

| Tác vụ | DAS | Probe0 | Probe1 | Mean | PCA | k-means | LDA | Rand. | Vanilla |
|---|---|---|---|---|---|---|---|---|---|
| `agr_sv_num_subj-relc` | 7,05 (6,62) | 5,58 (5,23) | 5,57 (4,98) | 5,57 (4,24) | 2,66 (0,36) | 2,82 (0,39) | 0,26 (1,40) | 0,00 (0,01) | 5,84 (5,51) |
| `npi_any_subj-relc` | 9,76 (10,51) | 4,33 (4,33) | 4,33 (4,33) | 4,33 (4,33) | 2,80 (2,80) | 2,93 (2,93) | 0,20 (0,20) | 0,00 (0,00) | 4,41 (4,41) |
| `filler_gap_subj` | 11,44 (11,82) | 6,23 (6,23) | 6,19 (6,18) | 6,17 (6,17) | 3,77 (3,76) | 3,88 (3,87) | 0,19 (0,03) | 0,00 (0,00) | 6,23 (6,22) |
| `cleft` | 15,89 (15,56) | 5,81 (5,59) | 5,79 (3,76) | 5,78 (1,62) | 5,65 (0,25) | 5,78 (0,43) | 0,29 (0,16) | 0,00 (0,01) | 6,13 (6,04) |

1B, selectivity, mình (bài):

| Tác vụ | DAS | Probe0 | Probe1 | Mean | PCA | k-means | LDA | Rand. | Vanilla |
|---|---|---|---|---|---|---|---|---|---|
| `agr_sv_num_subj-relc` | 4,43 (4,13) | 7,46 (6,97) | 7,45 (6,59) | 7,45 (5,60) | 3,52 (0,42) | 3,72 (0,46) | 0,36 (1,75) | 0,00 (0,01) | 7,79 (7,32) |
| `npi_any_subj-relc` | 3,17 (3,32) | 4,62 (4,63) | 4,61 (4,62) | 4,61 (4,62) | 2,94 (2,95) | 3,07 (3,08) | 0,21 (0,21) | 0,00 (0,01) | 4,82 (4,83) |
| `filler_gap_subj` | 3,56 (3,51) | 5,94 (5,94) | 5,83 (5,82) | 5,80 (5,80) | 2,97 (2,96) | 3,25 (3,25) | 0,19 (0,03) | 0,00 (0,01) | 5,75 (5,74) |
| `cleft` | 4,22 (4,05) | 11,88 (11,38) | 11,83 (7,64) | 11,81 (3,36) | 11,55 (0,58) | 11,81 (0,96) | 0,40 (0,33) | 0,01 (0,03) | 12,54 (12,31) |

**Tách phần lệch theo lệch vị trí** (notebook 01b, ô 7):
- Tác vụ 0% cặp lệch (`npi_any_subj-relc`, `filler_gap_subj`): |tỉ lệ mình/bài − 1| lớn nhất của 6 phương pháp tất định là 0,001 (410M) và 0,002 (1B), tức bằng sai số làm tròn 2 chữ số của bài. Selectivity lệch ≤ 0,01 [ĐCM].
- Tác vụ có cặp lệch: tỉ lệ mình/bài của mean, PCA, k-means là 1,23 / 3,37 / 3,65 (`agr`, 410M), 1,31 / 7,39 / 7,23 (`agr`, 1B), 3,08 / 6,20 / 5,96 (`cleft`, 410M), 3,57 / 22,59 / 13,43 (`cleft`, 1B); probe1 ở `cleft` 1,13 / 1,54. Vanilla 1,02–1,08, DAS 0,99–1,12 [ĐCM].
- LDA lệch cả ở tác vụ không lệch vị trí (`filler_gap_subj` 1B: 0,19 so với 0,03), nên không do lỗi vị trí; giá trị nhỏ (< 0,3), không nằm trong tiêu chí.

**Ghi chú G1:**
1. **Pipeline trùng bài ở mọi chỗ trừ vị trí** [ĐCM cho 2 tác vụ không lệch vị trí]. Gồm cả dtype: nhóm chạy 1B ở fp32, bài ở bfloat16, mà số vẫn trùng tới 2 chữ số ở 2 tác vụ này. D-04 (FP = fp32) không làm mất tính so sánh.
2. **Lệch dồn vào đúng chỗ lỗi vị trí chạm tới** [GỢI Ý]: 2 tác vụ có cặp lệch, và các phương pháp học từ biểu diễn base do đơn vị Collect gom (mean, PCA, k-means; probe ít hơn, có thể nhờ điều chuẩn mạnh). DAS và vanilla gần như không đổi. Ngay trong bảng của bài, ở `cleft` mean (1,78) thấp hơn hẳn probe (5,53), trong khi ở tác vụ không lệch vị trí mean ≈ probe. Kiểm bằng G1r (D-16).
3. **DAS/vanilla** (odds): 410M 1,17 / 1,98 / 1,81 / 2,41 (trung vị 1,90); 1B 1,21 / 2,22 / 1,84 / 2,59 (trung vị 2,03). Hợp với Tanyel & Ayvaz (DAS > vanilla, trung vị 2,04 trên CausalGym) [GỢI Ý: cách đo có thể khác]. Hệ quả cho C1: báo cáo vanilla cạnh DAS ở mọi ô; odds DAS cao không có nghĩa biến được mã hoá mạnh hơn.
4. **`cleft` trùng train/eval:** 21/70 câu eval khác nhau có trong train, đều là câu pseudo-cleft (50/100 lượt câu). Bài gốc cũng vậy nên không ảnh hưởng G1. Với C1 (học lại DAS trên Q rồi so với FP), điểm DAS ở `cleft` một phần là điểm trên train. SPEC C1 phải chọn: giữ nguyên để so với G1, hay thêm tập eval không trùng (ví dụ lấy mẫu lại cặp có câu src chưa có trong train) [đề xuất, chưa chốt].
5. **Thời gian:** thời gian học DAS trung vị mỗi ô 3,5–3,8 s (410M), 4,4–7,6 s (1B). Phút mỗi tác vụ (9 phương pháp × tác vụ gốc + dog-give): 410M 26,4 / 43,8 / 47,7 / 11,0; 1B 31,3 / 63,5 / 64,4 / 12,9. Dùng để tính lại ngân sách C1 trong SPEC (D-11 ước với t = 6,41 s).
6. Chỉ 1 seed DAS; dao động DAS so với bài (0,92–1,12) chưa tách được giữa seed và phần cứng.

## Changelog
- v0.7 (16/11/2026, Claude): G1 đạt cho 410M và 1B (§2, §4 bảng áp tiêu chí, §10 mới); D-13 ghi đã xác nhận; thêm D-16 (G1r, quy tắc đặt trước khi chạy); §5 cập nhật việc (gộp `HUONG_DAN_VIEC_14_18_11.md` vào `VIEC_CAN_LAM.md`); §6 thêm dòng G1 (5,06 giờ), tổng 5,66 giờ; §7 câu 6 cập nhật; §8: CausalGym (đối chiếu Table 11–14 với PDF), Zhou (PDF đã có trong Project), repo gốc điểm 6, 9, 10, F thêm bằng chứng từ G1. File mới: `notebooks/01b_phan_tich_g1.ipynb`.
- v0.6 (13/11/2026 lần 3, Claude): G1 ghi "đang chạy" và coi D-13 đã xác nhận (người dùng báo); G-N đổi sang `notebooks/96_gn_tra_cuu_api.ipynb` (Semantic Scholar + OpenAlex + arXiv), bỏ Google Scholar, đổi trước khi có dữ liệu; nhận xét thầy do Claude viết từ nội dung người dùng dán; §5 cập nhật việc.
- v0.5 (13/11/2026 lần 2, Claude): §2 thêm kết quả phiên lần 2; §3 thêm ghi chú vào D-13 (phạm vi lỗi điểm 9; trùng train/eval ở `cleft`) và D-15 (đường GPTQ, đề xuất); §4 G-N cập nhật, G1 ghi điều kiện tin kết quả; §5 cập nhật việc; §6 thêm ước giờ notebook 97; §8 thêm 7 nguồn (pyvene 0.1.6, GPT-QModel, Nwaiwu, PAHQ, 2606.06267, tokenizer bản sao, ghi chú QError), cập nhật Zhou, Tanyel & Ayvaz, Makarov, Bhandari & Wade, Duan, CausalGym; bảng repo gốc thêm bằng chứng chạy cho điểm 6, 8, 9, 10 và thêm điểm A–F. File mới: `PHIEU_KIEM_REPO_GOC.md`, `GN_TRA_CUU.md`, `GHI_CHU_BAI_BAO.md`, `HUONG_DAN_VIEC_14_18_11.md`, `notebooks/97_kiem_gptqmodel.ipynb`, `notebooks/98_kiem_repo_goc.ipynb`.
- v0.4 (13/11/2026, Claude): G0 đạt; §4 thêm bảng áp quy tắc G0b và tiêu chí G1 định lượng; §9 điền kết quả G0b, bảng co biên độ, sửa bảng run (mỗi job một dòng); §6 sửa dòng G0b (0,51 giờ), thêm tổng; thêm D-11 (bỏ ô chính, đo theo layer), D-12 (chuẩn hoá T theo R), D-13 (thiết kế G1, chờ xác nhận), D-14 (Claude tự cập nhật sổ); §8 thêm 7 nguồn (Tanyel & Ayvaz, Wu et al., Yao et al., Bhandari & Wade, dataset HF, quant-lens, checkpoint Xu-Ouyang), cập nhật Zhou và Boguraev, ghi 2 nguồn chưa xác minh; repo gốc thêm điểm 9–12, sửa điểm 6; §7 thêm câu hỏi 6; §5 cập nhật việc.
- v0.3 (12/11/2026): điền §9 kết quả G0 full; áp 4 quy tắc G0 (§4: G0 một phần); thêm D-08, D-09, D-10; §6 dòng GPU đầu tiên; §8 thêm repo gốc và 8 điểm đối chiếu; §5 cập nhật việc cần làm.
- v0.2 (12/11/2026): thêm D-07; thay script `g0_pilot.py` bằng notebook `00_g0_pilot.ipynb` chạy qua `configs/kaggle_run.yaml`; §9 thêm bảng run.
- v0.1 (12/11/2026): tạo sổ; ghi D-01 đến D-06; cổng G-N…G3; quy tắc G0; sổ nguồn; hướng dẫn chạy G0.
