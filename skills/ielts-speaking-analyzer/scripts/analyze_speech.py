#!/usr/bin/env python3
"""Phân tích bài nói IELTS: transcript + fluency + chunking + phát âm (âm vị).
Usage: python analyze_speech.py AUDIO [--models DIR] [--out OUT_PREFIX] [--no-phones]
Ra: OUT.json (số liệu đầy đủ) + OUT.md (báo cáo để Claude đọc và nhận xét).
"""
import argparse, json, os, re, subprocess, sys, tempfile
import numpy as np
import soundfile as sf

SR = 16000
HERE = os.path.dirname(os.path.abspath(__file__))
FILLERS = {"uh", "um", "er", "erm", "ah", "eh", "hmm", "mm", "uhm"}
BOUNDARY_WORDS = {"and", "but", "so", "because", "which", "that", "who", "when", "if",
                  "although", "while", "or", "then", "however", "actually", "well",
                  "also", "since", "where", "as", "though", "unless"}

# ---------------- audio ----------------
def load_audio(path):
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), tmp], check=True)
    a, sr = sf.read(tmp, dtype="float32"); os.unlink(tmp)
    return a

def run_vad(sherpa_onnx, audio, models):
    cfg = sherpa_onnx.VadModelConfig()
    cfg.silero_vad.model = os.path.join(models, "silero_vad.onnx")
    cfg.silero_vad.min_silence_duration = 0.2
    cfg.silero_vad.min_speech_duration = 0.1
    cfg.silero_vad.threshold = 0.5
    cfg.sample_rate = SR
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=max(60, len(audio) / SR + 5))
    win = cfg.silero_vad.window_size
    segs = []
    def drain():
        while not vad.empty():
            s = vad.front; segs.append((s.start / SR, (s.start + len(s.samples)) / SR)); vad.pop()
    for i in range(0, len(audio), win):
        vad.accept_waveform(audio[i:i + win]); drain()
    vad.flush(); drain()
    return segs

def merge_chunks(segs, max_len=25.0, max_gap=1.5):
    """Gộp các đoạn VAD thành khối <= max_len giây để đưa vào ASR."""
    chunks = []
    for s, e in segs:
        if chunks and e - chunks[-1][0] <= max_len and s - chunks[-1][1] <= max_gap:
            chunks[-1][1] = e
        else:
            chunks.append([s, e])
    return [(max(0, s - 0.15), e + 0.15) for s, e in chunks]

# ---------------- ASR ----------------
def make_parakeet(sherpa_onnx, models):
    d = os.path.join(models, "sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8")
    return sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=f"{d}/encoder.int8.onnx", decoder=f"{d}/decoder.int8.onnx", joiner=f"{d}/joiner.int8.onnx",
        tokens=f"{d}/tokens.txt", model_type="nemo_transducer", num_threads=4)

def make_whisper(sherpa_onnx, models):
    d = os.path.join(models, "sherpa-onnx-whisper-base.en")
    if not os.path.isdir(d): return None
    return sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=f"{d}/base.en-encoder.int8.onnx", decoder=f"{d}/base.en-decoder.int8.onnx",
        tokens=f"{d}/base.en-tokens.txt", language="en", task="transcribe", num_threads=4)

def decode(rec, audio):
    st = rec.create_stream(); st.accept_waveform(SR, audio); rec.decode_stream(st); return st.result

def words_from_tokens(res, offset, chunk_end):
    toks, ts = list(res.tokens), list(res.timestamps)
    durs = list(getattr(res, "durations", []) or []) or [0.08] * len(toks)
    words = []
    for i, (t, s) in enumerate(zip(toks, ts)):
        new = t.startswith("▁") or t.startswith(" ") or not words
        piece = t.replace("▁", " ").lstrip() if new else t
        if new:
            words.append({"raw": piece, "start": offset + s})
        else:
            words[-1]["raw"] += piece
        words[-1]["end"] = offset + s + max(durs[i], 0.04)
    for i, w in enumerate(words):
        nxt = words[i + 1]["start"] if i + 1 < len(words) else chunk_end
        w["end"] = min(nxt, w["end"], w["start"] + 1.5)
        w["word"] = re.sub(r"[^a-z']", "", w["raw"].lower())
        w["punct_after"] = bool(re.search(r"[.,!?;:]$", w["raw"]))
    return [w for w in words if w["word"] or w["raw"]]

