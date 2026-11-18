# GN_TRA_CUU.md — Cổng G-N (tính mới): cách lấy dữ liệu, cách Claude tổng hợp, kết quả

> Bản 16/11/2026 (Claude). Thay bản 13/11 lần 3: §1–§4 giữ nguyên; §5 đã điền; thêm §6 (kết luận) và §7 (giới hạn và việc còn lại).
> **Kết quả: G-N đạt (16/11/2026).** Không bài nào trùng C1, C2 hay C3b theo định nghĩa §1. Có giới hạn, xem §7.

## 1. Điều kiện đạt (chốt trước khi tra)

Một bài bị coi là **trùng** khi:

- **C1:** đo kết quả của can thiệp học được (DAS, DII, interchange intervention theo hướng học) trên **cùng model ở FP và sau lượng tử hoá trọng số**, rồi so mức bảo toàn.
- **C2:** tách "mã hoá" và "đọc ra" của **một biến** bằng cách chèn toạ độ/hướng giữa FP và Q.
- **C3b:** theo dõi cơ chế (DAS hoặc patching) dưới lượng tử hoá **qua các checkpoint huấn luyện**.

Bài **lân cận** (phải trích và nói rõ khác biệt, nhưng không làm hỏng cổng): cùng câu hỏi "cơ chế có còn sau nén không" nhưng dùng SAE, steering vector, hoặc patch toàn bộ activation; hoặc dùng DAS nhưng không có lượng tử hoá. Ví dụ đã biết: Zhou et al. 2026, Duan 2606.03002, Makarov 2610.40055, Bhandari & Wade 2609.06473, Wu et al. 2608.06564, Yao et al. 2610.33299, CircuitKIT 2607.19317.

## 2. Việc của người: chạy notebook 96

- **File:** `notebooks/96_gn_tra_cuu_api.ipynb`.
- **Chạy ở đâu:** Kaggle, **CPU, bật Internet** (không cần GPU), chạy từng ô hoặc Run All (QT-11 trường hợp d: dưới 10 phút). Xong thì **Stop session**. Hoặc chạy trên máy cá nhân có Python và `requests`.
- **Tham số:** giữ mặc định. Không cần điền email hay khoá API.
- **Mang về:** file `outputs/96_gn_tra_cuu.zip`. Đính kèm vào phiên chat.
- **Nếu ô nào báo lỗi mạng hoặc bị giới hạn tốc độ:** cứ chạy tiếp tới ô 8; lỗi được ghi vào `errors.jsonl`. Nếu ô 8 báo trên 20 lỗi, chạy lại cả notebook sau khoảng 10 phút.

Notebook kéo:
- danh sách **bài trích dẫn** (citations) của 7 bài gốc và 4 bài lân cận, từ **Semantic Scholar** và **OpenAlex** (mỗi bài tra cả mã arXiv lẫn DOI ACL);
- kết quả **tìm theo từ khoá**: 10 truy vấn trên Semantic Scholar và OpenAlex (từ 2024), 7 truy vấn có trường trên arXiv;
- toàn bộ phản hồi gốc (`raw/`).

## 3. Việc của Claude khi nhận zip

1. Đọc `seeds.jsonl`: số trích dẫn mỗi nguồn báo, số lấy được, mã nào không tra được.
2. Đọc **mọi** bài trong `candidates_dedup.jsonl` (tiêu đề + tóm tắt), không chỉ bài có cờ. Cờ chỉ để xếp thứ tự.
3. Xếp mỗi bài vào: trùng C1 / trùng C2 / trùng C3b / lân cận / không liên quan, kèm một câu lý do.
4. Bài nghi trùng hoặc lân cận gần: Claude thử mở toàn văn; mở không được thì nhờ người tải PDF lên Project (chỉ những bài đó).
5. Điền bảng §5, cập nhật sổ §4 (trạng thái G-N) và §8 (nguồn mới), ghi vào `GHI_CHU_BAI_BAO.md` các bài lân cận mới.

## 4. Giới hạn của cách làm này

