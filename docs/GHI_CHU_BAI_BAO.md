# GHI_CHU_BAI_BAO.md — Ghi chú bài báo liên quan (số liệu cho đề cương và báo cáo)

> Bản 16/11/2026 (Claude). Thay bản 13/11: cập nhật "Còn phải làm" của §1–§3 (PDF đã có trong Project), xác nhận Chang et al. ở §4, thêm §5 (bài lân cận từ G-N).
> File này lớn dần: mỗi bài một mục theo cùng một khung (§0). Bài người dùng gửi sau sẽ thêm vào đây.
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
  - **Phân tích phụ cho "hỏng ở đâu, theo thứ tự nào"** [GỢI Ý]: domino test (chỉ lượng tử hoá k layer đầu, hoặc k layer cuối) rẻ và đọc thẳng được thứ tự. Có thể thêm như phân tích phụ của C1, tốn ít GPU.
  - **C4 / cấu hình GPTQ:** dùng làm mẫu ghi cấu hình (GPTQModel, g = 128, hiệu chỉnh C4 128 × 2048). Nhóm phải chọn C4 hay WikiText-2 và ghi rõ.
- **Giới hạn khi trích:** chỉ nhớ kiến thức, model lớn hơn nhiều; số liệu là trích máy.
- **Còn phải làm:** PDF đúng bài (`2026.findings-acl.1162.pdf`) đã có trong Project từ 14/11. Còn đối chiếu Bảng 1, 2, 4, 6 và cách đánh số k với PDF.

## 2. Tanyel & Ayvaz (2026) — DAS vượt vanilla là do hàm mục tiêu

- **Thông tin:** Toygar Tanyel, Serkan Ayvaz. "Whose Effect Is It? How Objectives Inflate Learned Subspace Interventions". arXiv 2611.05033v1 (3/11/2026), cs.CL. [ĐCM trang tóm tắt arXiv]
- **Đã đọc:** chỉ trang tóm tắt và các đoạn HTML hiện trong kết quả tìm kiếm (13/11/2026). **Chưa đọc toàn văn.** PDF có trong Project từ 16/11 (`2611.05033v1.pdf`).
- **Nội dung đã thấy:**
  - Tóm tắt: khi chỉ đổi hàm mục tiêu để nhắm vào cái mà mạng tự tạo ra, phần lớn phần vượt (so với patch cả trạng thái) mất đi; vậy hiệu ứng học được lớn hơn không phải bằng chứng mạnh hơn. [ĐCM trang tóm tắt]
  - Trên CausalGym, điểm DAS có trung vị gấp 2–3 lần patch cả trạng thái; phần dẫn trước của DAS là phần vượt, không phải vùng tốt hơn. [ĐCM đoạn HTML]
  - Phụ lục E.1: trong mọi bản đồ dựng lại, DAS cao hơn vanilla, trung vị gấp **2,04** (tứ phân vị 1,46–2,71); code CausalGym công bố truyền vị trí base và source theo thứ tự đảo (Hình 13). [ĐCM đoạn HTML]
  - Họ dựng lại bản đồ theo giao thức CausalGym (learning rate, batch size, một lượt), trừ learning rate hằng (CausalGym có lịch); bản đồ phủ cả layer lẻ. [ĐCM đoạn HTML]
  - DAS vẫn bám ở vị trí licensor qua các layer mà patch cả trạng thái ở đó gần như không có tác dụng. [ĐCM đoạn HTML]
  - Một bảng ở §7.1 có hai dòng "CausalGym" và "CausalGym number-only"; tiêu đề bị cắt, **chưa rõ ý nghĩa số**; không dùng cho tới khi đọc PDF. [CHƯA XÁC MINH]
- **Đối chiếu với kết quả của nhóm:**
  - G1 (16/11): DAS/vanilla (odds) trung vị 1,90 (410M) và 2,03 (1B) trên 4 tác vụ, hợp với 2,04 của họ [GỢI Ý: cách đo có thể khác].
  - G1r (16/11): chạy lại theo lỗi vị trí của code gốc. Ở `agr_sv_num_subj-relc`, mọi phương pháp về khớp bài (tỉ lệ 0,82–1,20); ở `cleft`, mean/PCA/k-means vẫn lệch (sổ §10). Khi đọc PDF, so với phần họ lượng hoá ảnh hưởng của lỗi (nếu có).