def norm_words(text):
    return [re.sub(r"[^a-z']", "", t.lower()) for t in text.split() if re.sub(r"[^a-z']", "", t.lower())]

def disagreements(a_words, b_text):
    """So sánh 2 ASR: từ mà 2 máy nghe khác nhau -> có thể phát âm chưa rõ."""
    import difflib
    a = [w["word"] for w in a_words]; b = norm_words(b_text)
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "replace":
            for k in range(i1, i2): a_words[k]["unclear"] = True
            out.append({"heard_A": " ".join(a[i1:i2]), "heard_B": " ".join(b[j1:j2]), "time": round(a_words[i1]["start"], 2)})
    return out

# ---------------- fluency ----------------
def fluency(words, vad_segs, dur):
    speech_time = sum(e - s for s, e in vad_segs)
    n = len([w for w in words if w["word"] not in FILLERS])
    pauses = []
    for i in range(len(words) - 1):
        gap = words[i + 1]["start"] - words[i]["end"]
        if gap >= 0.25:
            nxt = words[i + 1]["word"]
            boundary = words[i]["punct_after"] or nxt in BOUNDARY_WORDS
            pauses.append({"after": words[i]["raw"], "before": words[i + 1]["raw"], "time": round(words[i]["end"], 2),
                           "len": round(gap, 2), "at_boundary": boundary})
    # mean length of run
    runs, cur = [], 0
    pause_idx = {p["time"] for p in pauses}
    for w in words:
        cur += 1
        if round(w["end"], 2) in pause_idx: runs.append(cur); cur = 0
    if cur: runs.append(cur)
    # repetitions / self-corrections
    reps = []
    ws = [w["word"] for w in words]
    for i in range(len(ws) - 1):
        if ws[i] and ws[i] == ws[i + 1] and ws[i] not in {"that", "had", "very"}:
            reps.append({"word": ws[i], "time": round(words[i]["start"], 2)})
    for i in range(len(ws) - 3):
        if ws[i:i + 2] == ws[i + 2:i + 4] and ws[i]:
            reps.append({"word": " ".join(ws[i:i + 2]), "time": round(words[i]["start"], 2)})
    # voiced regions with no recognised word -> likely filled pauses (uh/um)
    hes = []
    for s, e in vad_segs:
        if e - s < 0.15: continue
        if not any(w["start"] < e and w["end"] > s for w in words):
            hes.append({"time": round(s, 2), "len": round(e - s, 2)})
    mid = [p for p in pauses if not p["at_boundary"]]
    return {
        "total_duration_s": round(dur, 1), "speaking_time_s": round(speech_time, 1), "n_words": n,
        "speech_rate_wpm": round(n / dur * 60, 1) if dur else 0,
        "articulation_rate_wpm": round(n / speech_time * 60, 1) if speech_time else 0,
        "phonation_ratio": round(speech_time / dur, 2) if dur else 0,
        "n_pauses": len(pauses), "pauses_per_min": round(len(pauses) / dur * 60, 1) if dur else 0,
        "n_long_pauses_1s": len([p for p in pauses if p["len"] >= 1.0]),
        "mean_pause_s": round(float(np.mean([p["len"] for p in pauses])), 2) if pauses else 0,
        "mean_length_of_run_words": round(float(np.mean(runs)), 1) if runs else 0,
        "pct_pauses_mid_chunk": round(100 * len(mid) / len(pauses)) if pauses else 0,
        "pauses": pauses, "repetitions": reps, "probable_filled_pauses": hes,
        "explicit_fillers": [{"word": w["word"], "time": round(w["start"], 2)} for w in words if w["word"] in FILLERS],
    }

# ---------------- intonation ----------------
def pitch_stats(audio, vad_segs):
    f0s = []
    fl, hop = 640, 160
    for s, e in vad_segs:
        x = audio[int(s * SR):int(e * SR)]
        for i in range(0, len(x) - fl, hop):
            fr = x[i:i + fl] * np.hanning(fl)
            if np.sqrt(np.mean(fr ** 2)) < 0.01: continue
            ac = np.correlate(fr, fr, "full")[fl - 1:]
            lo, hi = SR // 400, SR // 70
            k = lo + int(np.argmax(ac[lo:hi]))
            if ac[k] > 0.45 * ac[0]: f0s.append(SR / k)
    if len(f0s) < 20: return {"note": "không đủ dữ liệu cao độ"}
    st = 12 * np.log2(np.array(f0s) / np.median(f0s))
    return {"median_f0_hz": round(float(np.median(f0s))), "pitch_range_semitones_p10_p90": round(float(np.percentile(st, 90) - np.percentile(st, 10)), 1),
            "pitch_sd_semitones": round(float(np.std(st)), 1),
            "hint": "<4 bán cung: khá đều đều; 4-7: bình thường; >7: ngữ điệu biến hoá"}

