#!/usr/bin/env python3
"""Monta la voce finale senza toccarne la velocità: stringe le pause e sostituisce le frasi indicate.
uso: monta_voce.py montaggio.json  (percorsi relativi al file json)
{"base": "eleven/voce.mp3", "uscita": "voce.wav",
 "sostituzioni": [{"da": 3.03, "a": 3.87, "file": "eleven/altra_voce.mp3"}]}
da/a = dove inizia e finisce la frase nella base, anche approssimati: si aggancia alle pause più vicine."""
import json, os, subprocess, sys
import numpy as np
cfg = os.path.abspath(sys.argv[1]); os.chdir(os.path.dirname(cfg)); C = json.load(open(cfg)); SR = 48000
def carica(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, dtype=np.float32).copy()
def rms(x): return float(np.sqrt(np.mean(x ** 2)) + 1e-9)
def attiva(x, soglia=-42):
    h = int(.01 * SR); n = len(x) // h
    return 20 * np.log10(np.array([rms(x[i * h:(i + 1) * h]) for i in range(n)]) + 1e-9) > soglia, h
def taglia(x):
    a, h = attiva(x); i = np.where(a)[0]
    return x[max(0, (i[0] - 1) * h):min(len(x), (i[-1] + 2) * h)]
M = carica(C["base"]); a, h = attiva(M); S = []; i = 0
while i < len(a):
    if not a[i]:
        j = i
        while j < len(a) and not a[j]: j += 1
        if (j - i) * h >= .12 * SR and i > 0: S.append((i * h, j * h))
        i = j
    else: i += 1
SOST = []
for s in C.get("sostituzioni", []):
    p0 = min(S, key=lambda p: abs(p[1] / SR - s["da"])); p1 = min(S, key=lambda p: abs(p[0] / SR - s["a"])); c = taglia(carica(s["file"]))
    c *= rms(M[p0[1]:p1[0]]) / rms(c); np.clip(c, -.98, .98, out=c); SOST.append((p0, p1, c))
    print("sostituisco da", round(p0[1] / SR, 2), "a", round(p1[0] / SR, 2), "con", round(len(c) / SR, 2), "s")
f = int(.012 * SR)
def fade(x):
    x = x.copy(); n = min(f, len(x) // 2)
    if n: x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
    return x
SIL = lambda s: np.zeros(int(s * SR), dtype=np.float32)
P = []; pos = 0
for s, e in S:
    d = (e - s) / SR; salta = False
    for p0, p1, c in SOST:
        if (s, e) == p0: P += [fade(M[pos:s]), SIL(.2)]; pos = e; salta = True
        elif (s, e) == p1: P += [fade(c), SIL(.24)]; pos = e; salta = True
        elif p0[0] < s < p1[0]: salta = True
    if salta: continue
    P += [fade(M[pos:s]), SIL(min(d, .1 if d < .24 else (.16 if d < .42 else .24)))]; pos = e
P.append(fade(M[pos:])); V = np.concatenate(P)
print("durata: da", round(len(M) / SR, 2), "a", round(len(V) / SR, 2), "s")
open("monta.raw", "wb").write(V.astype(np.float32).tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "monta.raw", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "1", C.get("uscita", "voce.wav")], check=True)
os.remove("monta.raw")
