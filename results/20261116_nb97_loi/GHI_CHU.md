# Notebook 97 (GPT-QModel) lỗi ngày 16/11/2026 — chẩn đoán của Claude

**Đầu vào:** ảnh ô 1 (`o1_phien_ban.png`) và traceback ô 2 (`o2_traceback.txt`), người dùng gửi trong chat.

**Ô 1 in:** `torch_truoc` = `torch_sau` = 2.11.0+cpu; transformers 5.20.2; numpy 2.2.6; gptqmodel 7.6.0; **gpu: CPU**. Kèm cảnh báo xung đột phụ thuộc của pip (bigframes, dopamine-rl, moviepy, ydf, gradio): không liên quan tới thí nghiệm.

**Hai vấn đề:**

1. **Không có GPU.** Session chạy với Accelerator None (torch bản `+cpu`, `gpu: CPU`). Notebook 97 cần GPU T4 (VIEC_CAN_LAM 16/11, Bước 7). Kiểm "cài GPT-QModel có đổi torch không" vì thế chưa có giá trị: ảnh môi trường GPU của Kaggle có torch bản CUDA khác bản CPU.
2. **Lỗi ô 2 là lỗi trộn hai phiên bản numpy trong cùng một tiến trình** [GỢI Ý: khớp với traceback, chưa tái hiện]. Ô 1 nhập torch (kéo theo numpy) **trước** khi `pip install`; pip đổi file numpy trên đĩa; ô 2 nhập `numpy.strings` từ file mới trong khi phần C của numpy cũ đã nằm trong bộ nhớ, nên dòng `ufunc.__module__ = ...` hỏng (`'numpy.ufunc' object has no attribute '__module__'`). Dấu hiệu phụ: số `numpy 2.2.6` in ở ô 1 là bản đang nằm trong bộ nhớ, không chắc là bản trên đĩa sau khi cài.

**Cách chạy lại (không cần sửa notebook):** bật GPU T4 + Internet; chạy ô 1; **khởi động lại kernel** (Restart, không phải Stop session, để giữ thư viện đã cài); chạy lại ô 1 (pip lúc này gần như không làm gì), rồi chạy tiếp ô 2 tới ô 8. Chi tiết ở `docs/VIEC_CAN_LAM.md`.

**Nên sửa notebook sau (chưa làm, Claude không có mã notebook 97 trong phiên này):** ô 1 đọc phiên bản bằng `importlib.metadata.version(...)` sau khi cài và in rõ "khởi động lại kernel rồi chạy lại ô 1".
