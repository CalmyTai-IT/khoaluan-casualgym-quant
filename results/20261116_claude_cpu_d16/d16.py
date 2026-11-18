import json, sys, collections, csv
base = sys.argv[1]
M = ["das","probe0","probe1","mean","pca","kmeans","lda","random","vanilla"]
paper = {  # sổ v0.7 §10 (Table 11-14 của bài)
 ("410m","odds","agr_sv_num_subj-relc"): [4.97,4.32,4.19,3.72,0.29,0.28,1.88,0.03,4.42],
 ("410m","odds","cleft"): [14.46,5.53,4.84,1.78,0.86,0.92,0.05,0.02,5.79],
 ("410m","sel","agr_sv_num_subj-relc"): [3.64,5.63,5.45,4.84,0.40,0.38,2.43,0.03,5.52],
 ("410m","sel","cleft"): [6.91,12.09,10.55,3.99,2.02,2.13,0.08,0.02,12.91],
 ("1b","odds","agr_sv_num_subj-relc"): [6.62,5.23,4.98,4.24,0.36,0.39,1.40,0.01,5.51],
 ("1b","odds","cleft"): [15.56,5.59,3.76,1.62,0.25,0.43,0.16,0.01,6.04],
 ("1b","sel","agr_sv_num_subj-relc"): [4.13,6.97,6.59,5.60,0.42,0.46,1.75,0.01,7.32],
 ("1b","sel","cleft"): [4.05,11.38,7.64,3.36,0.58,0.96,0.33,0.03,12.31],
}
g1 = {  # G1 correct, sổ v0.7 §10 (2 chữ số)
 ("410m","odds","agr_sv_num_subj-relc"): [5.55,4.63,4.59,4.58,0.98,1.02,0.16,0.00,4.75],
 ("410m","odds","cleft"): [14.29,5.52,5.49,5.48,5.34,5.48,0.17,0.01,5.93],
 ("410m","sel","agr_sv_num_subj-relc"): [4.03,6.08,6.02,6.01,1.31,1.39,0.22,0.01,6.09],
 ("410m","sel","cleft"): [6.50,12.27,12.22,12.20,11.94,12.20,0.30,0.01,13.27],
 ("1b","odds","agr_sv_num_subj-relc"): [7.05,5.58,5.57,5.57,2.66,2.82,0.26,0.00,5.84],
 ("1b","odds","cleft"): [15.89,5.81,5.79,5.78,5.65,5.78,0.29,0.00,6.13],
 ("1b","sel","agr_sv_num_subj-relc"): [4.43,7.46,7.45,7.45,3.52,3.72,0.36,0.00,7.79],
 ("1b","sel","cleft"): [4.22,11.88,11.83,11.81,11.55,11.81,0.40,0.01,12.54],
}
out = {}
for job, mk in [("g1r_410m","410m"),("g1r_1b","1b")]:
    site = collections.defaultdict(dict)  # (task,method,layer) -> {region: {manip: odds}}
    manips = collections.Counter()
    for l in open(f"{base}/{job}/results.jsonl"):
        r = json.loads(l)
        if r["exp"] != "site": continue
        manips[r["manip"]] += 1
        site[(r["task"], r["method"], r["layer"])].setdefault(r["region"], {})[r["manip"]] = r["odds"]
    print(job, "manip:", dict(manips))
    csvv = {(row["task"], row["method"]): row for row in csv.DictReader(open(f"{base}/{job}/summary_methods.csv"))}
    for task in ["agr_sv_num_subj-relc","cleft"]:
        for mi, m in enumerate(M):
            layers = sorted({k[2] for k in site if k[0]==task and k[1]==m})
            o = [max(v["none"] for v in site[(task,m,L)].values()) for L in layers]
            s = [max(v["none"]-v["dog-give"] for v in site[(task,m,L)].values() if "dog-give" in v) for L in layers]
            odds = sum(o)/len(o); sel = sum(s)/len(s)
            out[(mk,"odds",task,m)] = odds; out[(mk,"sel",task,m)] = sel
            c = csvv[(task,m)]
            assert abs(odds-float(c["odds"]))<1e-9 and abs(sel-float(c["selectivity"]))<1e-9, (job,task,m,odds,c)
    print(job, "khop summary_methods.csv: odds va selectivity (sai lech < 1e-9)")
# D-16
print("\n=== D-16: {mean, pca, kmeans} x 2 tac vu x 2 model, ti le minh/bai (odds) ===")
n_in = 0; n_in9 = 0; n = 0
for mk in ["410m","1b"]:
    for task in ["agr_sv_num_subj-relc","cleft"]:
        for m in ["mean","pca","kmeans"]:
            i = M.index(m); p = paper[(mk,"odds",task)][i]
            r1 = g1[(mk,"odds",task)][i]/p; rr = out[(mk,"odds",task,m)]/p
            ok = 0.5<=rr<=2; n_in += ok; n_in9 += 0.9<=rr<=1.1; n += 1
            print(f"{mk:5s} {task[:6]:6s} {m:7s} bai {p:5.2f} | G1 {g1[(mk,'odds',task)][i]:5.2f} ({r1:5.2f}) | G1r {out[(mk,'odds',task,m)]:5.2f} ({rr:5.2f}) {'TRONG' if ok else 'ngoai'}")
print(f"Trong [0,5; 2]: {n_in}/{n}; trong [0,9; 1,1]: {n_in9}/{n}")
lab = "Xac nhan" if n_in>=10 else ("Giai thich mot phan" if n_in>=7 else "Khong giai thich duoc")
print("Nhan D-16:", lab)
print("\n=== Moi phuong phap, ti le minh/bai: G1 -> G1r (odds | selectivity) ===")
for mk in ["410m","1b"]:
    for task in ["agr_sv_num_subj-relc","cleft"]:
        print(f"-- {mk} {task}")
        for i,m in enumerate(M):
            po = paper[(mk,"odds",task)][i]; ps = paper[(mk,"sel",task)][i]
            print(f"   {m:7s} odds {g1[(mk,'odds',task)][i]/po:6.2f} -> {out[(mk,'odds',task,m)]/po:6.2f}   (G1r {out[(mk,'odds',task,m)]:6.2f}, bai {po:5.2f}) | sel {g1[(mk,'sel',task)][i]/ps:6.2f} -> {out[(mk,'sel',task,m)]/ps:6.2f} (G1r {out[(mk,'sel',task,m)]:6.2f}, bai {ps:5.2f})")
json.dump({"|".join(k):v for k,v in out.items()}, open("/home/claude/scripts/g1r_tables.json","w"), indent=1)
