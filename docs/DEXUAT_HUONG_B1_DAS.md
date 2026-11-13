# DEXUAT_HUONG_B1_DAS.md — Đề xuất đề tài: bài gốc CausalGym, hướng phát triển "cơ chế nhân quả dưới lượng tử hoá"

> Version: v0.6 · Ngày: 13/11/2026 · Soạn: Claude theo yêu cầu của TV-A Nguyễn Tấn Tài · Nhóm đã duyệt hướng; GVHD **chưa duyệt**.
> Thay đổi so với v0.5: G0 đã chạy và đạt; dự toán tính toán theo t đo được; RQ0 cụ thể hoá (4 tác vụ, split test, vanilla, vị trí source, tiêu chí G1 định lượng); C1 bỏ "ô chính", đo theo layer, chuẩn hoá T theo mức co biên độ; lưới nén chốt; C2 chạy 2×2 ở mọi layer; C3b thêm tiên nghiệm từ Yao et al.; thêm nguồn và rủi ro. Quyết định và trạng thái theo dõi trong sổ `KHOALUAN_KE_HOACH_THEO_DOI.md` (v0.4: D-11 đến D-14).
> Quy ước: [ĐCM] đã kiểm chứng · [GỢI Ý] bằng chứng chưa đủ · [PHỎNG ĐOÁN] chưa kiểm. Mọi đóng góp là **đề xuất chưa thử**, trừ các số G0 ghi rõ nguồn.

---

## §0. Tóm tắt

**Bài gốc.** Arora, Jurafsky, Potts (2024). *CausalGym: Benchmarking causal interpretability methods on linguistic tasks.* ACL 2024, SAC Award [ĐCM].
- 29 tác vụ cú pháp tiếng Anh; 7 phương pháp 1 chiều trên Pythia 14M–6.9B.
- DAS cho odds cao nhất nhưng không chọn lọc hơn probe từ 160M trở lên.
- Cơ chế hình thành theo giai đoạn, tất cả trước bước 10K.

**Câu hỏi.** Cơ chế mà CausalGym định vị trên model đầy đủ độ chính xác có còn khi lượng tử hoá trọng số sau huấn luyện không? Nếu hỏng, hỏng ở phía mã hoá hay phía đọc ra, ở layer nào, và mức hỏng có tăng theo quá trình huấn luyện không?

**Đóng góp:**

| Mã | Nội dung | Phạm vi |
|---|---|---|
| RQ0 | Tái lập CausalGym trên 410M/1B, 4 tác vụ, 9 phương pháp (kể cả vanilla), có đối chứng dog-give; 1 nghiên cứu trường hợp | MVP |
| C1 | Hồ sơ bảo toàn cơ chế **theo layer**: 5 trục đo, T chuẩn hoá theo mức co biên độ, null hai phía theo seed, sàn step0, quy tắc ba nhãn đặt trước | MVP |
| C2 | Phân rã mã hoá/đọc ra ở **cấp biến**: chèn toạ độ dọc v giữa FP và Q (thiết kế 2×2) ở mọi layer; tách theo layer là phân tích phụ; bộ dự báo bậc nhất có baseline | MVP |
| C3b | QiD ở mức cơ chế: hồ sơ C1 trên các checkpoint Pythia 10K–143K; mức hỏng cơ chế có tăng theo huấn luyện như QiD mức loss (Ouyang et al.) không | MVP |
| C3 | Giả thuyết "vào sau, ra trước" (LIFO), có kiểm soát độ lớn hiệu ứng | Target |
| C4 | So sánh RTN, GPTQ, AWQ, TaCQ: bộ nào giữ hành vi mà không giữ cơ chế | Target |

C5 (bảo vệ có định hướng nhân quả) đã bỏ: CircuitKIT (arXiv 2607.19317, §11.6) đã thử lượng tử hoá hỗn hợp theo độ quan trọng của mạch [ĐCM].

