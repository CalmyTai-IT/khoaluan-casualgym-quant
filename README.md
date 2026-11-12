# khoaluan-causalgym-quant

Khoá luận tốt nghiệp (HCMUS): cơ chế nhân quả mà CausalGym định vị bằng DAS có còn khi lượng tử hoá trọng số Pythia không.

## Cấu trúc

```
kaggle/runner.ipynb        notebook duy nhất trên Kaggle: clone repo, chạy job bằng papermill
configs/kaggle_run.yaml    "chạy gì" cho lần Save Version tiếp theo
notebooks/NN_*.ipynb       thí nghiệm (ô đầu là ô parameters; có chế độ TOY_TEST)
results/<run_id>/          kết quả tải về từ Kaggle (file nhỏ)
docs/                      quy trình, việc cần làm, sổ dự án, đề xuất, project instructions
```

## Chạy một thí nghiệm

1. Sửa `configs/kaggle_run.yaml`: bật/tắt job, đổi `params`.
2. Commit `[<cổng>] <việc>`, rồi push.
3. Kaggle: mở notebook runner → **Save Version → Save & Run All**.
4. Tab Output: tải `outputs/<run_id>.zip`, giải nén vào `results/`, rồi commit.

Chi tiết và ngoại lệ (khi nào chạy từng ô): `docs/QUY_TRINH_LAM_VIEC.md`. Việc trước mắt: `docs/VIEC_CAN_LAM.md`.

## Kiểm code trên máy (không cần GPU)

```
pip install papermill torch transformers datasets pyyaml
papermill notebooks/00_g0_pilot.ipynb /tmp/out.ipynb -p TOY_TEST True -p OUT_DIR /tmp/g0_toy
```
