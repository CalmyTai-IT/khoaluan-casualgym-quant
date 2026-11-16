# GHI_CHU_BAI_BAO.md — Ghi chú bài báo liên quan (số liệu cho đề cương và báo cáo)

> Bản 13/11/2026 (Claude). File này lớn dần: mỗi bài một mục theo cùng một khung (§0). Bài người dùng gửi sau sẽ thêm vào đây.
> Quy ước: [ĐCM] đã kiểm chứng với nguồn mở được · [GỢI Ý] có bằng chứng nhưng chưa đủ · [PHỎNG ĐOÁN] chưa kiểm · [CHƯA XÁC MINH] chưa mở được nguồn.
> Số liệu ghi kèm vị trí (§, Bảng, Hình). Số đọc qua công cụ trích văn bản (không phải tự đọc PDF) ghi "(trích máy)" và **phải đối chiếu PDF trước khi đưa vào luận văn**.

## 0. Khung cho mỗi bài

- **Thông tin:** tác giả, năm, tiêu đề, nơi đăng, mã arXiv/DOI.
- **Đã đọc:** toàn văn / một phần (phần nào) / chỉ tóm tắt; ngày đọc; nguồn mở được.
- **Thiết lập:** model; lượng tử hoá (phương pháp, bit, group size, đối xứng hay không, dữ liệu hiệu chỉnh, công cụ, giả lập hay kernel thật); dữ liệu và số mẫu; số seed.
- **Đo gì, bằng gì.**
- **Số liệu chính** (mỗi số kèm vị trí).
- **Liên quan đề tài:** đóng góp nào (RQ0/G1, C1, C2, C3b, C3, C4); trùng hay khác; nhóm lấy gì dùng.
- **Giới hạn và rủi ro khi trích dẫn.**
- **Còn phải làm.**

---

## 1. Zhou et al. (2026) — hai kiểu hỏng khi lượng tử hoá

- **Thông tin:** Chenxi Zhou, Pengfei Cao, Jiang Li, Bohan Yu, Jinyu Ye, Jun Zhao, Kang Liu. "From Signal Degradation to Computation Collapse: Uncovering the Two Failure Modes of LLM Quantization". Findings of ACL 2026, tr. 23204–23222. ACL Anthology `2026.findings-acl.1162`; arXiv 2604.19884 (21/4/2026).
- **Đã đọc:** PDF ACL Anthology, 13/11/2026, qua công cụ trích (trích máy). [ĐCM] cho tiêu đề, tác giả, trang, nơi đăng (trang ACL + PDF).
- **Thiết lập (trích máy):**
  - Model: Llama-3.1-8B (chính), Qwen3-8B, Mistral-7B-Instruct-v0.3, Gemma-2-9B-it (§3.1).
  - Lượng tử hoá: GPTQ là chính; AWQ để kiểm tính tổng quát trên Llama-3.1-8B (§3.1, Phụ lục D). Chỉ trọng số. So 4 bit với 2 bit; 3 và 8 bit làm bối cảnh. Group size 128; hiệu chỉnh 128 chuỗi C4 dài 2048 token; công cụ **GPTQModel** (Phụ lục A.1). Không nêu giả lập hay kernel thật.
  - Tác vụ: nhớ lại kiến thức (factual recall) trên ParaRel, 39 loại quan hệ (§3.1). Chia mỗi model thành tập Robust (đúng ở cả FP16 và 4 bit) và Failure (đúng ở FP16, sai ở 4 bit) (§3.1). Cỡ (Bảng 4, Tổng / Robust / Failure): Llama-3.1-8B 7.777 / 5.661 / 2.116; Qwen3-8B 4.055 / 3.558 / 497; Mistral-7B 4.294 / 3.787 / 507; Gemma-2-9B 6.375 / 5.601 / 774.