# ---------------- phonemes ----------------
ARPA2IPA = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "AW": "aʊ", "AY": "aɪ", "B": "b", "CH": "tʃ", "D": "d", "DH": "ð",
            "EH": "ɛ", "ER": "ɝ", "EY": "eɪ", "F": "f", "G": "ɡ", "HH": "h", "IH": "ɪ", "IY": "i", "JH": "dʒ", "K": "k",
            "L": "l", "M": "m", "N": "n", "NG": "ŋ", "OW": "oʊ", "OY": "ɔɪ", "P": "p", "R": "ɹ", "S": "s", "SH": "ʃ",
            "T": "t", "TH": "θ", "UH": "ʊ", "UW": "u", "V": "v", "W": "w", "Y": "j", "Z": "z", "ZH": "ʒ"}
CONS = set("b d ð f ɡ h dʒ k l m n ŋ p ɹ s ʃ t tʃ θ v w j z ʒ".split())
# nhóm âm coi là "gần đúng" để không bắt lỗi vụn vặt
EQUIV = [{"ɑ", "ɔ", "a", "ɒ"}, {"ʌ", "ə", "ɐ"}, {"ɝ", "ɚ", "ɹ", "ɻ", "ɹ̩", "ɚ˞"}, {"i", "iː"}, {"u", "uː"}, {"ɡ", "g"},
         {"e", "eɪ", "ɛ"}, {"o", "oʊ"}, {"ɾ", "t", "d"}, {"ɪ", "ɨ", "i"}, {"ʊ", "u"}]

def same(a, b):
    return a == b or any(a in g and b in g for g in EQUIV)

def expected_phones(word, cmu):
    prons = cmu.get(word)
    if not prons: return None
    return [ARPA2IPA[re.sub(r"\d", "", p)] for p in prons[0]]

def split_phone(p):
    p = p.replace("ː", "")
    for d in ["tʃ", "dʒ", "aʊ", "aɪ", "eɪ", "oʊ", "ɔɪ"]:
        if p == d: return [p]
    return [p]

def align(exp, got):
    n, m = len(exp), len(got)
    D = np.zeros((n + 1, m + 1)); D[:, 0] = range(n + 1); D[0, :] = range(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i, j] = min(D[i - 1, j] + 1, D[i, j - 1] + 1, D[i - 1, j - 1] + (0 if same(exp[i - 1], got[j - 1]) else 1))
    ops, i, j = [], n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i, j] == D[i - 1, j - 1] + (0 if same(exp[i - 1], got[j - 1]) else 1):
            if not same(exp[i - 1], got[j - 1]): ops.append(("sub", exp[i - 1], got[j - 1], i - 1))
            i, j = i - 1, j - 1
        elif i > 0 and D[i, j] == D[i - 1, j] + 1:
            ops.append(("del", exp[i - 1], None, i - 1)); i -= 1
        else:
            ops.append(("ins", None, got[j - 1], i)); j -= 1
    return ops[::-1]

WEAK = {"a", "an", "the", "to", "and", "of", "for", "from", "can", "was", "were", "her", "them", "at", "as",
        "but", "that", "than", "some", "your", "you", "do", "does", "has", "have", "had", "or", "are", "be", "been", "he",
        "she", "we", "us", "his", "him", "there", "would", "could", "should", "just", "is", "it", "in", "on", "my"}
VOWELS = {"ɑ", "æ", "ʌ", "ɔ", "aʊ", "aɪ", "ɛ", "ɝ", "eɪ", "ɪ", "i", "oʊ", "ɔɪ", "ʊ", "u", "ə"}