**Tính mới, nói đúng mức.**
- Chưa thấy công trình nào đo cơ chế tìm bằng DAS/interchange intervention dưới lượng tử hoá trên tác vụ cú pháp [GỢI Ý, chờ G-N].
- Lân cận đã có:
  - feature SAE dưới RTN (Duan 2026; repo quant-lens trên GPT-2);
  - hướng refusal (Chhabra & Khalili 2025);
  - vector steering dưới INT8/NF4 (Bhandari & Wade 2026; Makarov 2026);
  - activation patching cho hai kiểu hỏng 4 bit/2 bit (Zhou et al. 2026);
  - co biên độ quyết định dưới lượng tử hoá, chỉ đo ở đầu ra (Wu et al. 2026);
  - phần DAS vượt vanilla trên CausalGym do hàm mục tiêu, không về nén (Tanyel & Ayvaz 2026);
  - mạch agreement của Pythia thưa dần qua huấn luyện, chỉ trên FP (Yao et al., EMNLP 2026).
- Null theo seed không phải ý mới; cái mới là áp nó vào DAS dưới lượng tử hoá.
- C3b mới ở chỗ đưa kết quả QiD mức loss (Ouyang et al.; Armstrong 2026) xuống mức cơ chế nhân quả.

**Số G0 đã có** (410M, `agr_sv_num_subj-relc`; sổ §9) [ĐCM cho tác vụ này]:
- t = 6,41 s cho một lần học DAS + đánh giá.
- Odds kiểu bài gốc 5,24 so với 4,97 của bài; accuracy 0,97 bằng bài.
- T tương quan 0,997 với tỉ lệ logit diff Q/FP qua 9 cấu hình nén (lý do của §2.1).

---

## §1. Tái lập (RQ0)

Cấu hình của bài gốc [ĐCM, đối chiếu code ở sổ §8]:
- 1D DII ở residual stream sau mỗi layer, tại token cuối mỗi vùng template.
- 1 epoch, batch 4 (100 bước), Adam, lr 5·10⁻³, linear warmup 10%.
- 400 cặp train (200 cặp + cặp đảo) và 100 cặp eval (50 + cặp đảo) mỗi tác vụ; eval là tập seed 1 (split `test` của HF).

Nhóm tái lập (D-13; notebook `01_tai_lap_causalgym.ipynb`):
1. **Tác vụ:** `agr_sv_num_subj-relc`, `npi_any_subj-relc`, `filler_gap_subj`, `cleft`.
   - 4 họ hiện tượng; gồm 2 tác vụ nghiên cứu trường hợp của bài (§6).
   - Accuracy trong bài ≥ 0,89 ở cả 410m và 1b.
   - `agr_sv_num_subj-relc` là tác vụ phát triển (đã nhìn dữ liệu ở G0).
2. **Model:** Pythia-410M và 1B, fp32 (bài chạy 1b ở bfloat16).
3. **Phương pháp:** DAS, probe (2 mức L2), diff-in-means, PCA, k-means, LDA, ngẫu nhiên, và vanilla (thay cả vector). Odds và selectivity với tác vụ đối chứng dog-give, tổng hợp đúng như `plot.py`.
4. **Chỗ cố ý khác code gốc:** lấy biểu diễn source ở vị trí của source. Code gốc lấy ở vị trí của base (sổ §8 điểm 9; cũng được Tanyel & Ayvaz chỉ ra). Nếu số lệch bài, chạy thêm chế độ `repo` để biết lệch do đâu.
5. **Một nghiên cứu trường hợp** (`npi_any_subj-relc` hoặc `filler_gap_subj`) trên checkpoint Pythia-1B, dày ở 1K–10K. Làm sau G1, dùng chung hạ tầng với C3b.

