# NHAN_XET_GVHD_LAN3.md — Lời duyệt và nhận xét lần 3 của GVHD

> Ghi ngày 16/11/2026 (Claude), từ nội dung TV-A dán vào phiên chat. GVHD: ThS. Tuân Nguyễn Hoài Đức. Đối tượng nhận xét: đề xuất hướng B1 (CausalGym × lượng tử hoá).
> File riêng cho lần 3, để không ghi đè các lần nhận xét trước nếu repo đã có file nhận xét khác.

## 1. Nguyên văn

> Tôi đã xem đề xuất của các em và có ý kiến như sau:
>
> 1/ Về bài báo gốc: Tôi đồng ý chọn CausalGym làm bài báo nền tảng. Bài báo có chất lượng học thuật tốt và phù hợp với hướng nghiên cứu.
>
> 2/ Về khối lượng công việc: Phạm vi hiện tại khá tham vọng đối với khóa luận tốt nghiệp. Tôi đề nghị ưu tiên RQ0, C1 và C2; chuyển C3b thành phần mở rộng nếu còn thời gian. Cần đảm bảo chất lượng thực nghiệm và phân tích thay vì chạy theo số lượng đóng góp.
>
> 3/ Về kết quả nghiên cứu: Nếu thực nghiệm cho thấy cơ chế vẫn được bảo toàn ở 8-bit và 4-bit, chỉ suy giảm ở 3-bit và 2-bit, thì đây vẫn là kết quả khoa học hợp lệ. Điều quan trọng là phương pháp đánh giá chặt chẽ, có đối chứng, kiểm định thống kê phù hợp và giải thích được kết quả. Không nhất thiết phải phát hiện sự suy giảm ở 4-bit mới được xem là có đóng góp.

## 2. Ý kiến nào trả lời câu hỏi nào (sổ §7)

| Câu hỏi trong sổ §7 | Ý kiến | Trạng thái |
|---|---|---|
| 1. CausalGym có đạt yêu cầu "bài báo gốc" không? | Ý 1: đồng ý | Đã trả lời |
| 2. MVP có hợp lý không? | Ý 2: quá rộng; ưu tiên RQ0, C1, C2; C3b là mở rộng | Đã trả lời; ghi thành D-17 |
| 3. "Cơ chế được bảo toàn" có được tính là kết quả không? | Ý 3: được, nếu phương pháp chặt | Đã trả lời |
| 4. Dùng checkpoint GPTQ của Ouyang et al.? | Chưa nhắc | Còn hỏi (ít cấp thiết hơn sau D-17) |
| 5. Hạn đề cương | Chưa nhắc | Còn hỏi |
| 6. Báo cáo cả bản theo công thức và bản theo code gốc? | Chưa nhắc | Còn hỏi, kèm kết quả G1r |

## 3. Hệ quả cho kế hoạch (Claude đề xuất; sổ v0.8 ghi)

1. **Phạm vi (D-17).** MVP = RQ0 + C1 + C2. C3b chuyển sang phần mở rộng, chỉ làm khi G2 đã đạt. C3 và C4 vẫn là Target, xếp sau C3b. Cổng G3 không còn là cổng MVP.
2. **Ngân sách.** Phần GPU dành cho C3b (học DAS trên nhiều checkpoint) chuyển cho C1 và C2. SPEC C1 nên dùng phần này để tăng độ tin cậy (đủ seed cho null hai phía, đủ 4 tác vụ × 2 model) thay vì thêm phép đo mới. Con số cụ thể chốt trong SPEC.
3. **"Bảo toàn" phải là phát biểu có kiểm định.** Ý 3 chấp nhận kết quả "giữ ở 8 và 4 bit". Điều kiện thầy nêu (đối chứng, kiểm định phù hợp) nghĩa là nhãn *Tương đương* phải đến từ một phép kiểm tương đương với biên chốt trước (D-05; cách làm của Makarov), không phải từ việc "không thấy khác". Varshney (arXiv 2609.30275, tìm thấy qua G-N) nói đúng điểm này: không phát hiện dịch chuyển ở INT8 chưa phải là phát biểu tương đương.
4. **Chất lượng hơn số lượng.** Khớp với yêu cầu của TV-A ngày 16/11: hoãn SPEC C1 tới sau một phiên tìm hiểu code và phương pháp (D-18).

## 4. Việc kéo theo

- Sửa ô Instructions của Claude Project: dòng MVP (TV-A làm; Claude không ghi lên Project).
- Đề xuất `DEXUAT_HUONG_B1_DAS.md` v0.6 chưa cập nhật theo D-17. Khi mâu thuẫn, theo sổ. Cập nhật đề xuất khi viết đề cương.
- Câu hỏi 4, 5, 6 gửi thầy kèm đề cương (23–30/11).