- **Đo gì:** logit lens theo layer; activation patching từ FP sang Q (đủ); zero ablation (cần); entropy attention và JSD; tỉ lệ đảo dấu cổng FFN; CKA; tương đồng không gian con SVD; "domino test" (lượng tử hoá k layer đầu).
- **Số liệu chính (trích máy):**
  - 4 bit, tập Failure: tín hiệu đáp án vẫn xuất hiện ở layer giữa đến cuối nhưng yếu hơn (§3.3, Hình 3). Patch activation FP vào Q tại token chủ ngữ cuối ở layer sớm phục hồi dự đoán (§3.4, Hình 4).
  - 2 bit: xác suất token đúng gần 0 ở mọi layer; patch không có tác dụng (§3.3–3.4). Đảo dấu cổng FFN > 30%; tương đồng không gian con (top 50) gần 0 so với > 0,8 ở 4 bit (Hình 7, Hình 9).
  - Domino 2 bit, Llama-3.1-8B, accuracy Robust / Failure (Bảng 2): FP16 100 / 100; k = 0: 65,47 / 15,03; k = 1: 41,65 / 5,29; k = 2: 24,66 / 2,50; k = 3: 10,72 / 1,04; k = 5: 2,51 / 0,38. Công cụ trích lưu ý cách đánh số k ("k = 0 (Layer 0)" so với "k = 1 là hai layer đầu") chưa rõ; kiểm lại trong PDF.
  - Sửa 4 bit không cần huấn luyện (Bảng 1, tập Failure, gốc → sửa cơ bản → sửa + khuếch đại): Llama3.1-8B 0,00% → 67,91% → 75,19%; Mistral-7B 0,00% → 66,86% → 81,26%; Qwen3-8B 0,00% → 40,24% → 79,88%; Gemma2-9B 0,00% → 33,85% → 64,08%. Mức 0% là do cách chia tập.
  - Phụ lục E (Bảng 6, Llama-3.1-8B, FP16 / 4 / 3 / 2 bit): MMLU 63,42 / 61,44 / 49,11 / 24,18; GSM8K 56,79 / 51,33 / 10,16 / 0,99.
  - 4 bit, Llama và Mistral: module MLP nhạy hơn attention; Qwen và Gemma cân bằng hơn (Phụ lục C.1, Bảng 5).
- **Liên quan đề tài:**
  - **C2** [GỢI Ý, không trùng]: hai kiểu hỏng của Zhou tương ứng câu hỏi "mã hoá yếu đi hay đọc ra hỏng" của C2. Khác biệt: Zhou patch **toàn bộ activation** ở token chủ ngữ cho bài nhớ kiến thức trên model 7–9B; C2 chèn **một toạ độ v do DAS tìm** giữa FP và Q, ở cấp biến, trên tác vụ cú pháp của CausalGym, Pythia ≤ 1B, có null hai phía và sàn step0. Nên viết rõ khác biệt này trong đề cương.
  - **G0b** [GỢI Ý]: G0b thấy họ 2 bit khác họ 3–4 bit (T theo ô cao hơn R ở layer giữa). Hợp với nhận định hai kiểu hỏng, nhưng mới 1 tác vụ, 1 seed mỗi ô.
  - **Phân tích phụ cho "hỏng ở đâu, theo thứ tự nào"** [GỢI Ý]: domino test (chỉ lượng tử hoá k layer đầu, hoặc k layer cuối) rẻ và đọc thẳng được thứ tự. Có thể thêm như phân tích phụ của C1/C3, tốn ít GPU.
  - **C4 / cấu hình GPTQ:** dùng làm mẫu ghi cấu hình (GPTQModel, g = 128, hiệu chỉnh C4 128 × 2048). Nhóm phải chọn C4 hay WikiText-2 và ghi rõ.
- **Giới hạn khi trích:** chỉ nhớ kiến thức, model lớn hơn nhiều; số liệu là trích máy.
- **Còn phải làm:** TV-A tải đúng PDF `2026.findings-acl.1162` lên Project; đối chiếu Bảng 1, 2, 4, 6 và cách đánh số k.

## 2. Tanyel & Ayvaz (2026) — DAS vượt vanilla là do hàm mục tiêu

