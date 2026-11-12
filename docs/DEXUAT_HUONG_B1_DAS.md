# DEXUAT_HUONG_B1_DAS.md — Đề xuất đề tài: bài gốc CausalGym, hướng phát triển "cơ chế nhân quả dưới lượng tử hoá"

> Version: v0.5 · Ngày: 12/11/2026 · Soạn: Claude theo yêu cầu của TV-A Nguyễn Tấn Tài · Nhóm đã duyệt hướng; GVHD **chưa duyệt**.
> Thay đổi so với v0.4: bỏ C5; C3b vào MVP; C3 (LIFO) sang Target; vá thiết kế C1/C2/C3 theo review ngày 12/11; sửa trích dẫn. Quyết định và trạng thái theo dõi trong sổ `KHOALUAN_KE_HOACH_THEO_DOI.md`.
> Quy ước: [ĐCM] đã kiểm chứng · [GỢI Ý] bằng chứng chưa đủ · [PHỎNG ĐOÁN] chưa kiểm. Mọi đóng góp là **đề xuất chưa thử**.

---

## §0. Tóm tắt

**Bài gốc.** Arora, Jurafsky, Potts (2024). *CausalGym: Benchmarking causal interpretability methods on linguistic tasks.* ACL 2024, SAC Award [ĐCM].
- 29 tác vụ cú pháp tiếng Anh; 7 phương pháp 1 chiều trên Pythia 14M–6.9B.
- DAS cho odds cao nhất nhưng không chọn lọc hơn probe từ 160M trở lên.
- Cơ chế hình thành theo giai đoạn, tất cả trước bước 10K.

**Câu hỏi.** Cơ chế mà CausalGym định vị trên model đầy đủ độ chính xác có còn khi lượng tử hoá trọng số sau huấn luyện không? Nếu hỏng, hỏng ở phía mã hoá hay phía đọc ra, và mức hỏng có tăng theo quá trình huấn luyện không?

**Đóng góp:**

| Mã | Nội dung | Phạm vi |
|---|---|---|
| RQ0 | Tái lập CausalGym trên 410M/1B, 4–6 tác vụ, 1 nghiên cứu trường hợp | MVP |
| C1 | Hồ sơ bảo toàn cơ chế: 5 trục đo, null hai phía theo seed, sàn step0, quy tắc ba nhãn đặt trước | MVP |
| C2 | Phân rã mã hoá/đọc ra ở **cấp biến**: chèn toạ độ dọc v giữa FP và Q (thiết kế 2×2); tách theo layer là phân tích phụ; bộ dự báo bậc nhất có baseline từ tài liệu | MVP |
| C3b | QiD ở mức cơ chế: hồ sơ C1 trên các checkpoint Pythia 10K–143K; mức hỏng cơ chế có tăng theo huấn luyện như QiD mức loss (Ouyang et al.) không | MVP |
| C3 | Giả thuyết "vào sau, ra trước" (LIFO), có kiểm soát độ lớn hiệu ứng | Target |
| C4 | So sánh RTN, GPTQ, AWQ, TaCQ: bộ nào giữ hành vi mà không giữ cơ chế | Target |

C5 (bảo vệ có định hướng nhân quả) đã bỏ: CircuitKIT (arXiv 2607.19317, §11.6) đã thử lượng tử hoá hỗn hợp theo độ quan trọng của mạch [ĐCM].

**Tính mới, nói đúng mức.**
- Chưa thấy công trình nào đo cơ chế tìm bằng DAS/interchange intervention dưới lượng tử hoá trên tác vụ cú pháp [GỢI Ý, chờ G-N].
- Lân cận đã có: feature SAE dưới RTN (Duan 2026); hướng refusal (Chhabra & Khalili 2025); vector steering (Bhandari & Wade 2026; Makarov 2026); activation patching cho hai kiểu hỏng (Zhou et al. 2026).
- Null theo seed không phải ý mới; cái mới là áp nó vào DAS dưới lượng tử hoá.
- C3b mới ở chỗ đưa kết quả QiD mức loss (Ouyang et al.; Armstrong 2026) xuống mức cơ chế nhân quả.