DIPH = {("a", "j"): "aɪ", ("a", "ɪ"): "aɪ", ("e", "j"): "eɪ", ("e", "ɪ"): "eɪ", ("o", "w"): "oʊ", ("o", "ʊ"): "oʊ",
        ("a", "w"): "aʊ", ("a", "ʊ"): "aʊ", ("ɔ", "j"): "ɔɪ", ("ɔ", "ɪ"): "ɔɪ"}

def norm_recognized(seq):
    seq = [x.replace("t͡ʃ", "tʃ").replace("d͡ʒ", "dʒ").replace("ː", "").replace("ɹ̩", "ɝ").replace("ɚ", "ɝ") for x in seq]
    out, i = [], 0
    while i < len(seq):
        if i + 1 < len(seq) and (seq[i], seq[i + 1]) in DIPH: out.append(DIPH[(seq[i], seq[i + 1])]); i += 2
        else: out.append(seq[i]); i += 1
    return out

def phone_analysis(audio, words, models, chunks):
    try:
        from allosaurus.app import read_recognizer
        import cmudict
    except Exception as ex:
        return {"error": f"chưa cài allosaurus/torch: {ex}"}
    rec = read_recognizer("eng2102")
    cmu = cmudict.dict()
    tmpd = tempfile.mkdtemp()
    per_word, patterns = {}, {}
    for ci, (s, e) in enumerate(chunks):
        p = os.path.join(tmpd, f"c{ci}.wav"); sf.write(p, audio[int(s * SR):int(e * SR)], SR)
        got = norm_recognized(rec.recognize(p, "eng").split())
        exp, owner = [], []
        cw = [i for i, w in enumerate(words) if s <= w["start"] < e]
        for i in cw:
            ph = expected_phones(words[i]["word"], cmu) if words[i]["word"] not in FILLERS else None
            if not ph: continue
            per_word[i] = {"word": words[i]["word"], "time": round(words[i]["start"], 2),
                           "expected": "/" + " ".join(ph) + "/", "errors": [], "_n": len(ph)}
            for k, x in enumerate(ph): exp.append(x); owner.append((i, k, len(ph)))
        if not exp or not got: continue
        # căn chỉnh toàn khối (global alignment) rồi quy lỗi về từng từ
        for typ, ea, gb, pos in align(exp, got):
            if typ == "ins" or pos >= len(owner): continue
            wi, k, n = owner[pos]
            # dạng yếu tự nhiên của từ chức năng: nguyên âm -> schwa, "and" mất /d/, "h" câm ...
            if words[wi]["word"] in WEAK and (ea in VOWELS or ea == "h" or (words[wi]["word"] == "and" and ea == "d")):
                continue
            final = k == n - 1 and ea in CONS
            key = f"/{ea}/ → /{gb}/" if typ == "sub" else (f"bỏ âm cuối /{ea}/" if final else f"bỏ /{ea}/")
            per_word[wi]["errors"].append(key)
            patterns.setdefault(key, []).append(words[wi]["word"])
    pw = [v for k, v in sorted(per_word.items())]
    for v in pw:
        v["flag"] = len(v["errors"]) / v.pop("_n") >= 0.5  # >= nửa số âm lệch -> từ nghi đọc sai
    checked = len(pw)
    top = sorted(([k, len(v), sorted(set(v))[:8]] for k, v in patterns.items()), key=lambda x: -x[1])
    return {"words_checked": checked,
            "words_with_issue_pct": round(100 * len([x for x in pw if x["errors"]]) / checked) if checked else 0,
            "recurring_patterns": [{"pattern": k, "count": c, "examples": ex} for k, c, ex in top if c >= 2][:25],
            "flagged_words": [f"{v['word']} {v['expected']} @{v['time']}s: {', '.join(v['errors'])}" for v in pw if v["flag"]][:30],
            "per_word": pw}

