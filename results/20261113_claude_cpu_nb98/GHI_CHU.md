# Bản chạy notebook 98 của Claude (13/11/2026, CPU)

- Môi trường: Python 3.13, torch 2.15.0 (CPU), transformers 4.46.2, pyvene 0.1.6. Chạy lại bằng transformers 5.22.2 (không có ô pyvene) cho cùng kết quả.
- Repo gốc `aryamanarora/causalgym` @ `0f3129f`.
- Tokenizer: GPT-NeoX-20B, bản sao `BlinkDL/RWKV-LM/RWKV-v4/20B_tokenizer.json` (sha256 56ac4821e129d2c520fdaba60abd920fa852ada51b45c0dd52bbb6bd8c985ade), vì phiên không vào được Hugging Face.
- Tham số: `TOY_TEST = True`, `COMPARE_HF = False`, `RUN_PYVENE_TEST = True`. Dữ liệu là dữ liệu thật của repo gốc; chỉ phần so với file HF bị bỏ qua.
- TV-B chạy lại với tokenizer HF và `COMPARE_HF = True` (`docs/VIEC_CAN_LAM.md` bản 16/11, Bước 4; trước đây là HUONG_DAN_VIEC_14_18_11.md Bước 3).