**Tiêu chí G1** (sổ §4, chốt trước khi chạy), xét riêng cho mỗi model, phải đạt cả ba:
- **Thứ tự phương pháp:** Kendall τ_b ≥ 0,7 giữa odds trung bình 4 tác vụ của nhóm và của bài (9 phương pháp); DAS đứng đầu.
- **Thứ tự vị trí** (tiêu chí tối thiểu): layer xuất hiện của vùng khác nhau đầu tiên ≤ layer xuất hiện của vùng cuối ở ≥ 3/4 tác vụ.
- **Cùng bậc:** ≥ 12/16 cặp (tác vụ × {DAS, probe tốt hơn, diff-in-means, vanilla}) có tỉ lệ nhóm/bài trong [0,5; 2].

**Ghi thêm từ G0 và Tanyel & Ayvaz:** DAS có thể vượt "trần tráo trung thực". Ở G0b, odds DAS gần đầu ra là 7,33–8,70, lớn hơn 2 × logit diff = 6,59 [ĐCM]. Vì vậy RQ0 báo cáo DAS cạnh vanilla, và C1 không dựa riêng vào độ lớn odds của DAS.

---

## §2. C1 — Hồ sơ bảo toàn cơ chế

### 2.1 Trục đo (FP = gốc fp32; Q = lượng tử hoá giả lập)