# ---------------- report ----------------
def report_md(R):
    F, L = R["fluency"], []
    L.append(f"# Phân tích bài nói: {os.path.basename(R['audio'])}\n")
    L.append("## Transcript (ASR — có thể sai ở chỗ phát âm chưa rõ)\n")
    L.append(R["transcript_marked"] + "\n")
    L.append("Ký hiệu: `(0.8s)` = ngừng ≥0.25s; `[?]` = từ 2 máy nghe khác nhau (nghi phát âm chưa rõ); `{uh}` = khoảng phát âm không thành từ (nghi ừm/à).\n")
    L.append("## Fluency\n")
    for k in ["total_duration_s", "speaking_time_s", "n_words", "speech_rate_wpm", "articulation_rate_wpm", "phonation_ratio",
              "n_pauses", "pauses_per_min", "n_long_pauses_1s", "mean_pause_s", "mean_length_of_run_words", "pct_pauses_mid_chunk"]:
        L.append(f"- {k}: {F[k]}")
    L.append(f"- lặp từ: {len(F['repetitions'])} → {', '.join(r['word'] for r in F['repetitions'][:10])}")
    L.append(f"- nghi ừm/à (filled pauses): {len(F['probable_filled_pauses']) + len(F['explicit_fillers'])}\n")
    L.append("### Ngừng giữa cụm (chunking chưa tốt)\n")
    for p in [p for p in F["pauses"] if not p["at_boundary"]][:25]:
        L.append(f"- {p['time']}s: \"…{p['after']} / ({p['len']}s) / {p['before']}…\"")
    L.append("\n## Ngữ điệu\n"); L.append(json.dumps(R["pitch"], ensure_ascii=False) + "\n")
    if R.get("asr_disagreements"):
        L.append("## Từ nghi phát âm chưa rõ (2 ASR nghe khác nhau)\n")
        for d in R["asr_disagreements"][:30]: L.append(f"- {d['time']}s: A=\"{d['heard_A']}\" / B=\"{d['heard_B']}\"")
    P = R.get("phones")
    if P:
        L.append("\n## Âm vị\n")
        if "error" in P: L.append(P["error"])
        else:
            L.append(f"Kiểm tra {P['words_checked']} từ; {P['words_with_issue_pct']}% có lệch so với phát âm chuẩn (máy nhận dạng âm vị có nhiễu — chỉ tin các lỗi LẶP LẠI).\n")
            for x in P["recurring_patterns"]: L.append(f"- {x['pattern']} ×{x['count']}: {', '.join(x['examples'])}")
            if P["flagged_words"]:
                L.append("\n### Từ lệch nhiều (≥ nửa số âm)\n")
                for x in P["flagged_words"]: L.append(f"- {x}")
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("--models", default=os.environ.get("SPEECH_MODELS", os.path.expanduser("~/.cache/ielts-speech-models")))
    ap.add_argument("--out"); ap.add_argument("--no-phones", action="store_true")
    a = ap.parse_args()
    import sherpa_onnx
    out = a.out or os.path.splitext(a.audio)[0] + "_analysis"
    audio = load_audio(a.audio); dur = len(audio) / SR
    vad = run_vad(sherpa_onnx, audio, a.models)
    pk, wh = make_parakeet(sherpa_onnx, a.models), make_whisper(sherpa_onnx, a.models)
    words, wtext = [], []
    chunks = merge_chunks(vad)
    for s, e in chunks:
        seg = audio[int(s * SR):int(e * SR)]
        words += words_from_tokens(decode(pk, seg), s, e)
        if wh: wtext.append(decode(wh, seg).text)
    dis = disagreements(words, " ".join(wtext)) if wh else []
    F = fluency(words, vad, dur)
    # transcript có đánh dấu
    pmap = {p["time"]: p for p in F["pauses"]}
    hes = sorted(F["probable_filled_pauses"], key=lambda h: h["time"])
    parts, hi = [], 0
    for w in words:
        while hi < len(hes) and hes[hi]["time"] < w["start"]: parts.append("{uh}"); hi += 1
        parts.append(w["raw"] + ("[?]" if w.get("unclear") else ""))
        p = pmap.get(round(w["end"], 2))
        if p: parts.append(f"({p['len']}s)" if p["at_boundary"] else f"**/({p['len']}s)/**")
    R = {"audio": a.audio, "transcript": " ".join(w["raw"] for w in words), "transcript_marked": " ".join(parts),
         "whisper_transcript": " ".join(wtext), "fluency": F, "pitch": pitch_stats(audio, vad), "asr_disagreements": dis,
         "words": [{k: (round(v, 2) if isinstance(v, float) else v) for k, v in w.items()} for w in words]}
    if not a.no_phones: R["phones"] = phone_analysis(audio, words, a.models, chunks)
    json.dump(R, open(out + ".json", "w"), ensure_ascii=False, indent=1)
    open(out + ".md", "w").write(report_md(R))
    print(out + ".md")

if __name__ == "__main__":
    main()