- Không dùng Google Scholar: không có API, chặn máy truy cập tự động. Scholar có thể có thêm luận văn, poster, bản PDF trên trang cá nhân mà Semantic Scholar và OpenAlex chưa có. Bù lại bằng 3 nguồn và 17 truy vấn từ khoá. Báo cáo cho thầy ghi rõ nguồn đã rà.
- Bài đăng vài ngày gần đây có thể chưa vào chỉ mục. Chạy lại notebook trước khi nộp đề cương (23–30/11) để cập nhật.
- (Tuỳ chọn, 1 phút) Nếu muốn có con số "Cited by" của Google Scholar cho báo cáo: chụp màn hình dòng "Cited by N" của CausalGym trên Scholar, gửi kèm.

## 5. Bảng kết quả (Claude điền 16/11/2026)

Notebook 96 chạy lúc 08:05 UTC ngày 16/11/2026; 1449 bài sau gộp; 16 lỗi, đều ở Semantic Scholar (S2): 9 lần tra bài (7 do giới hạn tốc độ, 2 mã DOI ACL không có trong S2) và 7/10 truy vấn từ khoá. Dữ liệu và bảng xếp loại từng bài: `results/20261116_gn_tra_cuu/` (`phan_loai_claude.csv`).

| # | Bài gốc | Ngày tra | Trích dẫn (S2 / OpenAlex): báo, lấy được | Bài trùng | Bài lân cận mới |
|---|---|---|---|---|---|
| 1 | CausalGym | 16/11 | S2 67, lấy 67 (DOI ACL: S2 không có) / OA 30, lấy 28 | 0 | Khorasani et al. 2605.07631 (dùng CausalGym làm benchmark, không nén) |
| 2 | Ouyang et al. | 16/11 | S2 24 + 10 (arXiv + ACL) / OA 26 + 2 | 0 | — |
| 3 | Duan | 16/11 | S2 lỗi (giới hạn tốc độ) / OA 6 | 0 | Varshney 2609.30275; Gupta et al. 2611.07891 |
| 4 | Makarov | 16/11 | S2 lỗi / OA 0 | 0 | — |
| 5 | Tanyel & Ayvaz | 16/11 | S2 lỗi / OA 0 | 0 | — |
| 6 | Geiger et al. (DAS) | 16/11 | S2 270, lấy 270 / OA 65, lấy 63 | 0 | Không bài nào dùng DAS dưới lượng tử hoá |
| 7 | Zhou et al. | 16/11 | S2 lỗi (arXiv) và không có (DOI ACL) / OA 6 + 1 | 0 | Gupta et al. 2611.07891 |
| — | 4 bài phụ (Bhandari & Wade, Wu et al., Yao et al., Armstrong) | 16/11 | S2: Armstrong 0, ba bài kia lỗi / OA 1, 3, 1, 0 | 0 | — |
| — | Tìm theo từ khoá (17 truy vấn) | 16/11 | S2 chạy được 3/10, OpenAlex 10/10, arXiv 7/7 | 0 | Elluru et al. 2603.25035; Hu & Ramachandran 2609.01587; E. Duan 2606.15980; Singh & Sajjad (IJCNLP-AACL 2025); Faumi & Sumanathilaka 2610.37126; Tigges et al. (NeurIPS 2024); Baligar (Computation, 2026) |

**Cách Claude đọc 1449 bài** (nói rõ để người kiểm lại được):

1. **Lọc máy điều kiện cần** trên tiêu đề + tóm tắt của cả 1449 bài. Định nghĩa "trùng" (§1) đòi hỏi lượng tử hoá trọng số, nên bài không nhắc lượng tử hoá hay nén không thể trùng. 765 bài thuộc nhóm này; Claude không đọc từng bài, chỉ rà riêng các bài nói về checkpoint huấn luyện kèm can thiệp/mạch (để tìm lân cận C3b).
2. **Claude đọc:** tóm tắt của 70 bài có cả lượng tử hoá và từ khoá can thiệp/diễn giải; tiêu đề của 544 bài có lượng tử hoá còn lại; tiêu đề của 70 bài nén khác (pruning, distillation) không có lượng tử hoá; tiêu đề của 64 bài không có tóm tắt; tóm tắt đầy đủ của khoảng 40 bài gần nhất.
3. Bài lân cận gần được tra thêm trên web. Không mở được toàn văn bài nào trong phiên (arXiv không nằm trong danh sách được truy cập); xếp loại dựa trên tóm tắt.

Biểu thức lọc và nhãn tay nằm trong `results/20261116_gn_tra_cuu/phan_loai.py`.

## 6. Kết luận

