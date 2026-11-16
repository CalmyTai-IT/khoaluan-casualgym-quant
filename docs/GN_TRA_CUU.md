# GN_TRA_CUU.md — Cổng G-N (tính mới): cách lấy dữ liệu và cách Claude tổng hợp

> Bản 13/11/2026 (lần 3, Claude). Thay bản lần 2. Đổi cách làm theo yêu cầu người dùng: **người chỉ chạy notebook lấy dữ liệu; Claude lọc, đánh giá và điền bảng.**
> Hạn: 17/11/2026. Việc của người: khoảng 15 phút (phần lớn là chờ).

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
- **Mang về:** file `outputs/96_gn_tra_cuu.zip` (trên Kaggle: khung Output bên phải, thư mục `/kaggle/working/outputs/`). Đính kèm vào phiên chat. Mở phiên mới cũng được.
- **Nếu ô nào báo lỗi mạng hoặc bị giới hạn tốc độ:** cứ chạy tiếp tới ô 8; lỗi được ghi vào `errors.jsonl`. Nếu ô 8 báo trên 20 lỗi, chạy lại cả notebook sau khoảng 10 phút.

Notebook kéo:
- danh sách **bài trích dẫn** (citations) của 7 bài gốc và 4 bài lân cận, từ **Semantic Scholar** và **OpenAlex** (mỗi bài tra cả mã arXiv lẫn DOI ACL, vì OpenAlex có thể tách hai bản);
- kết quả **tìm theo từ khoá**: 10 truy vấn trên Semantic Scholar và OpenAlex (từ 2024), 7 truy vấn có trường trên arXiv;
- toàn bộ phản hồi gốc (`raw/`), để Claude phân tích lại nếu phần xử lý trong notebook sai.

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

## 5. Bảng kết quả (Claude điền)

| # | Bài gốc | Ngày tra | Trích dẫn (S2 / OpenAlex) | Bài trùng | Bài lân cận mới |
|---|---|---|---|---|---|
| 1 | CausalGym | | | | |
| 2 | Ouyang et al. | | | | |
| 3 | Duan | | | | |
| 4 | Makarov | | | | |
| 5 | Tanyel & Ayvaz | | | | |
| 6 | Geiger et al. (DAS) | | | | |
| 7 | Zhou et al. | | | | |
| — | Tìm theo từ khoá (17 truy vấn) | | — | | |

Tra bằng công cụ tìm kiếm web của Claude ngày 13/11/2026 (trước khi có notebook): chưa thấy bài trùng; bài lân cận ghi ở `GHI_CHU_BAI_BAO.md` §4.