- **Liên quan đề tài:**
  - **Điểm 9 (đảo vị trí)** nay có bốn nguồn độc lập: Claude đọc code; notebook 98 (Claude và TV-B, pyvene 0.1.6); phiếu kiểm của TV-B; Tanyel & Ayvaz.
  - **C1** [GỢI Ý]: odds DAS gồm cả phần vượt do hàm mục tiêu. Đề xuất cho SPEC C1: báo cáo vanilla ở cùng ô làm mốc, và báo cáo tỉ lệ DAS/vanilla ở FP và Q. Nếu Q làm giảm odds DAS mà vanilla không đổi, phần mất có thể là phần vượt chứ không phải cơ chế.
- **Còn phải làm (khi viết SPEC C1):** Claude đọc PDF trong Project và ghi: (1) hàm mục tiêu thay thế là gì; (2) ý nghĩa bảng §7.1; (3) E.1: lỗi đảo vị trí ảnh hưởng bao nhiêu và sửa có đổi kết quả không; (4) Corollary 7 phát biểu gì. TV-A kiểm lại 3–5 số.

## 3. Makarov (2026) — steering OT theo cụm dưới INT8/NF4, kiểm định tương đương

- **Thông tin:** Illia Makarov. "One Vector or Many? Clustered Optimal-Transport Steering under Quantization". arXiv 2610.40055v1 (29/10/2026), 34 trang, 12 hình, 14 bảng. [ĐCM trang tóm tắt arXiv]
- **Đã đọc:** trang tóm tắt và đoạn HTML qua tìm kiếm (13/11/2026). PDF có trong Project từ 16/11 (`2610.40055v1.pdf`); Claude chưa đọc lại.
- **Thiết lập đã thấy:** Gemma-2-2B và Granite-3.1-2B; giảm độc tính (toxicity); INT8 và NF4. [ĐCM tóm tắt]
- **Cách kiểm định tương đương** [ĐCM đoạn HTML]:
  - TOST dạng khoảng (Schuirmann, 1987): hai phương pháp **tương đương** nếu khoảng bootstrap ghép cặp **90%** của **tỉ số các trung bình** nằm trong một biên **cố định trước**.
  - Tám phép kiểm (2 model × 2 cường độ × 2 thước đo) đều phải ra tương đương, nên không cần hiệu chỉnh đa phép kiểm.
  - Hình 8 dùng khoảng 95% chưa hiệu chỉnh cho hiệu số.
  - Chuyển ánh xạ từ FP sang model NF4 thay vì học lại không làm tăng độc tính có ý nghĩa sau hiệu chỉnh đa phép kiểm. [ĐCM tóm tắt]
  - NF4 dịch activation trung bình của văn bản dùng để khớp 7–11%, INT8 2–3%; INT8 không đổi độc tính hay lặp từ có ý nghĩa. [ĐCM đoạn HTML]
