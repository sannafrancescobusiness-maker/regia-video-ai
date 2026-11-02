#!/usr/bin/env python3
"""Tempi parola per parola di una voce sul testo del copy.
uso: allinea.py voce.wav copy.txt cartella_comp  →  parole.js (window.PAROLE) e frasi.js (window.FRASI).
Ogni riga non vuota del copy è una frase. Il modello si indica con WHISPER_MODEL oppure si cerca in ./models."""
import difflib, glob, json, os, re, subprocess, sys, tempfile
wav, copy, out = sys.argv[1:4]
cand = [os.environ.get("WHISPER_MODEL", ""), "models/ggml-large-v3.bin", "../models/ggml-large-v3.bin"] + glob.glob(os.path.expanduser("~/*/models/ggml-large-v3.bin"))
MOD = next((c for c in cand if c and os.path.exists(c)), None)
if not MOD: sys.exit("Modello non trovato: imposta WHISPER_MODEL")
norm = lambda s: re.sub(r"[^a-zàèéìòù0-9]", "", s.lower())
frasi = [r.strip().replace("«", "").replace("»", "").split() for r in open(copy, encoding="utf-8") if r.strip()]
tmp = tempfile.mkdtemp()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-ar", "16000", "-ac", "1", tmp + "/a.wav"], check=True)
subprocess.run(["whisper-cli", "-m", MOD, "-l", os.environ.get("LINGUA", "it"), "-f", tmp + "/a.wav", "-ml", "1", "-sow", "-dtw", "large.v3", "-oj", "-of", tmp + "/p", "-np"], check=True, capture_output=True)
W = []
for s in json.load(open(tmp + "/p.json"))["transcription"]:
    t = s["text"].strip()
    if t and not t.startswith("["): W.append((norm(t), s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000))
C = [(i, j, norm(w)) for i, f in enumerate(frasi) for j, w in enumerate(f)]
T = [None] * len(C)
for a, b, n in difflib.SequenceMatcher(None, [c[2] for c in C], [w[0] for w in W], autojunk=False).get_matching_blocks():
    for k in range(n): T[a + k] = (W[b + k][1], W[b + k][2])
agg = sum(1 for x in T if x); k = 0
while k < len(T):      # parole non riconosciute: tra le vicine, in proporzione alle lettere
    if T[k]: k += 1; continue
    e = k
    while e < len(T) and not T[e]: e += 1
    a = T[k - 1][1] if k else 0.0; b = T[e][0] if e < len(T) else a + .35 * (e - k)
    L = [max(1, len(C[x][2])) for x in range(k, e)]; c = a
    for x, l in zip(range(k, e), L):
        d = (b - a) * l / sum(L); T[x] = (c, c + d); c += d
    k = e
P = [[] for _ in frasi]
for (i, j, _), t in zip(C, T): P[i].append(dict(w=frasi[i][j], t0=round(t[0], 3), t1=round(t[1], 3)))
F = [dict(t0=f[0]["t0"], t1=f[-1]["t1"]) for f in P]
for i in range(1, len(F)):
    F[i]["t0"] = max(F[i]["t0"], F[i - 1]["t1"]); F[i]["t1"] = max(F[i]["t1"], F[i]["t0"] + .2)
open(os.path.join(out, "parole.js"), "w", encoding="utf-8").write("window.PAROLE=" + json.dumps(P, ensure_ascii=False) + ";\n")
open(os.path.join(out, "frasi.js"), "w", encoding="utf-8").write("window.FRASI=" + json.dumps(F) + ";\n")
print(f"parole {len(C)}, agganciate {agg} ({100 * agg // len(C)}%), fine voce {F[-1]['t1']:.2f} s")
if agg < .85 * len(C): print("ATTENZIONE: poche parole agganciate, controlla che il testo sia uguale alla voce")