- **Thông tin:** Toygar Tanyel, Serkan Ayvaz. "Whose Effect Is It? How Objectives Inflate Learned Subspace Interventions". arXiv 2611.05033v1 (3/11/2026), cs.CL. [ĐCM trang tóm tắt arXiv]
- **Đã đọc:** chỉ trang tóm tắt và các đoạn HTML hiện trong kết quả tìm kiếm (13/11/2026). Trang HTML bị giới hạn tốc độ truy cập 4 lần trong phiên này. **Chưa đọc toàn văn.**
- **Nội dung đã thấy:**
  - Tóm tắt: khi chỉ đổi hàm mục tiêu để nhắm vào cái mà mạng tự tạo ra, phần lớn phần vượt (so với patch cả trạng thái) mất đi; vậy hiệu ứng học được lớn hơn không phải bằng chứng mạnh hơn. [ĐCM trang tóm tắt]
  - Trên CausalGym, điểm DAS có trung vị gấp 2–3 lần patch cả trạng thái; phần dẫn trước của DAS là phần vượt, không phải vùng tốt hơn. [ĐCM đoạn HTML]
  - Phụ lục E.1: trong mọi bản đồ dựng lại, DAS cao hơn vanilla, trung vị gấp **2,04** (tứ phân vị 1,46–2,71); code CausalGym công bố truyền vị trí base và source theo thứ tự đảo (Hình 13). [ĐCM đoạn HTML]
  - Họ dựng lại bản đồ theo giao thức CausalGym (learning rate, batch size, một lượt), trừ learning rate hằng (CausalGym có lịch); bản đồ phủ cả layer lẻ. [ĐCM đoạn HTML]
  - DAS vẫn bám ở vị trí licensor qua các layer mà patch cả trạng thái ở đó gần như không có tác dụng. [ĐCM đoạn HTML]
  - Một bảng ở §7.1 có hai dòng "CausalGym" (+29 (29) | +20 | +39 (28) | +29 | +74 (29) | +52) và "CausalGym number-only" (+18 (6) | +15 | +22 (6) | +17 | +42 (6) | +34), tiêu đề cột thấy được: Pythia / DAS, Qwen2.5 / max., Qwen2.5 / DAS, Llama / max., Llama / DAS. Tiêu đề bị cắt, **chưa rõ ý nghĩa số**; không dùng cho tới khi đọc PDF. [CHƯA XÁC MINH]
