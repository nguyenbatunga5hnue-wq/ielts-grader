#!/usr/bin/env python3
"""Đo các dấu hiệu văn bản do AI viết (hoặc AI sửa) trong bài IELTS Writing.
KHÔNG phải máy phát hiện AI: chỉ đưa ra số đo để thầy/Claude cân nhắc cùng các bằng chứng khác.

Usage: python ai_signals.py BAI.txt [--baseline BAI_CU1.txt BAI_CU2.txt ...] [--json]
"""
import argparse, json, re, statistics as st, sys

# Từ/cụm LLM dùng nhiều bất thường so với người học (và cả người bản ngữ)
AI_WORDS = """delve delves delving tapestry multifaceted pivotal plethora myriad underscore underscores underscored
foster fosters fostering bolster bolstering navigate navigating landscape realm intricate intricacies nuanced
paramount crucial crucially vital seamless seamlessly robust holistic synergy leverage leveraging
embark testament transformative unprecedented ever-evolving ever-changing interconnected meticulous
commendable noteworthy notably profound profoundly invaluable indispensable inherent inherently
facet facets showcase showcasing streamline elevate empower empowering resonate resonates harness
cornerstone catalyst trajectory paradigm discourse bustling vibrant enhance enhancing enhances""".split()
AI_PHRASES = ["in today's fast-paced world", "in today's world", "in today's society", "in the modern era",
    "in an era of", "in an increasingly", "it is important to note", "it is worth noting", "it is crucial to",
    "it is imperative", "plays a crucial role", "plays a pivotal role", "plays a vital role", "a double-edged sword",
    "on the one hand", "striking a balance", "strike a balance", "a delicate balance", "a wide range of",
    "a myriad of", "a plethora of", "serves as a", "not only", "paving the way", "pave the way",
    "in conclusion, while", "ultimately,", "furthermore,", "moreover,", "additionally,", "consequently,",
    "by doing so", "this, in turn", "in turn,", "foster a sense of", "sense of community", "well-being",
    "holistic approach", "multifaceted approach", "collective effort", "shared responsibility",
    "it is essential", "far-reaching", "long-term consequences", "the benefits far outweigh",
    "outweigh the drawbacks", "both sides of the argument", "a balanced approach"]
CONNECTORS = ["moreover", "furthermore", "additionally", "in addition", "consequently", "therefore", "thus",
              "however", "nevertheless", "nonetheless", "ultimately", "notably", "conversely", "hence", "subsequently"]

def sents(t):
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])", t.strip()) if len(s.split()) >= 2]

def words(t):
    return re.findall(r"[A-Za-z][A-Za-z'-]*", t)

def mattr(ws, w=50):
    ws = [x.lower() for x in ws]
    if len(ws) <= w: return len(set(ws)) / max(1, len(ws))
    return st.mean(len(set(ws[i:i + w])) / w for i in range(len(ws) - w + 1))

def metrics(text):
    try:
        from wordfreq import zipf_frequency as zf
    except Exception:
        zf = None
    low = text.lower()
    ws = words(text); n = max(1, len(ws))
    ss = sents(text); sl = [len(words(s)) for s in ss]
    paras = [p for p in re.split(r"\n\s*\n|\n", text) if len(words(p)) >= 5]
    pl = [len(words(p)) for p in paras]
    aiw = {}
    for w in ws:
        lw = w.lower()
        if lw in AI_WORDS: aiw[lw] = aiw.get(lw, 0) + 1
    aip = {p: low.count(p) for p in AI_PHRASES if low.count(p)}
    con = {c: len(re.findall(r"(?:^|[.;]\s+|\n)" + c + r"\b", low)) for c in CONNECTORS}
    con = {k: v for k, v in con.items() if v}
    triads = len(re.findall(r"\b\w+(?: \w+)?, \w+(?: \w+)?,? and \w+", text))
    typo = {
        "em_dash —": text.count("—"), "en_dash –": text.count("–"),
        "curly_quotes ‘’“”": sum(text.count(c) for c in "‘’“”"), "straight_quotes '\"": text.count("'") + text.count('"'),
        "markdown ** or #": text.count("**") + len(re.findall(r"^#+ ", text, re.M)),
        "bullets •": text.count("•"), "nbsp/zero-width": sum(text.count(c) for c in " ​‌‍﻿"),
    }
    out = {
        "n_words": len(ws), "n_sentences": len(ss), "n_paragraphs": len(paras),
        "sent_len_mean": round(st.mean(sl), 1) if sl else 0,
        "sent_len_sd": round(st.pstdev(sl), 1) if len(sl) > 1 else 0,
        "sent_len_cv": round(st.pstdev(sl) / st.mean(sl), 2) if len(sl) > 1 else 0,
        "para_len_cv": round(st.pstdev(pl) / st.mean(pl), 2) if len(pl) > 1 else 0,
        "mattr50": round(mattr(ws), 3),
        "ai_words_per_100w": round(100 * sum(aiw.values()) / n, 2), "ai_words": aiw,
        "ai_phrases": aip, "connectors_sentence_initial": con,
        "connectors_per_sentence": round(sum(con.values()) / max(1, len(ss)), 2),
        "triads_X_Y_and_Z": triads, "contractions": len(re.findall(r"\b\w+'(?:t|s|re|ve|ll|d|m)\b", text)),
        "typography": typo,
    }
    if zf:
        z = [zf(w.lower(), "en") for w in ws if len(w) > 2]
        out["mean_zipf"] = round(st.mean(z), 2) if z else 0
        out["pct_rare_words_zipf_lt_3.5"] = round(100 * sum(1 for x in z if 0 < x < 3.5) / max(1, len(z)), 1)
        out["rare_words"] = sorted({w.lower() for w in ws if len(w) > 2 and 0 < zf(w.lower(), "en") < 3.5})[:40]
        out["non_dictionary_words (lỗi chính tả?)"] = sorted({w for w in ws if len(w) > 2 and zf(w.lower(), "en") == 0})[:30]
    return out

