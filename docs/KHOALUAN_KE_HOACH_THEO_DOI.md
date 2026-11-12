# KHOALUAN_KE_HOACH_THEO_DOI.md — Sổ dự án khoá luận

> Version: v0.2 · Ngày: 12/11/2026 · Nguồn sự thật của project. Đề xuất chi tiết: `DEXUAT_HUONG_B1_DAS.md` v0.5. Quy trình: `QUY_TRINH_LAM_VIEC.md`. Việc trước mắt: `VIEC_CAN_LAM.md`.
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

## 2. Trạng thái hiện tại (12/11/2026)

- Đã có:
  - đề xuất v0.4, review v0.4 (tài liệu Claude Docs), đề xuất v0.5;
  - khung repo: runner Kaggle, `configs/kaggle_run.yaml`, notebook `notebooks/00_g0_pilot.ipynb`. Đã chạy thử bằng TOY_TEST và papermill trên CPU, **chưa chạy trên Pythia thật**.
- Đang làm: G0 (chạy pilot trên Kaggle), G-N (kiểm tính mới).
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

## 4. Cổng quyết định

| Cổng | Hạn | Điều kiện đạt | Trạng thái | Nếu không đạt |
|---|---|---|---|---|
| G-N tính mới | 17/11/2026 | "Cited by" của CausalGym, Ouyang, Duan, Makarov; tìm thêm; không ai đã làm C1/C2/C3b | Đang làm | Bỏ hoặc đổi đóng góp bị trùng |
| G0 chạy được | 22/11/2026 | Chạy hết `notebooks/00_g0_pilot.ipynb` trên 410M; có t; có vùng chuyển tiếp; có sàn step0; đo t cho 1B | Đang làm | Thu phạm vi theo t đo được |
| G1 tái lập | 31/12/2026 (có thể dời 15/01/2027) | Đúng thứ tự phương pháp và thứ tự xuất hiện vị trí; odds cùng bậc | Chưa | Dừng phát triển; sửa pipeline; hỏi tác giả |
| G2 MVP C1 + C2 | 28/02/2027 | Hồ sơ đầy đủ cho 2 model × 4 tác vụ | Chưa | Giảm tác vụ; chỉ 410M |
| G3 MVP C3b | 31/03/2027 | Đường QiD mức cơ chế qua ≥ 5 checkpoint cho ≥ 1 tác vụ | Chưa | Viết luận văn với C1 + C2 |

**Quy tắc quyết định ở G0 (đặt trước khi chạy):**

1. **Thời gian.** Nếu t (học + đánh giá một ô) ≤ 60 giây cho 410M, giữ kế hoạch. Nếu > 60 giây, chỉ học lại ở ô chính và giảm số vị trí.
2. **Lưới nén.** Chọn 3–4 mức (bit hoặc α) sao cho accuracy giảm dần từ ≥ 95% của FP xuống gần mức ngẫu nhiên. Nếu 8 bit đã sụp, có lỗi code.
3. **Sàn step0.** Nếu odds step0 ≥ 50% odds FP ở ô chính, thì DAS học lại (b') không đủ thông tin. Khi đó C1 dựa chủ yếu vào (b) dùng lại hướng, và C3 cần ngưỡng khác.
4. **Seed.** Nếu |cos| giữa các seed < 0.9 ở ô chính, thì trục hình học (c) không dùng được; báo cáo như một kết quả về độ bất ổn của DAS.

## 5. Việc cần làm

- [ ] (TV-A, 13/11) Thiết lập repo và Kaggle runner; chạy smoke test (xem `VIEC_CAN_LAM.md` mục 1–3)
- [ ] (TV-A, 15/11) G0 đầy đủ 410M + đo thời gian 1B trong cùng một version; ghi kết quả vào §9
- [ ] (TV-B, 16/11) Đối chiếu với repo `aryamanarora/causalgym`: BOS, cách tách token theo vùng, hàm loss, công thức odds
- [ ] (Cả hai, 17/11) G-N: "Cited by" trên Google Scholar; đọc Makarov 2610.40055 và Duan 2606.03002
- [ ] (TV-A, 18/11) Kiểm GPT-QModel với `gpt_neox` trên Pythia-70M
- [ ] (Cả hai, 22/11) Chốt G0; cập nhật đề xuất lên v0.6 nếu cần
- [ ] (TV-A, 23–30/11) Đề cương theo mẫu FIT; gửi thầy kèm 5 câu hỏi ở §7
- [ ] Ghi lần nhận xét thứ 3 vào `NHAN_XET_GVHD.md`; đóng sổ đề tài cũ lên v1.4

## 6. Nhật ký GPU

Kaggle tính quota theo thời gian phiên. Ghi mỗi lần chạy để biết còn bao nhiêu.

| Ngày | Tài khoản | Việc | Model | Giờ GPU | Ghi chú |
|---|---|---|---|---|---|
| | | | | | |

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

## 9. G0 — cách chạy và kết quả

**Cách chạy** (theo `QUY_TRINH_LAM_VIEC.md`):
- Notebook: `notebooks/00_g0_pilot.ipynb`.
- Ba job đã khai báo trong `configs/kaggle_run.yaml`:
  - `g0_smoke_410m`: đang bật;
  - `g0_full_410m`: đang tắt;
  - `g0_timing_1b`: đang tắt.
- Bật/tắt bằng `enabled`, commit, rồi Save Version trên runner. Các bước chi tiết nằm trong `VIEC_CAN_LAM.md`.
- Nếu tải dữ liệu lỗi, thêm `"datasets>=3"` vào mục `pip:` trong file cấu hình.

**Run đã chạy:**

| run_id | Commit | Job | Trạng thái | Phút |
|---|---|---|---|---|
| | | | | |

**Kết quả (điền sau khi chạy):**

| Chỉ số | 410M | 1B |
|---|---|---|
| t học + đánh giá một ô (giây) | | |
| Accuracy / logit diff FP | | |
| Odds FP cao nhất (layer, vùng) | | |
| Accuracy theo bit 8/6/4/3 | | — |
| Accuracy theo α (4 bit) 0.25/0.5/0.75 | | — |
| Spearman bản đồ dùng lại theo bit | | — |
| Odds học lại trên Q 8/4/3 bit, \|cos\| với FP | | — |
| Tách đoạn 4 bit: pre / post / all | | — |
| Sàn step0 (odds) | | — |
| \|cos\| giữa seed; khoảng odds | | — |
| Quyết định theo §4 | | |

## Changelog
- v0.2 (12/11/2026): thêm D-07 (quy trình GitHub → Kaggle runner, Save Version, notebook-first); thay script `g0_pilot.py` bằng notebook `00_g0_pilot.ipynb` chạy qua `configs/kaggle_run.yaml`; §9 thêm bảng run.
- v0.1 (12/11/2026): tạo sổ; ghi D-01 đến D-06; cổng G-N…G3; quy tắc G0; sổ nguồn; hướng dẫn chạy G0.