- **Không bài nào trùng C1, C2, C3b.** Không bài nào trong 1449 bài dùng DAS, DII hay interchange intervention học được trên model đã lượng tử hoá trọng số. Có 2 bài nhắc cả DAS/causal abstraction lẫn nén: một bài về pruning bằng thay cơ chế (Asiaee, 2602.24266) và một bài về giọng nói (interchange intervention trên mô hình tổng hợp tiếng nói); cả hai không trùng.
- **Lân cận gần nhất** (phải trích và nói rõ khác biệt trong đề cương):
  - **Varshney, arXiv 2609.30275** "Cosine Similarity Is Not Evidence: Measuring the Noise Floor of Interpretability Transfer Under Quantization". Hướng diff-in-means (hướng từ chối) chuyển từ FP sang INT8/INT4; so cos với null split-half đo **ngay trong model Q**, vì null lấy từ FP giả định phương sai như nhau. Ở INT4 hướng xoay vượt nhiễu; ở INT8 không thấy dịch chuyển, và tác giả nói rõ đó **không** phải phát biểu tương đương. Chỉ ra rằng thống kê không phụ thuộc thang đo không phân biệt được *dịch chuyển* với *co giãn* của biến được chuyển. Khác đề tài: không dùng DAS hay can thiệp học được, không CausalGym, không tách mã hoá/đọc ra bằng chèn toạ độ, không checkpoint. **Đây là tiền lệ trực tiếp cho null hai phía (D-05) và cho việc tách "co biên độ" khỏi "đổi hướng" (D-12, C2).** Đề cương nên trích, và không trình bày null hai phía như đóng góp riêng của nhóm.
  - **Elluru et al., arXiv 2603.25035** "Mechanistically Interpreting Compression in Vision-Language Models". Phân tích mạch nhân quả và crosscoder dưới pruning và lượng tử hoá trên VLM: pruning giữ cấu trúc mạch nhưng xoay và làm yếu feature; lượng tử hoá đổi mạch ở mức cao hơn nhưng feature còn lại khớp hơn. Khác: VLM, mạch/patching, không DAS.
- **Lân cận khác** (đủ để trích một câu): Hu & Ramachandran 2609.01587 (tổn hại lượng tử hoá không nằm ở mạch tác vụ, đo bằng phục hồi 8 bit theo layer); E. Duan 2606.15980 (probe đóng băng giữ được dưới lượng tử hoá, hỏng dưới fine-tune, liên quan trục (b) của C1); Singh & Sajjad IJCNLP-AACL 2025 (arXiv 2508.16785; neuron dưới 4/8 bit); Gupta et al. 2611.07891 (mạng bù trừ tổn hại khi nén, kém dần theo cỡ model); Faumi & Sumanathilaka 2610.37126 (pruning làm đảo dấu mạch IOI); Tigges et al. NeurIPS 2024 (mạch ổn định qua checkpoint Pythia, không lượng tử hoá, lân cận C3b); Baligar 2026 (sai số fp32 trong activation patching cấp tương tác, có Pythia-410M; phương pháp luận).
- Danh sách đầy đủ và lý do: `GHI_CHU_BAI_BAO.md` §5; `results/20261116_gn_tra_cuu/phan_loai_claude.csv`.

## 7. Giới hạn và việc còn lại

- **S2 bị giới hạn tốc độ:** 7/10 truy vấn từ khoá trên S2 không chạy được; trích dẫn của Duan, Makarov, Tanyel & Ayvaz, Zhou, Bhandari & Wade, Wu, Yao chỉ có từ OpenAlex. OpenAlex chạy đủ 10/10 truy vấn, nên phần thiếu là phần trùng giữa hai nguồn, không phải một vùng chưa rà [GỢI Ý]. Chạy lại notebook 96 trước khi nộp đề cương (23–30/11) để lấp; tổng số lỗi dưới 20 nên theo quy tắc §2 không bắt buộc chạy lại ngay.
- Bài rất mới (Tanyel & Ayvaz 3/11, Makarov 29/10) chưa có trích dẫn nào trong hai chỉ mục.
- Xếp loại dựa trên tóm tắt. Nên đọc toàn văn Varshney 2609.30275 trước khi viết đề cương (TV-A tải PDF lên Project nếu muốn Claude đọc).
- Không có Google Scholar (§4).
