# QUY_TRINH_LAM_VIEC.md — Quy trình làm việc (GitHub → Kaggle, notebook, phiên chat)

> Bản 12/11/2026. **Người dùng được thêm, sửa, xoá bất kỳ quy tắc nào.** Claude luôn theo bản mới nhất có trong project hoặc được gửi trong phiên. Khi một yêu cầu trong chat trái với file này, Claude làm theo chat nhưng phải nhắc để cập nhật file.
> Mỗi quy tắc có mã (QT-xx) để dễ trỏ tới. Quy tắc bị xoá thì bỏ luôn mã, không đánh lại số.

## A. Luồng code: máy → GitHub → Kaggle

- **QT-01** Repo GitHub là nơi duy nhất chứa code và cấu hình. Không sửa code trên Kaggle, trừ ô CẤU HÌNH của runner (sửa một lần).
- **QT-02** Claude luôn đưa **file hoàn chỉnh**, không đưa đoạn hay diff. Mỗi file ghi rõ: đường dẫn đích trong repo, và **THAY** (ghi đè file cũ) hay **THÊM** (file mới).
- **QT-03** Người dùng copy file vào repo trên máy, commit với thông điệp `[<cổng hoặc mục>] <việc>` (ví dụ `[G0] smoke test 410M`), rồi push.
- **QT-04** Trên Kaggle chỉ có một notebook `runner` (import một lần từ `kaggle/runner.ipynb`). Mỗi lần chạy, runner:
  - clone commit mới nhất;
  - đọc `configs/kaggle_run.yaml`;
  - chạy các job bằng papermill;
  - lưu kết quả vào `/kaggle/working/outputs/<run_id>/` kèm file `.zip`.
- **QT-05** Muốn chạy gì thì sửa `configs/kaggle_run.yaml` (bật/tắt job bằng `enabled`, đổi `params`). Không mở notebook thí nghiệm trên Kaggle.
- **QT-06** Token GitHub chỉ nằm trong Kaggle Secrets, tên `GITHUB_TOKEN`; dùng fine-grained token, chỉ repo này, quyền Contents: Read-only. Không commit token, không in token ra log.

## B. Cách chạy trên Kaggle

- **QT-10** Mặc định chạy bằng **Save Version → Save & Run All (Commit)**, để có thể tắt Kaggle và làm việc khác.
- **QT-11** Ngoại lệ: chạy **từng ô (interactive)**. Claude phải **nhắc rõ** khi rơi vào một trong các trường hợp sau:
  - (a) smoke test lỗi mà `executed.ipynb` không đủ để biết nguyên nhân;
  - (b) lỗi môi trường (cài thư viện, CUDA, hết RAM/VRAM) cần thử nhiều lần;
  - (c) cần xem biến trung gian hoặc biểu đồ để ra quyết định ngay;
  - (d) việc đo rất nhanh (dưới khoảng 5 phút) mà chờ một version là phí.

  Cách làm: import notebook thí nghiệm (không phải runner) vào Kaggle, bật GPU và Internet, sửa ô `parameters`, chạy từng ô. **Xong thì Stop session** để không tốn quota. Sửa gì thì chép ngược về repo (QT-01).
- **QT-12** Trước mỗi lần chạy dài, chạy job smoke tương ứng trước.
- **QT-13** Mỗi version ghi một dòng vào nhật ký GPU (sổ dự án §6): ngày, tài khoản, run_id, số phút (lấy từ `run_summary.json`).
- **QT-14** Một version không nên dài quá khoảng 9 giờ (phiên Kaggle tối đa 12 giờ). Việc dài hơn thì chia thành nhiều job hoặc nhiều version.

## C. Notebook

- **QT-20** Mọi thí nghiệm viết dạng notebook `.ipynb` trong `notebooks/`, tên `NN_ten_ngan.ipynb` (ví dụ `01_tai_lap_causalgym.ipynb`).
- **QT-21** Ô code đầu tiên là ô `parameters` (tag papermill). Mọi tham số chỉ khai báo ở đây. Comment trong ô này không chứa dấu `=`, vì papermill không phân tích được.
- **QT-22** Mỗi bước một ô, có ô markdown giải thích ngay phía trên. Mỗi ô tự in kết quả chính để đọc được trong `executed.ipynb`.
- **QT-23** Kết quả ghi dần ra JSONL trong `OUT_DIR` (mỗi thí nghiệm một dòng). Không để kết quả chỉ nằm trong RAM.
- **QT-24** Mỗi notebook có chế độ `TOY_TEST = True`, chạy trên CPU với model và dữ liệu giả để kiểm code. Claude chạy chế độ này trước khi gửi notebook.
- **QT-25** Hàm dùng chung giữa các notebook: mặc định chép sang notebook mới. Khi một hàm đã bị chép từ 3 lần trở lên, Claude đề xuất chuyển sang `src/` và **hỏi trước**.
- **QT-26** Mỗi notebook in phiên bản torch, transformers và tên GPU ở ô đầu.

## D. Kết quả

- **QT-30** Sau mỗi version: tải `.zip` ở tab Output, giải nén vào `results/<run_id>/` trong repo, rồi commit. Chỉ commit file nhỏ (jsonl, csv, json, executed.ipynb); không commit trọng số model.
- **QT-31** Mang kết quả vào phiên chat bằng cách đính kèm `run_summary.json` cùng các `results.jsonl` (hoặc nguyên file zip).

## E. Phiên chat với Claude

- **QT-40** Đầu phiên mới: đính kèm `docs/VIEC_CAN_LAM.md` hiện tại và kết quả mới (nếu có).
- **QT-41** Cuối mỗi phiên có thay đổi, Claude viết lại `docs/VIEC_CAN_LAM.md`: việc cụ thể theo thứ tự, file nào thay/thêm, sửa gì trong `kaggle_run.yaml`, ước thời gian GPU, cần mang kết quả gì về.
- **QT-42** Cuối phiên, Claude nhắc cập nhật sổ dự án (version, changelog, trạng thái cổng, việc cần làm, nhật ký GPU). Claude không tự nhận đã lưu gì vào repo hay Kaggle.
- **QT-43** Khi người dùng nói đang vội: trả lời ngắn, đưa việc cần làm trước, lý do sau.

## Lịch sử thay đổi quy trình

- 12/11/2026: tạo file (GitHub → Kaggle runner, Save Version mặc định, notebook-first, file việc cần làm sau phiên).