| Trục | Phép đo | Ghi chú |
|---|---|---|
| (a) Hành vi | Logit difference từng câu (chính); accuracy, KL (phụ); R = logit diff Q / FP | Không dùng ngưỡng accuracy cố định |
| (b) Dùng lại | Odds khi áp hướng FP vào Q; **T_rel = T / R** (chính), T thô và c của Wu et al. (phụ) | Không cần học lại; trục chính. Chỉ tính T_rel khi R đủ xa 0 (ngưỡng chốt trong SPEC) |
| (b') Học lại | Odds khi học lại DAS trên Q, chia odds FP | Chỉ có nghĩa khi vượt sàn step0 và tác vụ đối chứng |
| (c) Hình học | \|cos\| giữa hướng FP và hướng Q, so với \|cos\| giữa seed | Chỉ dùng ở layer có \|cos\| giữa seed FP ≥ 0,9 (quy tắc G0 số 4, áp theo layer) |
| (d) Bản đồ | Spearman giữa bản đồ odds của FP và Q (hướng dùng lại), trên ô có hiệu ứng | Rẻ; kém nhạy ở 3–4 bit (G0b: 0,97–1,00) |
| (e) Chọn lọc | Selectivity với tác vụ đối chứng dog-give | Theo Hewitt & Liang |

**Vì sao phải chuẩn hoá T (D-12).** Wu et al. (2026) thấy lượng tử hoá **nhân** biên quyết định với một hệ số co. Nếu đầu ra chỉ co lại, odds của mọi can thiệp cũng co theo, nên T giảm dù không gian con không đổi. G0b xác nhận điều này cho tác vụ phát triển:
- tương quan giữa T (trung vị theo ô) và R là 0,997 qua 9 cấu hình;
- ở 3–4 bit, T/R nằm trong 0,93–1,00.

Mẫu số chính là R vì khoảng tin cậy hẹp. Độ dốc c của Wu et al. nhiễu hơn (3 bit: R 0,75 [0,68; 0,80], c 0,77 [0,45; 1,10]).

**Giới hạn:** T_rel ≈ 1 nghĩa là hướng vẫn điều khiển cùng tỉ lệ của biên quyết định. Nó không phân biệt "đầu ra co lại" với "biến bị mã hoá yếu đi"; phần đó do C2 tách.

**Quan sát sơ bộ cần kiểm** [GỢI Ý, G0b, 1 tác vụ]: ở 2 bit (cấu hình nội suy α0,25 và α0,5), hướng ở layer giữa của vùng cuối giữ T cao hơn R rõ rệt (T/R tới 1,5–2,0). Ở 3–4 bit thì T ≈ R. Nếu lặp lại trên các tác vụ khác, đây là một dạng "hành vi hỏng, cơ chế còn", khớp với hai kiểu hỏng của Zhou et al.

### 2.2 Mức nén

- RTN bất đối xứng theo nhóm (g = 128) trên 4 ma trận Linear mỗi khối; embedding, lm head, LayerNorm giữ FP.
- **Lưới chốt sau G0b** (quy tắc G0 số 2): 4 bit, 3 bit, 2 bit α0,5, 2 bit α0,75. Accuracy giảm 0,97 → 0,79 → 0,64 → 0,52 [ĐCM cho tác vụ phát triển]. 8 bit giữ làm mức kiểm tra.
  - Ưu tiên mức bit thật (α = 1); chỉ dùng α ở dải không có mức bit nào.
  - 2 bit α1,0 không đơn điệu (0,62), không dùng.
  - Tác vụ khác có thể cần lưới khác. Quy tắc chọn giữ nguyên, áp lại trên dữ liệu FP và hành vi của từng tác vụ trước khi đo cơ chế.
- GPTQ (GPT-QModel hoặc tự cài dạng giả lập) ở 4/3 bit.

Lý do có nút α: Armstrong (2026) thấy INT4 theo nhóm trên Pythia-160m cuối huấn luyện đã làm perplexity tăng tới 517%, còn INT8 dưới 1% [ĐCM]. Một lưới bit cố định dễ chỉ cho hai cực. G0 xác nhận: 8/6/4 bit và mọi α ở 4 bit đều giữ accuracy 0,97.

### 2.3 Phạm vi đo, null và sàn (D-11)

- **Không chọn một ô chính.** Đo ở **mọi layer** của hai vùng: vùng khác nhau đầu tiên và vùng cuối (vị trí dự đoán).
  - Lý do: quy tắc chọn ô D-08 đã rơi vào L22 ở G0b, sát đầu ra; T khác rõ giữa các layer.
  - Ô ở các vùng còn lại chỉ đo trục rẻ (b) và (d).
- **Null hai phía:** học DAS k seed (k = 5) trên FP và trên Q ở mỗi layer nói trên.
  - So khoảng cách giữa model với khoảng cách trong model bằng kiểm định hoán vị, lấy lần học làm đơn vị.
  - Báo cáo độ rộng null như một kết quả. G0 cho thấy độ rộng phụ thuộc ô: \|cos\| min 0,891 ở L0/vùng 1, 0,967 ở L22/vùng 5.
- **Sàn:** DAS trên Pythia step0 và trên tác vụ đối chứng, cùng ô.

### 2.4 Quy tắc kết luận (đặt trước khi chạy)

Mỗi trục cho một trong ba nhãn, ở mỗi (tác vụ, layer, vùng, mức nén):
- **Tương đương:** khoảng tin cậy 90% của chênh lệch nằm trong biên tương đương;
- **Khác:** khoảng tin cậy 95% không chứa 0 và vượt biên;
- **Chưa kết luận:** còn lại.

Biên tương đương lấy từ null theo seed (với (b)(c)(d)) và từ dao động bootstrap của FP (với (a)). Mẫu cách làm: Bhandari & Wade (2026), Makarov (2026).

Cây quyết định, dùng (b) = T_rel:
1. (a) Tương đương và (b) Tương đương → **Bảo toàn**.
2. (a) Tương đương, (b) Khác → **Trôi cơ chế**. Nếu thêm (b') Tương đương và vượt sàn → ghi chú phụ "**mã hoá lại**".
3. (a) Khác, (b) Tương đương → **Hành vi hỏng, cơ chế còn**.
4. (a) Khác, (b) Khác → **Sụp cùng nhau**.
5. Còn lại → **Chưa kết luận**.

Hiệu chỉnh nhiều so sánh: Benjamini–Hochberg trên các layer của mỗi tác vụ. Tổng hợp qua tác vụ: mô hình hiệu ứng hỗn hợp. Mọi ngưỡng (biên tương đương, ngưỡng R cho T_rel) chốt trong SPEC C1 trước khi chạy notebook 02.

---

## §3. C2 — Phân rã mã hoá/đọc ra

### 3.1 Thiết kế chính ở cấp biến (2×2)

Với hướng v ở layer ℓ, xét hai thừa số:
- **Giá trị** z = v·h, lấy từ FP hay từ Q;
- **Phần sau ℓ**, chạy bằng FP hay bằng Q.

Cách làm: chạy FP tới ℓ, thay toạ độ z bằng z của Q (cùng câu), đi tiếp bằng FP; và ngược lại. Như vậy tách được hỏng do **biến bị mã hoá sai** với hỏng do **biến bị đọc sai**. Đây là cross-model activation patching (Chang et al., EMNLP 2025) thu hẹp về một toạ độ.

**Chạy ở mọi layer của vùng cuối** (D-11). Thiết kế 2×2 không cần học thêm, chỉ cần đánh giá, nên rẻ. Lợi thế: thấy được điểm mà phần hỏng chuyển từ phía mã hoá sang phía đọc ra, thay vì một con số ở một ô. G0b cho thấy tách ở một ô sát đầu ra là suy biến (phía sau chỉ còn 1 khối).

### 3.2 Phân tích phụ: tách theo layer

Q-trước (lượng tử hoá layer ≤ ℓ), Q-sau (layer > ℓ), Q-toàn bộ, ở cùng các layer.
- Tương tác được coi là mặc định, vì lỗi mới của mỗi layer triệt tiêu một phần lỗi kế thừa (Chen et al., arXiv 2609.11716) [ĐCM]. Đặt trước cách đọc dấu và độ lớn của hệ số tương tác. G0b ở L22: gần cộng tính (3 bit: 1 − 0,74 cộng 1 − 0,95 ≈ 1 − 0,69).
- Với GPTQ, phải hiệu chỉnh lại cho từng cấu hình tách. Chỉ RTN mới "gần như không tốn thêm".

### 3.3 Bộ dự báo bậc nhất (phụ)

Δodds ≈ (độ nhạy đầu ra theo z) × (chênh z giữa hai lớp). Dạng này khớp với cách Tanyel & Ayvaz tách hiệu ứng can thiệp thành độ lệch trạng thái nhân gradient đọc ra (chưa đọc toàn văn để đối chiếu chi tiết).

So với các baseline:
- sai số tái tạo hidden state, CKA, perplexity;
- **độ lớn residual của FP** (Chang et al. 2025);
- **activation đỉnh của FP** (Duan 2026);
- **R** (mức co biên độ hành vi, Wu et al. 2026).

Báo cáo rõ vùng mà xấp xỉ bậc nhất còn đúng.

---

## §4. C3b — QiD ở mức cơ chế qua checkpoint (MVP)

**Cơ sở [ĐCM]:**
- Ouyang et al. (ACL 2025): QiD mức loss tăng theo số token đã huấn luyện, trên checkpoint Pythia.
- Armstrong (2026): khoảng cách INT4 của Pythia-160m bùng nổ sau khi perplexity FP32 hội tụ (khoảng 77K bước).
- Catalan-Tatjer et al. (ICLR 2026): động lực learning rate quyết định độ bền PTQ.
- **Yao et al. (EMNLP 2026):** mạch subject–verb agreement của pythia-1b và 10 seed pythia-410m được học sớm và ban đầu phân tán. Sau khi hành vi ổn định, mạch vẫn tổ chức lại và thu nhỏ; mạch cuối của 1b rất thưa.

**Giả thuyết tiên nghiệm (đặt trước, [GỢI Ý]):** mạch thưa dần làm mất dư thừa, nên cùng một mức nén sẽ làm hỏng cơ chế nhiều hơn ở checkpoint muộn. Dự báo: QiD_mech(t) tăng ở pha sau khi accuracy đã bão hoà, cùng chiều với QiD_loss. Nếu QiD_mech không tăng, đó là bằng chứng chống lại cách giải thích bằng độ thưa của mạch.

**Thiết kế:**
1. Checkpoint Pythia-410M (và 1B nếu đủ GPU): khoảng 10K, 30K, 60K, 77K, 110K, 143K.
2. Ở mỗi checkpoint: tìm DAS trên FP, rồi đo hồ sơ C1 (theo layer, §2.3) ở cùng mức nén: một α ở vùng chuyển tiếp và một mức bit.
3. Đại lượng chính: QiD_mech(t) = 1 − T_rel(t). So với QiD_loss(t) và QiD hành vi 1 − R(t).
4. Có thể dùng checkpoint GPTQ công khai của Ouyang et al. (Pythia **deduped**, HF `Xu-Ouyang`) nếu GVHD đồng ý. Khi đó phải chạy cả FP deduped; CausalGym và Yao et al. dùng Pythia thường.

**Cách đọc:**

| Kết quả | Ý nghĩa |
|---|---|
| QiD_mech tăng theo t, cùng dạng QiD_loss | Giải thích ở cấp cơ chế cho Ouyang/Armstrong |
| QiD_mech tăng sớm hơn QiD hành vi | Cơ chế tổn thương trước khi hành vi lộ ra; có giá trị cảnh báo |
| QiD_mech không đổi dù QiD_loss tăng | Cơ chế cú pháp bền; tổn thương nằm ở phần khác của model |
| Không đơn điệu | Báo cáo hình dạng; đối chiếu với các pha của Armstrong và Yao et al. |

**Giới hạn:** trên Pythia, số token và learning rate đi cùng nhau, nên không tách được hai nguyên nhân.

---

## §5. Target

- **C3 LIFO:**
  - t_form = checkpoint đầu tiên mà odds vượt sàn step0;
  - b_lose định nghĩa tương đối: mức α làm T_rel còn 50% ở chính ô đó;
  - dùng tương quan riêng phần, kiểm soát odds FP; thêm đối chứng nhiễu Gauss cùng chuẩn sai số;
  - mô hình hiệu ứng hỗn hợp thay cho Spearman trên vài vị trí.
- **C4:** RTN, GPTQ, AWQ (nếu thư viện còn hỗ trợ GPT-NeoX), TaCQ (COLM 2025). G0b đã gợi ý dạng sai số quan trọng hơn độ lớn: 2 bit α0,25 hỏng hành vi hơn 3 bit α0,75 dù sai số tương đối nhỏ hơn [GỢI Ý].

---

## §6. Phương pháp lấy từ đâu

| Thành phần | Nguồn |
|---|---|
| DAS, DII | Geiger, Wu et al. (CLeaR 2024); pyvene (NAACL 2024 Demo) |
| Tác vụ, odds, selectivity, checkpoint | CausalGym (ACL 2024); Pythia (ICML 2023); Hewitt & Liang (EMNLP 2019) |
| Giới hạn của DAS | Makelov, Lange, Geiger, Nanda (ICLR 2024); Wu et al. (2024, phản hồi); Sutter et al. (NeurIPS 2025); Kumon & Yanaka (ACL 2026); Tanyel & Ayvaz (arXiv 2611.05033) |
| Độ lệch của can thiệp | Grant et al. (ICLR 2026, Oral) |
| Kiểm định tương đương, quy tắc ba nhãn | Bhandari & Wade (arXiv 2609.06473); Makarov (arXiv 2610.40055) |
| Co biên độ dưới lượng tử hoá | Wu, Dhiman, Koshiyama (arXiv 2608.06564) |
| Cross-model patching, dự báo lỗi | Chang et al. (EMNLP 2025); Duan (arXiv 2606.03002) |
| Lan truyền lỗi lượng tử hoá | Chen et al. (arXiv 2609.11716); Zhou et al. (Findings ACL 2026) |
| Lượng tử hoá × huấn luyện | Ouyang et al. (ACL 2025); Armstrong (arXiv 2604.15167); Catalan-Tatjer et al. (ICLR 2026); Kumar et al. (ICLR 2025) |
| Mạch cú pháp qua huấn luyện | Yao, Boguraev, Pimentel, Mahowald (EMNLP 2026) |
| Nén × cơ chế (liên quan) | Faumi & Sumanathilaka (arXiv 2610.37157, distillation); Chhabra & Khalili (2025); CircuitKIT (arXiv 2607.19317) |
| Lượng tử hoá | RTN; GPTQ (ICLR 2023) qua GPT-QModel; AWQ (MLSys 2024); TaCQ (COLM 2025) |
| Thống kê | Bootstrap theo cụm; TOST; Benjamini–Hochberg; mô hình hiệu ứng hỗn hợp |

---

## §7. Phạm vi, cổng, tính toán

| | MVP | Target |
|---|---|---|
| RQ0 | 4 tác vụ, 410M/1B, 9 phương pháp + dog-give; 1 nghiên cứu trường hợp | 2 nghiên cứu trường hợp; chế độ `repo` cho mọi tác vụ |
| C1 | Đủ trục (a)–(e) theo layer ở 2 vùng; null hai phía; RTN theo lưới 4 mức + 8 bit kiểm tra; GPTQ 4 bit | + LEACE, EMD, GPTQ 3 bit |
| C2 | 2×2 cấp biến ở mọi layer vùng cuối; tách layer với RTN | GPTQ tách đoạn |
| C3b | 410M, 6 checkpoint, 1–2 tác vụ | + 1B |
| C3, C4 | — | Nếu còn thời gian |

Cổng: G-N 17/11/2026 · G0 đạt 13/11/2026 · G1 31/12/2026 (có thể dời 15/01/2027) · G2 28/02/2027 · G3 (C3b) 31/03/2027. Chi tiết trong sổ dự án.

**Tính toán** (thay dự toán v0.5, vốn giả định t = 20–60 s):
- Đo được ở G0: t = 6,41 s cho 410M [ĐCM, tác vụ ngắn]; 9,2 s cho 1B [GỢI Ý, 2 lần đo]. Tác vụ câu dài sẽ chậm hơn.
- G1: khoảng 6,5–7 giờ cho 4 tác vụ × 2 model [PHỎNG ĐOÁN].
- C1, học lại theo layer ở 2 vùng (5 seed FP + 5 seed × 3 cấu hình Q + step0): khoảng 1,6 giờ/tác vụ cho 410M, khoảng 12 giờ cho 4 tác vụ × 2 model [PHỎNG ĐOÁN]. Các trục dùng lại và 2×2 chỉ cần đánh giá, cỡ vài phút mỗi tác vụ.
- C3b: 6 checkpoint × 1–2 tác vụ, khoảng 6–10 giờ [PHỎNG ĐOÁN].
- Tổng MVP khoảng 30–35 giờ GPU, tức khoảng 1–2 tuần của hai tài khoản Kaggle.

---

## §8. Rủi ro

| Mã | Rủi ro | Mức | Giảm thiểu |
|---|---|---|---|
| R1 | Ôm quá nhiều | Cao | MVP cố định; Target chỉ sau G3 |
| R2 | Không tái lập được | Trung bình | G1 trước mọi phát triển; tiêu chí định lượng; chế độ `repo`; đối chiếu 12 điểm code gốc |
| R3 | Bị công bố trước | Trung bình | G-N; ba đóng góp độc lập |
| R4 | Null rộng, không phát hiện được gì | Trung bình | Báo cáo độ bất ổn của DAS là kết quả; tăng k |
| R5 | Lưới nén chỉ cho hai cực | Thấp (đã xử lý ở G0b) | Lưới 4 mức có α; áp lại quy tắc theo tác vụ |
| R6 | DAS học lại vô nghĩa vì sàn cao | Trung bình | Trục (b) dùng lại là trục chính; sàn đo theo layer |
| R7 | Lệch phiên bản thư viện; GPTQ cho GPT-NeoX | Trung bình | Tự cài 1D DII; lượng tử hoá giả lập; ghim phiên bản |
| R8 | Quota Kaggle giảm | Trung bình | Ưu tiên 410M; nhật ký GPU; `MAX_HOURS` |
| R9 | Kết quả ở ≤ 1B không chuyển sang model lớn | Chắc chắn là giới hạn | Ghi vào phạm vi |
| R10 | Co biên độ đầu ra che lấp thay đổi cơ chế (T chỉ phản ánh R) | Cao (đã thấy ở G0b) | T_rel (D-12); C2 tách mã hoá/đọc ra; báo cáo cả T thô |
| R11 | Odds DAS bị thổi phồng do hàm mục tiêu (excess) | Trung bình | Báo cáo DAS cạnh vanilla; dùng tỉ lệ (T, T_rel) thay cho độ lớn odds; sàn step0 và dog-give |
| R12 | Code gốc có lỗi vị trí làm số của bài lệch | Trung bình | Tái lập theo công thức; chạy chế độ `repo` để giải thích chênh; hỏi GVHD (sổ §7 câu 6) |
| R13 | Quy tắc thiết kế đổi sau khi thấy dữ liệu (D-08, D-09, D-11, D-12) | Trung bình | Ghi "sau dữ liệu"; chốt trên tác vụ phát triển, áp nguyên cho 3 tác vụ chưa nhìn và 1B |

**Giới hạn ghi vào đề cương:**
- chỉ lượng tử hoá trọng số sau huấn luyện, dạng giả lập;
- chỉ tác vụ template tiếng Anh, chỉ họ Pythia;
- IIA/odds cao chỉ chứng minh có không gian con tuyến tính đủ để chuyển hành vi;
- trên Pythia không tách được số token và learning rate;
- quy tắc chọn lưới, chuẩn hoá T và phạm vi đo được chốt sau khi nhìn tác vụ phát triển.

---

## §9. Việc trước khi chốt

1. ~~G0~~ (đạt 13/11).
2. G1: nhóm xác nhận D-13, chạy `notebooks/01_tai_lap_causalgym.ipynb` (smoke → 410M → 1B), áp tiêu chí §1.
3. Đối chiếu repo gốc: TV-B kiểm 12 điểm (sổ §8).
4. G-N: "Cited by" của CausalGym, Ouyang et al., Duan, Makarov, Tanyel & Ayvaz; tìm "quantization causal abstraction", "quantized distributed alignment search".
5. SPEC C1/C2 (biên tương đương, ngưỡng R, cách đọc tương tác) trước notebook 02.
6. Gửi thầy §0 và 6 câu hỏi (sổ §7).

## Changelog
- v0.6 (13/11/2026): G0 đạt; §0 thêm lân cận mới và số G0; §1 cụ thể hoá RQ0 (4 tác vụ, split test, 9 phương pháp, vị trí source, tiêu chí G1); §2 T_rel = T/R, đo theo layer thay cho ô chính, chốt lưới nén, quan sát 2 bit; §3 2×2 ở mọi layer; §4 tiên nghiệm Yao et al.; §6 thêm nguồn; §7 dự toán theo t đo được; §8 thêm R10–R13, hạ R5.
- v0.5 (12/11/2026): bỏ C5; C3b vào MVP; C3 sang Target; C1 dùng ba nhãn, null hai phía, sàn step0, nút α; C2 chuyển sang thiết kế 2×2 cấp biến; sửa trích dẫn.
- v0.4 (12/11/2026): 3 đóng góp chính + 2 mở rộng.
- v0.3, v0.2, v0.1 (12/11/2026): xem bản cũ.