- **Liên quan đề tài:**
  - **Điểm 9 (đảo vị trí)** nay có ba nguồn độc lập: Claude đọc code, phép chạy pyvene trong notebook 98, và Tanyel & Ayvaz. Tỉ lệ cặp eval (split test) có vị trí base khác vị trí src: 16% ở `agr_sv_num_subj-relc`, 8% ở `cleft`, 0% ở `npi_any_subj-relc` và `filler_gap_subj` (notebook 98, sổ §8).
  - **G1** [GỢI Ý]: dự kiến DAS / vanilla khoảng 2 lần. G0b đã thấy DAS vượt trần tráo trung thực (odds 7,33 và 8,70 so với 2 × logit diff = 6,59). Nếu G1 ra tỉ lệ khác xa 2, cần xem lại.
  - **C1** [GỢI Ý]: odds DAS gồm cả phần vượt do hàm mục tiêu. Trục (b) "dùng lại hướng FP trên Q" ít bị ảnh hưởng hơn học lại (b'), vì hướng không được tối ưu lại trên Q; nhưng phần vượt nằm sẵn trong hướng FP. Đề xuất cho SPEC C1: báo cáo vanilla ở cùng ô làm mốc, và báo cáo tỉ lệ DAS/vanilla ở FP và Q. Nếu Q làm giảm odds DAS mà vanilla không đổi, phần mất có thể là phần vượt chứ không phải cơ chế.
- **Còn phải làm (TV-A, 18/11):** tải PDF lên Project. Đọc và ghi: (1) hàm mục tiêu thay thế là gì; (2) ý nghĩa bảng §7.1; (3) E.1: lỗi đảo vị trí ảnh hưởng bao nhiêu và sửa có đổi kết quả không; (4) Corollary 7 phát biểu gì.

## 3. Makarov (2026) — steering OT theo cụm dưới INT8/NF4, kiểm định tương đương

- **Thông tin:** Illia Makarov. "One Vector or Many? Clustered Optimal-Transport Steering under Quantization". arXiv 2610.40055v1 (29/10/2026), 34 trang, 12 hình, 14 bảng. [ĐCM trang tóm tắt arXiv]
- **Đã đọc:** trang tóm tắt và đoạn HTML qua tìm kiếm (13/11/2026). Sổ v0.4 ghi "[ĐCM] PDF" từ phiên trước, nhưng PDF chưa có trong Project nên Claude phiên này không mở lại được.
- **Thiết lập đã thấy:** Gemma-2-2B và Granite-3.1-2B; giảm độc tính (toxicity); INT8 và NF4. [ĐCM tóm tắt]
- **Cách kiểm định tương đương** [ĐCM đoạn HTML]:
  - TOST dạng khoảng (Schuirmann, 1987): hai phương pháp **tương đương** nếu khoảng bootstrap ghép cặp **90%** của **tỉ số các trung bình** (trung bình nhân với perplexity) nằm trong một biên **cố định trước**.
  - Tám phép kiểm (2 model × 2 cường độ × 2 thước đo) đều phải ra tương đương, nên không cần hiệu chỉnh đa phép kiểm.
  - Hình 8 dùng khoảng 95% chưa hiệu chỉnh cho hiệu số.
  - Chuyển ánh xạ từ FP sang model NF4 thay vì học lại không làm tăng độc tính có ý nghĩa sau hiệu chỉnh đa phép kiểm. [ĐCM tóm tắt]
  - NF4 dịch activation trung bình của văn bản dùng để khớp 7–11%, INT8 2–3%; INT8 không đổi độc tính hay lặp từ có ý nghĩa. [ĐCM đoạn HTML]
- **Chưa thấy:** **giá trị biên** cho từng thước đo và lý do chọn. Đây đúng là phần SPEC C1 cần.
- **Liên quan đề tài (SPEC C1)** [GỢI Ý]:
  - Dùng TOST dạng khoảng với KTC 90% trên **tỉ số Q/FP**. Hợp với D-12 (T_rel là tỉ số) và D-05 (ba nhãn).
  - Biên: Makarov cố định trước theo ngưỡng thực tế; D-05 lấy biên từ null FP–FP theo seed. Cả hai được, nhưng phải chốt trong SPEC trước khi chạy.
  - Hai họ phép kiểm khác nhau: kết luận "tương đương ở **mọi** layer" là giao của các phép kiểm (intersection–union), không cần hiệu chỉnh; kết luận "khác ở layer k" cho từng layer cần Benjamini–Hochberg như đề xuất §2.4. SPEC nên ghi rõ câu hỏi nào dùng họ nào.
  - "Chuyển từ FP so với học lại trên Q" của Makarov tương ứng trục (b) so với (b') của C1.
- **Còn phải làm (TV-A, 18/11):** thêm PDF vào Project; chép đúng biên tương đương, cách chọn biên, số lần bootstrap, đơn vị lấy mẫu lại.

## 4. Bài khác gặp khi tra G-N (13/11/2026)

| Bài | Trạng thái | Nội dung | Mức trùng với đề tài |
|---|---|---|---|
| Nwaiwu, Jongsawat, Tungkasthan, arXiv 2512.13725 | [ĐCM trang arXiv] | "Compressed Causal Reasoning": Llama-3-8B, BF16/INT8/NF4, đo accuracy trên CLadder (lập luận nhân quả) | Không trùng: đo hành vi, không đo cơ chế bên trong |
| Wang et al., arXiv 2510.23264 (PAHQ) | [ĐCM trang arXiv] | Dùng lượng tử hoá hỗn hợp theo đầu attention để **tăng tốc** tìm mạch (ACDC); RTN 8 bit đồng loạt làm ACDC hỏng (AUC-ROC 0,982 → 0,534, theo bản tóm tắt bên thứ ba) | Không trùng; số 0,534 [CHƯA XÁC MINH] từ trang tổng hợp |
| arXiv 2606.06267 (UKPLab, "phantom specialization") | [ĐCM trang arXiv, chưa ghi tác giả] | 75 mạch trên 5 model Pythia 70M–1.4B; nhiều mạch khác cấu trúc cùng thực hiện một phép tính | Không về nén; liên quan cảnh báo "cơ chế không duy nhất" khi diễn giải C1 |
| arXiv 2506.12044 ("QError", repo `terarachang/QError`) | [ĐCM đoạn PDF] | Cross-model activation patching để tìm nơi lỗi lượng tử hoá phát sinh; độ lớn activation FP tương quan âm với lỗi | Có thể chính là "Chang et al., EMNLP 2025" trong sổ; **chưa đối chiếu** tên tác giả và nơi đăng |
| Dự án hackathon "EdgeAlign" (Devpost) | trang Devpost | Pythia-70M, INT8 giả lập trên activation, độ bền mạch | Không phải bài khoa học; chỉ cho thấy ý tưởng đang được quan tâm |

Chưa thấy bài nào đo DAS/DII dưới lượng tử hoá trọng số trên CausalGym. Đây là [GỢI Ý], chưa đủ để đóng G-N: còn thiếu danh sách "Cited by" (xem `GN_TRA_CUU.md`).