---

## §1. Tái lập (RQ0)

Cấu hình của bài gốc [ĐCM]:
- 1D DII ở residual stream sau mỗi layer, tại token cuối mỗi vùng template.
- 1 epoch, batch 4 (100 bước), Adam, lr 5·10⁻³, linear warmup 10%.
- Khoảng 400 câu train và 100 câu test mỗi tác vụ.

Nhóm tái lập:
1. Odds và selectivity của 5 phương pháp (DAS, probe, diff-in-means, PCA, ngẫu nhiên) trên 4–6 tác vụ, Pythia-410M và 1B, ở **fp32**.
2. Một nghiên cứu trường hợp (filler-gap hoặc NPI) trên checkpoint Pythia-1B, dày ở 1K–10K.

Tiêu chí G1: đúng thứ tự phương pháp; đúng thứ tự xuất hiện vị trí; odds cùng bậc.

---

## §2. C1 — Hồ sơ bảo toàn cơ chế

### 2.1 Trục đo (FP = gốc fp32; Q = lượng tử hoá giả lập)

| Trục | Phép đo | Ghi chú |
|---|---|---|
| (a) Hành vi | Logit difference từng câu (chính); accuracy, KL (phụ) | Không dùng ngưỡng accuracy cố định |
| (b) Dùng lại | Odds/IIA khi áp hướng FP vào Q; tỉ lệ chuyển giao T | Không cần học lại; trục chính |
| (b') Học lại | Odds/IIA khi học lại DAS trên Q | Chỉ có nghĩa khi vượt sàn step0 và tác vụ đối chứng |
| (c) Hình học | \|cos\| giữa hướng FP và hướng Q | Chỉ dùng nếu \|cos\| giữa seed FP ≥ 0.9 (quy tắc G0) |
| (d) Bản đồ | Spearman giữa bản đồ odds layer × vị trí của FP và của Q, tính bằng hướng dùng lại | Rẻ |
| (e) Chọn lọc | Selectivity với tác vụ đối chứng của CausalGym | Theo Hewitt & Liang |

Phụ (Target): xoá hướng bằng LEACE; độ lệch phân phối của can thiệp (EMD, Grant et al. ICLR 2026).

### 2.2 Mức nén

- RTN bất đối xứng theo nhóm (g = 128) trên 4 ma trận Linear mỗi khối; embedding, lm head, LayerNorm giữ FP.
- **Nút vặn liên tục** W(α) = W + α·(Q(W) − W), α ∈ [0, 1].
- Lưới bit/α chốt sau pilot G0, chọn 3–4 mức trong vùng chuyển tiếp.
- GPTQ (GPT-QModel hoặc tự cài dạng giả lập) ở 4/3 bit.

Lý do: Armstrong (2026) thấy INT4 theo nhóm trên Pythia-160m cuối huấn luyện đã làm perplexity tăng tới 517%, còn INT8 dưới 1% [ĐCM]. Nên một lưới bit cố định dễ chỉ cho hai cực.

### 2.3 Null và sàn

- **Null hai phía:** học DAS k seed (k = 5 sơ bộ) trên FP và trên Q ở các ô chính. So khoảng cách giữa model với khoảng cách trong model bằng kiểm định hoán vị, lấy lần học làm đơn vị. Báo cáo độ rộng null như một kết quả.
- **Sàn:** DAS trên Pythia step0 và trên tác vụ đối chứng, cùng ô.

### 2.4 Quy tắc kết luận (đặt trước khi chạy)

Mỗi trục cho một trong ba nhãn: **Tương đương** (khoảng tin cậy 90% của chênh lệch nằm trong biên tương đương), **Khác** (khoảng tin cậy 95% không chứa 0 và vượt biên), **Chưa kết luận**. Biên tương đương lấy từ null theo seed (với (b)(c)(d)) và từ dao động bootstrap của FP (với (a)). Mẫu cách làm: Bhandari & Wade (2026), Makarov (2026).

Cây quyết định cho mỗi ô (tác vụ × layer × vị trí × mức nén):
1. (a) Tương đương và (b) Tương đương → **Bảo toàn**.
2. (a) Tương đương, (b) Khác → **Trôi cơ chế**. Nếu thêm (b') Tương đương và vượt sàn → ghi chú phụ "**mã hoá lại**".
3. (a) Khác, (b) Tương đương → **Hành vi hỏng, cơ chế còn**.
4. (a) Khác, (b) Khác → **Sụp cùng nhau**.
5. Còn lại → **Chưa kết luận**.

Hiệu chỉnh nhiều so sánh: Benjamini–Hochberg trên các ô. Tổng hợp qua tác vụ: mô hình hiệu ứng hỗn hợp. Mọi ngưỡng chốt trong SPEC trước khi chạy.

---

## §3. C2 — Phân rã mã hoá/đọc ra

### 3.1 Thiết kế chính ở cấp biến (2×2)

Với hướng v ở layer ℓ, xét hai thừa số:
- **Giá trị** z = v·h, lấy từ FP hay từ Q;
- **Phần sau ℓ**, chạy bằng FP hay bằng Q.

Cách làm: chạy FP tới ℓ, thay toạ độ z bằng z của Q (cùng câu), đi tiếp bằng FP; và ngược lại. Như vậy tách được hỏng do **biến bị mã hoá sai** với hỏng do **biến bị đọc sai**. Đây là cross-model activation patching (Chang et al., EMNLP 2025) thu hẹp về một toạ độ.

### 3.2 Phân tích phụ: tách theo layer

Q-trước (lượng tử hoá layer ≤ ℓ), Q-sau (layer > ℓ), Q-toàn bộ.
- Tương tác được coi là mặc định, vì lỗi mới của mỗi layer triệt tiêu một phần lỗi kế thừa (Chen et al., arXiv 2609.11716) [ĐCM]. Đặt trước cách đọc dấu và độ lớn của hệ số tương tác.
- Với GPTQ, phải hiệu chỉnh lại cho từng cấu hình tách. Chỉ RTN mới "gần như không tốn thêm".

### 3.3 Bộ dự báo bậc nhất (phụ)

Δodds ≈ (độ nhạy đầu ra theo z) × (chênh z giữa hai lớp). So với các baseline:
- sai số tái tạo hidden state, CKA, perplexity;
- **độ lớn residual của FP** (Chang et al. 2025);
- **activation đỉnh của FP** (Duan 2026).

Báo cáo rõ vùng mà xấp xỉ bậc nhất còn đúng.

---

## §4. C3b — QiD ở mức cơ chế qua checkpoint (MVP)

**Cơ sở [ĐCM]:**
- Ouyang et al. (ACL 2025): QiD mức loss tăng theo số token đã huấn luyện, trên checkpoint Pythia.
- Armstrong (2026): khoảng cách INT4 của Pythia-160m bùng nổ sau khi perplexity FP32 hội tụ (khoảng 77K bước).
- Catalan-Tatjer et al. (ICLR 2026): động lực learning rate quyết định độ bền PTQ.

**Thiết kế:**
1. Checkpoint Pythia-410M (và 1B nếu đủ GPU): khoảng 10K, 30K, 60K, 77K, 110K, 143K.
2. Ở mỗi checkpoint: tìm DAS trên FP, rồi đo hồ sơ C1 ở cùng mức nén (một α ở vùng chuyển tiếp và một mức bit).
3. Đại lượng chính: QiD_mech(t) = 1 − T(t), với T là tỉ lệ chuyển giao (b). So với QiD_loss(t) và QiD hành vi (a).
4. Có thể dùng checkpoint GPTQ công khai của Ouyang et al. (Pythia **deduped**) nếu GVHD đồng ý. Khi đó phải chạy cả FP deduped.

**Cách đọc:**

| Kết quả | Ý nghĩa |
|---|---|
| QiD_mech tăng theo t, cùng dạng QiD_loss | Giải thích ở cấp cơ chế cho Ouyang/Armstrong |
| QiD_mech tăng sớm hơn QiD hành vi | Cơ chế tổn thương trước khi hành vi lộ ra; có giá trị cảnh báo |
| QiD_mech không đổi dù QiD_loss tăng | Cơ chế cú pháp bền; tổn thương nằm ở phần khác của model |
| Không đơn điệu | Báo cáo hình dạng; đối chiếu với các pha của Armstrong |

**Giới hạn:** trên Pythia, số token và learning rate đi cùng nhau, nên không tách được hai nguyên nhân.

---

## §5. Target

- **C3 LIFO:** t_form = checkpoint đầu tiên mà odds vượt sàn step0. b_lose được định nghĩa tương đối (mức α làm odds còn 50% odds FP của chính ô đó). Dùng tương quan riêng phần, kiểm soát odds FP; thêm đối chứng nhiễu Gauss cùng chuẩn sai số; mô hình hiệu ứng hỗn hợp thay cho Spearman trên vài vị trí.
- **C4:** RTN, GPTQ, AWQ (nếu thư viện còn hỗ trợ GPT-NeoX), TaCQ (COLM 2025).

---

## §6. Phương pháp lấy từ đâu

| Thành phần | Nguồn |
|---|---|
| DAS, DII | Geiger, Wu et al. (CLeaR 2024); pyvene (NAACL 2024 Demo) |
| Tác vụ, odds, selectivity, checkpoint | CausalGym (ACL 2024); Pythia (ICML 2023); Hewitt & Liang (EMNLP 2019) |
| Giới hạn của DAS | Makelov, Lange, Geiger, Nanda (ICLR 2024); Wu et al. (2024, phản hồi); Sutter et al. (NeurIPS 2025); Kumon & Yanaka (ACL 2026) |
| Độ lệch của can thiệp | Grant et al. (ICLR 2026, Oral) |
| Kiểm định tương đương, quy tắc ba nhãn | Bhandari & Wade (2026); Makarov (arXiv 2610.40055) |
| Cross-model patching, dự báo lỗi | Chang et al. (EMNLP 2025); Duan (arXiv 2606.03002) |
| Lan truyền lỗi lượng tử hoá | Chen et al. (arXiv 2609.11716); Zhou et al. (Findings ACL 2026) |
| Lượng tử hoá × huấn luyện | Ouyang et al. (ACL 2025); Armstrong (arXiv 2604.15167); Catalan-Tatjer et al. (ICLR 2026); Kumar et al. (ICLR 2025) |
| Nén × cơ chế (liên quan) | Faumi & Sumanathilaka (arXiv 2610.37157, distillation); Chhabra & Khalili (2025); CircuitKIT (arXiv 2607.19317) |
| Lượng tử hoá | RTN; GPTQ (ICLR 2023) qua GPT-QModel; AWQ (MLSys 2024); TaCQ (COLM 2025) |
| Thống kê | Bootstrap ghép cặp; TOST; Benjamini–Hochberg; mô hình hiệu ứng hỗn hợp |

---

## §7. Phạm vi, cổng, tính toán

| | MVP | Target |
|---|---|---|
| RQ0 | 4–6 tác vụ, 410M/1B, 5 phương pháp; 1 nghiên cứu trường hợp | 2 nghiên cứu trường hợp |
| C1 | Đủ trục (a)–(e); null hai phía ở ô chính; RTN theo α + 2 mức bit; GPTQ 4 bit | + LEACE, EMD, GPTQ 3 bit |
| C2 | 2×2 cấp biến ở 2–3 ô chính; tách layer với RTN | Toàn bộ layer; GPTQ tách đoạn |
| C3b | 410M, 6 checkpoint, 1–2 tác vụ | + 1B |
| C3, C4 | — | Nếu còn thời gian |

Cổng: G-N 17/11/2026 · G0 22/11/2026 · G1 31/12/2026 (có thể dời 15/01/2027) · G2 28/02/2027 · G3 (C3b) 31/03/2027. Chi tiết và quy tắc G0 nằm trong sổ dự án.

**Tính toán [PHỎNG ĐOÁN, đo lại ở G0]:**
- Đơn vị đếm là một lần học DAS (100 bước) cộng đánh giá.
- MVP khoảng 3.000 lần nếu chỉ học lại ở ô chính; khoảng 10.000 lần nếu quét hết.
- Với t = 20–60 giây trên T4: 17–50 giờ GPU (có chọn lọc) hoặc 55–170 giờ (quét hết).
- Kaggle khoảng 30 giờ/tuần mỗi tài khoản; hai tài khoản chạy song song hai phần việc.

---

## §8. Rủi ro

| Mã | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| R1 | Ôm quá nhiều | Cao | MVP cố định; Target chỉ sau G3 |
| R2 | Không tái lập được | Trung bình | G1 trước mọi phát triển; đối chiếu repo gốc |
| R3 | Bị công bố trước | Trung bình | G-N; ba đóng góp độc lập |
| R4 | Null rộng, không phát hiện được gì | Trung bình | Báo cáo độ bất ổn của DAS là kết quả; tăng k |
| R5 | Lưới nén chỉ cho hai cực | Trung bình | Nút α; pilot G0 |
| R6 | DAS học lại vô nghĩa vì sàn cao | Trung bình | Trục (b) dùng lại là trục chính |
| R7 | Lệch phiên bản thư viện; GPTQ cho GPT-NeoX | Trung bình | Tự cài 1D DII; lượng tử hoá giả lập; ghim phiên bản |
| R8 | Quota Kaggle giảm | Trung bình | Ưu tiên 410M; ghi nhật ký GPU |
| R9 | Kết quả ở ≤ 1B không chuyển sang model lớn | Chắc chắn là giới hạn | Ghi vào phạm vi |

**Giới hạn ghi vào đề cương:**
- chỉ lượng tử hoá trọng số sau huấn luyện, dạng giả lập;
- chỉ tác vụ template tiếng Anh, chỉ họ Pythia;
- IIA/odds cao chỉ chứng minh có không gian con tuyến tính đủ để chuyển hành vi;
- trên Pythia không tách được số token và learning rate.

---

## §9. Việc trước khi chốt

1. G0: chạy `notebooks/00_g0_pilot.ipynb` qua Kaggle runner (smoke test → 410M đầy đủ → đo thời gian 1B). Quy trình trong `docs/QUY_TRINH_LAM_VIEC.md`.
2. Đối chiếu repo gốc: BOS, tách token theo vùng, hàm loss, công thức odds.
3. G-N: "Cited by" của CausalGym, Ouyang et al., Duan, Makarov; tìm "quantization causal abstraction", "quantized distributed alignment search".
4. Gửi thầy §0 và 5 câu hỏi (sổ dự án §7).

## Changelog
- v0.5 (12/11/2026): bỏ C5; C3b vào MVP; C3 sang Target; C1 dùng ba nhãn, null hai phía, sàn step0, nút α; C2 chuyển sang thiết kế 2×2 cấp biến; sửa trích dẫn (Zhou → Findings ACL 2026; Grant → ICLR 2026 Oral; TaCQ → COLM 2025; Makelov 4 tác giả; thêm Makarov, Faumi & Sumanathilaka, Duan, Chang, Chen, Armstrong, Catalan-Tatjer, CircuitKIT).
- v0.4 (12/11/2026): 3 đóng góp chính + 2 mở rộng.
- v0.3, v0.2, v0.1 (12/11/2026): xem bản cũ.
