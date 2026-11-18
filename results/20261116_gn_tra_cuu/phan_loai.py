# phan_loai.py — Claude xep loai G-N (16/11/2026) tu candidates_dedup.jsonl cua notebook 96.
# Chay: python3 phan_loai.py candidates_dedup.jsonl  -> ghi phan_loai_claude.csv
# Buoc 1 (may): co nhac luong tu hoa (Q) / nen khac (C) / can thiep-co che (S) trong tieu de + tom tat.
#   Dinh nghia "trung" (GN_TRA_CUU.md §1) doi hoi co luong tu hoa trong so, nen bai khong co Q khong the trung C1/C2/C3b.
# Buoc 2 (nguoi doc): Claude doc tom tat moi bai co Q va S (70 bai), tieu de moi bai co Q (614 bai),
#   tieu de bai co C ma khong co Q (49), tieu de bai khong co tom tat (64); doc ky tom tat cac bai trong NHAN_TAY.
import json, re, csv, sys
rows = [json.loads(l) for l in open(sys.argv[1])]
Q = re.compile(r"quantiz|quantis|low[- ]bit|\bint ?[2348]\b|\b[2348][- ]bit|gptq|\bawq\b|\bnf4\b|bit[- ]width|w4a16|binariz|ternar|post[- ]training quant|\bptq\b|\bqat\b", re.I)
C = re.compile(r"compress|prun|distill|sparsif", re.I)
S = re.compile(r"distributed alignment|\bdas\b|interchange|causal abstraction|patching|circuit|mechanistic|causal mediation|steering|sparse autoencoder|\bsaes?\b|probing|causal interven|interpretab", re.I)
# Nhan tay: chi so dong trong candidates_dedup.jsonl (dem tu 0) -> (loai, ly do)
NHAN_TAY = {
 356: ("lan_can_gan", "Varshney 2609.30275: huong diff-in-means (tu choi) chuyen FP->INT8/INT4, null split-half trong model Q, phan biet dich chuyen voi co gian. Khong DAS/interchange, khong CausalGym, khong tach ma hoa/doc ra, khong checkpoint"),
 1375: ("lan_can_gan", "Elluru et al. 2603.25035: phan tich mach nhan qua + crosscoder duoi pruning va luong tu hoa, VLM. Khong DAS"),
 626: ("lan_can", "Hu & Ramachandran 2609.01587: can thiep mixed-precision theo layer; ton hai khong nam o mach tac vu. Do accuracy, khong do bien"),
 1132: ("lan_can", "E. Duan 2606.15980: probe dong bang giu duoc duoi luong tu hoa, hong duoi fine-tune. Khong can thiep nhan qua; lien quan truc (b) C1"),
 1302: ("lan_can", "Singh & Sajjad IJCNLP-AACL 2025 (2508.16785): calibration, neuron chet, dong gop neuron duoi 4/8 bit. Cap neuron"),
 357: ("lan_can", "Gupta et al. 2611.07891: bu tru khi nen dau attention truy hoi, theo co model. Ablation"),
 749: ("lan_can", "Faumi & Sumanathilaka 2610.37126: pruning, mach IOI/Greater-Than bang patching. Khong luong tu hoa"),
 785: ("lan_can_C3b", "Tigges et al. NeurIPS 2024: mach qua checkpoint Pythia, khong luong tu hoa"),
 838: ("phuong_phap", "Baligar 2026 (Computation 14:212): san sai so fp32 trong activation patching cap tuong tac, co Pythia-410M"),
 9: ("lan_can", "Khorasani et al. 2605.07631: dung CausalGym lam benchmark cho can thiep khong can probe; khong nen"),
 1301: ("lan_can", "Gupte et al. 2507.15977: SAE cua model goc dung cho model nen"),
 1126: ("lan_can", "Zhang et al. 2504.02010: diff-of-means + attribution patching tren LRM nen"),
 587: ("lan_can", "PRISM 2610.20808: chuyen can thiep activation qua do chinh xac (NF4); steering"),
 163: ("phuong_phap", "Asiaee 2607.08349 (CIF): khoang tin cay cho danh gia can thiep"),
 744: ("da_co_trong_so", "Duan 2606.03002"), 377: ("da_co_trong_so", "Makarov 2610.40055"), 593: ("da_co_trong_so", "Bhandari & Wade 2609.06473"),
 647: ("da_co_trong_so", "Zhou et al. 2604.19884"), 943: ("da_co_trong_so", "Chang et al. EMNLP 2025 = 2506.12044 (xac nhan 16/11)"),
 981: ("da_co_trong_so", "TaCQ (C4)"), 1444: ("da_co_trong_so", "PAHQ 2510.23264"), 385: ("da_co_trong_so", "Nwaiwu et al. 2512.13725"),
 67: ("da_co_trong_so", "Wu et al. 2608.06564"), 0: ("da_co_trong_so", "Yao et al. 2610.33299"), 1424: ("da_co_trong_so", "Armstrong 2604.15167"),
 77: ("da_co_trong_so", "Catalan-Tatjer et al. 2510.06213"), 745: ("da_co_trong_so", "Chen et al. 2609.11716"), 829: ("da_co_trong_so", "Ouyang et al. 2411.17691"),
 741: ("da_co_trong_so", "CircuitKIT 2607.19317"),
}
out = csv.writer(open("phan_loai_claude.csv", "w", newline=""))
out.writerow(["id", "nam", "tieu_de", "arxiv", "doi", "Q", "C", "S", "co_tom_tat", "loai", "ly_do"])
cnt = {}
for i, r in enumerate(rows):
    t = (r["title"] or "") + " " + (r["abstract"] or "")
    q, c, s = bool(Q.search(t)), bool(C.search(t)), bool(S.search(t))
    if i in NHAN_TAY: loai, ly = NHAN_TAY[i]
    elif q and s: loai, ly = "khong_trung", "doc tom tat: luong tu hoa nghia khac (VQ, vat ly, trien khai) hoac chi do hanh vi"
    elif q: loai, ly = "khong_trung", "doc tieu de: co luong tu hoa, khong do can thiep/co che"
    elif c: loai, ly = "khong_trung", "doc tieu de: nen khac (pruning/distill), khong luong tu hoa"
    else: loai, ly = "khong_trung", "loc may: khong nhac luong tu hoa/nen nen khong the trung theo dinh nghia"
    cnt[loai] = cnt.get(loai, 0) + 1
    out.writerow([i, r["year"], r["title"], r["arxiv"], r["doi"], int(q), int(c), int(s), int(bool((r["abstract"] or "").strip())), loai, ly])
print(len(rows), "bai;", cnt)
print("Trung C1/C2/C3b:", sum(1 for k in NHAN_TAY.values() if k[0].startswith("trung")))