def flags(m):
    """Diễn giải thô. Ngưỡng là kinh nghiệm, không phải xác suất."""
    f = []
    if m["ai_words_per_100w"] >= 1.5: f.append(f"Mật độ từ 'kiểu AI' cao ({m['ai_words_per_100w']}/100 từ)")
    if len(m["ai_phrases"]) >= 4: f.append(f"Nhiều cụm sáo kiểu AI ({len(m['ai_phrases'])} cụm)")
    if m["n_sentences"] >= 8 and m["sent_len_cv"] < 0.30: f.append(f"Độ dài câu đều bất thường (CV={m['sent_len_cv']})")
    if m["n_paragraphs"] >= 4 and m["para_len_cv"] < 0.15: f.append(f"Các đoạn dài gần bằng nhau (CV={m['para_len_cv']})")
    if m["connectors_per_sentence"] >= 0.4: f.append("Mở câu bằng connector dày đặc (Moreover/Furthermore/Additionally…)")
    t = m["typography"]
    if t["em_dash —"] >= 2: f.append(f"Dùng em dash — {t['em_dash —']} lần (hiếm ở học sinh gõ tay)")
    if t["markdown ** or #"] or t["bullets •"]: f.append("Có dấu vết định dạng markdown/bullet (dán từ chatbot?)")
    if t["curly_quotes ‘’“”"] and t["straight_quotes '\""]: f.append("Trộn ngoặc cong và ngoặc thẳng (dấu hiệu dán từ nguồn khác)")
    if t["nbsp/zero-width"]: f.append("Có ký tự ẩn (nbsp/zero-width) — thường do copy-paste")
    if m.get("pct_rare_words_zipf_lt_3.5", 0) >= 12: f.append(f"Tỉ lệ từ hiếm cao ({m['pct_rare_words_zipf_lt_3.5']}%)")
    return f

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text"); ap.add_argument("--baseline", nargs="*", default=[]); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    m = metrics(open(a.text, encoding="utf-8").read())
    R = {"target": m, "flags": flags(m), "baseline": []}
    for b in a.baseline:
        bm = metrics(open(b, encoding="utf-8").read())
        R["baseline"].append({"file": b, **{k: bm[k] for k in ["n_words", "sent_len_mean", "sent_len_cv", "mattr50",
            "ai_words_per_100w", "connectors_per_sentence", "mean_zipf", "pct_rare_words_zipf_lt_3.5"] if k in bm},
            "non_dictionary_words": bm.get("non_dictionary_words (lỗi chính tả?)", [])})
    if a.json: print(json.dumps(R, ensure_ascii=False, indent=1)); return
    print("== BÀI CẦN KIỂM TRA ==")
    for k, v in m.items(): print(f"{k}: {v}")
    print("\n== CỜ (dấu hiệu, không phải kết luận) ==")
    for x in R["flags"] or ["(không có cờ nào)"]: print("- " + x)
    if R["baseline"]:
        print("\n== SO VỚI BÀI CŨ CỦA CHÍNH HỌC SINH ==")
        keys = ["sent_len_mean", "sent_len_cv", "mattr50", "ai_words_per_100w", "connectors_per_sentence", "mean_zipf", "pct_rare_words_zipf_lt_3.5"]
        print("chỉ số".ljust(30) + "bài này".ljust(10) + " | ".join(b["file"].split("/")[-1][:14] for b in R["baseline"]))
        for k in keys:
            print(k.ljust(30) + str(m.get(k)).ljust(10) + " | ".join(str(b.get(k)).ljust(14) for b in R["baseline"]))

if __name__ == "__main__":
    main()