- **Chưa thấy:** **giá trị biên** cho từng thước đo và lý do chọn. Đây đúng là phần SPEC C1 cần.
- **Liên quan đề tài (SPEC C1)** [GỢI Ý]:
  - Dùng TOST dạng khoảng với KTC 90% trên **tỉ số Q/FP**. Hợp với D-12 (T_rel là tỉ số) và D-05 (ba nhãn).
  - Biên: Makarov cố định trước theo ngưỡng thực tế; D-05 lấy biên từ null FP–FP theo seed. Cả hai được, nhưng phải chốt trong SPEC trước khi chạy.
  - Hai họ phép kiểm khác nhau: "tương đương ở **mọi** layer" là giao của các phép kiểm (intersection–union), không cần hiệu chỉnh; "khác ở layer k" cho từng layer cần Benjamini–Hochberg như đề xuất §2.4. SPEC nên ghi rõ câu hỏi nào dùng họ nào.
  - "Chuyển từ FP so với học lại trên Q" của Makarov tương ứng trục (b) so với (b') của C1.
- **Còn phải làm (khi viết SPEC C1):** Claude đọc PDF trong Project; chép đúng biên tương đương, cách chọn biên, số lần bootstrap, đơn vị lấy mẫu lại. TV-A kiểm lại 3–5 số.

## 4. Bài khác gặp khi tra G-N bằng web (13/11/2026)

| Bài | Trạng thái | Nội dung | Mức trùng với đề tài |
|---|---|---|---|
| Nwaiwu, Jongsawat, Tungkasthan, arXiv 2512.13725 | [ĐCM trang arXiv] | "Compressed Causal Reasoning": Llama-3-8B, BF16/INT8/NF4, đo accuracy trên CLadder (lập luận nhân quả) | Không trùng: đo hành vi, không đo cơ chế bên trong |
| Wang et al., arXiv 2510.23264 (PAHQ) | [ĐCM trang arXiv] | Dùng lượng tử hoá hỗn hợp theo đầu attention để **tăng tốc** tìm mạch (ACDC); RTN 8 bit đồng loạt làm ACDC hỏng (AUC-ROC 0,982 → 0,534, theo bản tóm tắt bên thứ ba) | Không trùng; số 0,534 [CHƯA XÁC MINH] từ trang tổng hợp |
| arXiv 2606.06267 (UKPLab, "phantom specialization") | [ĐCM trang arXiv, chưa ghi tác giả] | 75 mạch trên 5 model Pythia 70M–1.4B; nhiều mạch khác cấu trúc cùng thực hiện một phép tính | Không về nén; liên quan cảnh báo "cơ chế không duy nhất" khi diễn giải C1 |
| Chang, Zhang, Thomason, Jia. "Why Do Some Inputs Break Low-Bit LLM Quantization?" EMNLP 2025 (`2025.emnlp-main.168`); arXiv 2506.12044; repo `terarachang/QError` | [ĐCM đoạn PDF 13/11; tác giả và nơi đăng xác nhận 16/11 qua bản ghi S2/OpenAlex] | Cross-model activation patching để tìm nơi lỗi lượng tử hoá phát sinh; độ lớn residual FP dự báo lỗi | Lân cận; chính là "Chang et al., EMNLP 2025" trong sổ |
| Dự án hackathon "EdgeAlign" (Devpost) | trang Devpost | Pythia-70M, INT8 giả lập trên activation, độ bền mạch | Không phải bài khoa học |

## 5. Bài lân cận mới từ G-N (notebook 96, 16/11/2026)

Nguồn: bản ghi Semantic Scholar/OpenAlex (tiêu đề, tác giả, tóm tắt) trong `results/20261116_gn_tra_cuu/candidates_dedup.jsonl`. **Chỉ đọc tóm tắt**, trừ khi ghi khác. Không bài nào trùng C1, C2, C3b (`GN_TRA_CUU.md` §6).

| Bài | Nội dung (theo tóm tắt) | Khác đề tài ở đâu | Dùng vào đâu |
|---|---|---|---|
| **Varshney, P.** "Cosine Similarity Is Not Evidence: Measuring the Noise Floor of Interpretability Transfer Under Quantization". arXiv 2609.30275 (2026) | Hướng diff-in-means (từ chối) trên Qwen2.5-1.5B-Instruct, chuyển FP → INT8/INT4. Sàn nhiễu split-half của cos phụ thuộc κ = nρ²/d; hai lần ước lượng độc lập đã khớp 0,978–0,994 chỉ do lấy mẫu. So cos FP–Q với null split-half **đo trong model Q**. INT4: hướng xoay vượt nhiễu; INT8: không thấy dịch chuyển, "không phải phát biểu tương đương". Thống kê không phụ thuộc thang đo không tách được dịch chuyển với co giãn | Không DAS hay can thiệp học được; không CausalGym; không tách mã hoá/đọc ra bằng chèn toạ độ; không checkpoint | **Lân cận gần nhất.** Tiền lệ cho null hai phía (D-05), cho việc báo cáo n và sàn nhiễu cùng mọi \|cos\| (trục (c) của C1), và cho tách co biên độ khỏi đổi hướng (D-12, C2). Nên đọc toàn văn trước đề cương |
| **Elluru, Singh, Aguero, Agarwal và cộng sự.** "Mechanistically Interpreting Compression in Vision-Language Models". arXiv 2603.25035 (2026) | Phân tích mạch nhân quả + crosscoder dưới pruning và lượng tử hoá; pruning giữ cấu trúc mạch nhưng xoay/làm yếu feature; lượng tử hoá đổi mạch ở mức cao hơn, feature còn lại khớp hơn | VLM; mạch và patching, không DAS; không cấp biến | Lân cận gần; trích khi nói "đã có công trình đo mạch dưới nén" |
| **Hu, Ramachandran.** "The Structure of Quantization Damage in LLMs: Why the Next Bit Should Be Spent Globally". arXiv 2609.01587 (2026) | 9 model; nâng từng layer lên 8 bit để đo phần phục hồi; tổn hại không nằm ở mạch tác vụ hay thống kê trọng số mà lan toả; 8 bit gần như không mất (RTN, GPTQ, AWQ) | Đo accuracy, không đo biến | Bối cảnh cho C4 và cho việc bỏ C5 (D-02) |
| **Duan, E.** "Do Activation Monitors Survive Model Updates?" arXiv 2606.15980 (2026) | Probe đóng băng trên model gốc phần lớn vẫn dùng được sau lượng tử hoá, hỏng sau fine-tune; QLoRA gây hại dù NF4 một mình ít hại | Probe, không can thiệp nhân quả | Liên quan trục (b) "dùng lại hướng FP trên Q" của C1 |
| **Singh, Sajjad.** "Interpreting the Effects of Quantization on LLMs". IJCNLP-AACL 2025 (`2025.ijcnlp-long.123`); arXiv 2508.16785 [ĐCM trang arXiv qua tìm kiếm] | 4 bit và 8 bit; calibration thay đổi ít; số neuron chết không đổi; đóng góp và độ dư thừa của neuron thay đổi tuỳ model | Cấp neuron, không can thiệp | Trích một câu ở tổng quan |
| **Gupta, Kukreja, Kumar, Mittal và cộng sự.** "When Bigger Becomes Brittle: Why Compression Hurts More as Language Models Scale". arXiv 2611.07891 (2026) | Tách tổn hại khi ablation/nén các đầu attention truy hồi thành phần được mạng bù và phần tới đầu ra; model nhỏ bù nhiều hơn model lớn | Ablation đầu attention, không DAS | Cảnh báo khi diễn giải 410M so với 1B trong C1 |
| **Faumi, Sumanathilaka.** "Mechanistic Failure Modes of Weight Pruning in Transformer Language Models". arXiv 2610.37126 (2026) | GPT-2; pruning theo độ lớn: cắt đầu attention xoá mạch IOI; cắt 30% neuron giữ đủ đầu của mạch nhưng đảo dấu đóng góp; perplexity xếp sai mức hỏng | Pruning, không lượng tử hoá | Sổ §8 có "Faumi & Sumanathilaka, arXiv 2610.37157" (cùng tác giả, [ĐCM] PDF); **chưa đối chiếu** hai mã là hai bài hay một |
| **Tigges, Hanna, Yu, Biderman.** "LLM Circuit Analyses Are Consistent Across Training and Scale". NeurIPS 2024 | Mạch trên Pythia 70M–2.8B qua 300 tỉ token: chức năng xuất hiện ở số token tương tự qua các cỡ; đầu attention có thể đổi nhưng thuật toán giữ | Không lượng tử hoá | Lân cận C3b (nay là phần mở rộng, D-17) |
| **Baligar, Y.** "Float32-Induced Distortion in Activation Patching". Computation 14(9):212 (2026) | Patching cấp tương tác trên GPT-2-medium và Pythia-410M: fp32 tạo sàn sai số; sai số endpoint tăng theo độ dời | Phương pháp luận, không nén | Nhắc khi chọn dtype cho phép đo hiệu nhỏ ở C2 (D-04: FP = fp32) [GỢI Ý] |
| **Khorasani, Salehkaleybar, Kiyavash, Grossglauser.** "Inference Time Causal Probing in LLMs". arXiv 2605.07631 (2026) | Can thiệp không cần probe (HDMI) đánh giá trên CausalGym, Pythia-70M và Llama-3-8B | Không nén | Ví dụ CausalGym vẫn được dùng làm benchmark năm 2026 |
| Gupte, Chhabra, Khalili. arXiv 2507.15977 (2025) | SAE của model gốc vẫn diễn giải được model nén, kém hơn chút | SAE | Trích một câu |
| Zhang và cộng sự. arXiv 2504.02010 (2025) | Diff-of-means + attribution patching trên model suy luận đã nén | Không DAS | Trích một câu |
| PRISM, arXiv 2610.20808 (2026) | Chuyển can thiệp activation qua độ chính xác (nhãn từ bản NF4) | Steering | Trích một câu |
| Asiaee, arXiv 2607.08349 (2026) "Certified Interventional Fidelity" | Khoảng tin cậy và dãy tin cậy cho đánh giá can thiệp | Phương pháp luận | Tuỳ chọn khi viết phần thống kê của SPEC |
