#!/usr/bin/env python3
"""Barre di avanzamento dei lavori lunghi (trascrizioni, conversioni, render): http://localhost:8765
I lavori sono elencati in lavori.json: [{"nome", "tipo": ffmpeg|whisper|hyperframes|percento, "file", "totale" (s, solo ffmpeg), "inizio" (epoch)}]"""
import http.server, json, os, re, time

DIR = os.path.dirname(os.path.abspath(__file__))

def percento(l):
    try:
        txt = open(l["file"], errors="ignore").read()
    except FileNotFoundError:
        return 0.0
    if l["tipo"] == "ffmpeg":
        if "progress=end" in txt:
            return 100.0
        v = re.findall(r"out_time_us=(\d+)", txt)
        return min(99.9, int(v[-1]) / 1e6 / l["totale"] * 100) if v else 0.0
    txt = txt[-20000:]
    if l["tipo"] == "whisper":
        if "total time" in txt:
            return 100.0
        t = re.findall(r"--> (\d+):(\d+):(\d+\.\d+)\]", txt)   # ultimo punto trascritto / durata dell'audio
        if t and l.get("totale"):
            h, m, sec = t[-1]
            return min(99.9, (int(h) * 3600 + int(m) * 60 + float(sec)) / l["totale"] * 100)
        v = re.findall(r"progress =\s*(\d+)%", txt)
    elif l["tipo"] == "hyperframes":
        v = re.findall(r'"pct":\s*(\d+)', txt)
    else:
        v = re.findall(r"(\d+(?:\.\d+)?)\s*%", txt)
    return float(v[-1]) if v else 0.0

def stato():
    try:
        lavori = json.load(open(os.path.join(DIR, "lavori.json")))
    except Exception:
        lavori = []
    out, ora = [], time.time()
    for l in lavori:
        p = percento(l)
        trascorso = ora - l.get("inizio", ora)
        eta = trascorso * (100 - p) / p if 1 <= p < 100 else None
        out.append({"nome": l["nome"], "pct": round(p, 1), "trascorso": int(trascorso), "eta": int(eta) if eta else None})
    return out

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=DIR, **k)
    def do_GET(self):
        if self.path.startswith("/stato.json"):
            b = json.dumps(stato()).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        else:
            super().do_GET()
    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
