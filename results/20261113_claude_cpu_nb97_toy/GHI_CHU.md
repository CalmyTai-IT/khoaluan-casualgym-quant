# Bản chạy TOY notebook 97 của Claude (13/11/2026, CPU)

- Môi trường: Python 3.13, torch 2.15.0 (CPU), transformers 5.22.2, numpy 2.2.6, gptqmodel 7.6.0; `GPTQMODEL_CPU_WORKERS=2`.
- Model GPT-NeoX **ngẫu nhiên** cỡ Pythia-70M, dữ liệu hiệu chỉnh là câu tự ghép (N_CALIB 32, CALIB_LEN 128).
- Chỉ chứng minh code chạy: định nghĩa `gpt_neox`, lượng tử hoá, lưu, nạp lại, lấy Q(W) fp32, tối đa 16 giá trị mỗi nhóm.
- Số PPL và sai số trọng số ở đây **vô nghĩa** về chất lượng (model chưa học). Không đưa vào báo cáo.
