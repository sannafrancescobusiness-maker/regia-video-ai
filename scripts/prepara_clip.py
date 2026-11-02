#!/usr/bin/env python3
"""Prepara i pezzi di video per la stanza a cubetti, incorporati in file .js dentro comp/assets.
uso: prepara_clip.py clip.json cartella_assets
{"primo": ["video.mp4", 94], "recente": ["altro.mp4", 86], "muro": [["a.mp4", 10], "...8 in tutto"], "ads": [["x.mp4", 13], ["y.mp4", 6]]}"""
import base64, glob, json, os, subprocess, sys, tempfile
C = json.load(open(sys.argv[1])); O = sys.argv[2]; os.makedirs(O, exist_ok=True)
def pezzo(v, t, dur, fps, w, h, q):
    d = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-t", str(dur), "-i", v, "-vf", f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}", "-q:v", str(q), d + "/%03d.jpg"], check=True)
    return ["data:image/jpeg;base64," + base64.b64encode(open(f, "rb").read()).decode() for f in sorted(glob.glob(d + "/*.jpg"))]
def scrivi(n, var, val):
    open(os.path.join(O, n + ".js"), "w").write(f"window.{var}=" + json.dumps(val) + ";\n"); print(n, os.path.getsize(os.path.join(O, n + ".js")) // 1024, "KB")
scrivi("primo", "PRIMO", pezzo(*C["primo"], 6, 12, 360, 640, 6)); scrivi("recente", "RECENTE", pezzo(*C["recente"], 6, 12, 360, 640, 6))
scrivi("muro", "MURO", [pezzo(v, t, 1.25, 8, 216, 384, 7)[:10] for v, t in C["muro"]]); scrivi("ads", "ADS", [pezzo(v, t, 3, 12, 360, 640, 6)[:36] for v, t in C["ads"]])
