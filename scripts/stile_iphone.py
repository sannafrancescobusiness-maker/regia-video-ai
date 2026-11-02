#!/usr/bin/env python3
"""Libreria dello «stile iPhone» per HyperFrames (video verticali 1080×1920).

Uso tipico (vedi esempio_ads.py):

    import stile_iphone as st
    st.imposta(progetto="ads/video", colore="arancione")
    st.scena("a-casa", corpo_html, script_js, durata=3)      # schermata bianca con vetro, macchie, fluttuare
    st.overlay("a-notifica", corpo_html, script_js)           # grafica sopra la camera
    inserts = st.allinea_fine(inserts, parole, tagli)          # niente pezzetti di clip muta
    st.scrivi_index(...); st.scrivi_sottotitoli(...)

Funzioni JS disponibili dentro gli script di scena/overlay:
    pop(sel, t, {x,y})   comparsa a molla iOS (da 0.72 + sfocatura)
    blurIn(sel, t)        testo che entra sfocato dal basso
    draw(sel, t, durata)  disegna percorsi SVG (frecce: la punta arriva per ultima)
    xOut(sel, t)          X rossa che si rivela (usa XSVG)
    hide(sel, t)          uscita sfocata
    tl                    la timeline GSAP della scena (tempi in secondi locali)
"""
import json
import math
import os
import re
import subprocess

# ------------------------------------------------------------------ colori
# Il CSS base è scritto in blu iOS; imposta() lo ricolora.
PRESET = {
    "blu": None,
    "arancione": [("31,92,255", "255,149,0"), ("#1f5cff", "#ff9500"), ("110,155,255", "255,196,110"), ("25,80,230", "240,115,0"),
                  ("150,185,255", "255,205,130"), ("40,100,255", "255,145,10"), ("20,70,210", "225,95,0"), ("0,30,120", "120,50,0")],
    "verde": [("31,92,255", "52,199,89"), ("#1f5cff", "#28a745"), ("110,155,255", "130,225,150"), ("25,80,230", "30,160,70"),
              ("150,185,255", "170,235,185"), ("40,100,255", "52,199,89"), ("20,70,210", "25,140,60"), ("0,30,120", "0,70,20")],
    "rosso": [("31,92,255", "255,59,48"), ("#1f5cff", "#ff3b30"), ("110,155,255", "255,140,130"), ("25,80,230", "220,40,35"),
              ("150,185,255", "255,175,170"), ("40,100,255", "255,70,60"), ("20,70,210", "200,30,25"), ("0,30,120", "110,0,0")],
    "viola": [("31,92,255", "175,82,222"), ("#1f5cff", "#af52de"), ("110,155,255", "210,160,240"), ("25,80,230", "150,60,200"),
              ("150,185,255", "220,185,245"), ("40,100,255", "175,82,222"), ("20,70,210", "130,45,180"), ("0,30,120", "60,0,90")],
}
MACCHIE = {
    "blu": [("rgba(31,92,255,0.20)", 760), ("rgba(90,200,250,0.24)", 680), ("rgba(175,82,222,0.12)", 620)],
    "arancione": [("rgba(255,149,0,0.22)", 780), ("rgba(255,204,0,0.20)", 680), ("rgba(255,94,58,0.12)", 620)],
    "verde": [("rgba(52,199,89,0.20)", 760), ("rgba(90,200,250,0.20)", 680), ("rgba(255,204,0,0.12)", 620)],
    "rosso": [("rgba(255,59,48,0.18)", 760), ("rgba(255,149,0,0.18)", 680), ("rgba(175,82,222,0.12)", 620)],
    "viola": [("rgba(175,82,222,0.20)", 760), ("rgba(90,200,250,0.20)", 680), ("rgba(255,45,85,0.12)", 620)],
}

CSS_BASE = """
    #root { position: absolute; inset: 0; pointer-events: none; }
    .bg { position: absolute; inset: 0; background: #ffffff; overflow: hidden; }
    .bg.k { background: #000000; }
    /* macchie di colore sfumate dietro il vetro (stile Apple) */
    .blob { position: absolute; border-radius: 50%; }
    .sk { position: absolute; inset: 0; }
    .row { position: absolute; display: flex; align-items: center; gap: 22px; }
    /* cerchio in vetro blu */
    .num {
      width: 96px; height: 96px; border-radius: 50%; flex: none;
      background: radial-gradient(circle at 30% 24%, rgba(255,255,255,0.85) 0%, rgba(150,185,255,0.7) 18%, rgba(40,100,255,0.78) 58%, rgba(20,70,210,0.88) 100%);
      border: 2px solid rgba(255,255,255,0.75);
      box-shadow: inset 0 -6px 14px rgba(255,255,255,0.25), 0 14px 30px rgba(31,92,255,0.35);
      backdrop-filter: blur(16px) saturate(180%);
      display: flex; align-items: center; justify-content: center;
      font-family: "Inter", sans-serif; font-weight: 800; font-size: 56px; line-height: 1; color: #ffffff;
      text-shadow: 0 2px 6px rgba(0,30,120,0.35);
      font-variant-numeric: tabular-nums; text-align: center;
    }
    /* pillola in vetro blu */
    .pill {
      position: relative; display: inline-block; padding: 18px 34px 20px; border-radius: 999px;
      background: linear-gradient(160deg, rgba(110,155,255,0.82) 0%, rgba(31,92,255,0.66) 55%, rgba(25,80,230,0.78) 100%);
      border: 1.5px solid rgba(255,255,255,0.7);
      box-shadow: inset 0 2px 0 rgba(255,255,255,0.75), inset 0 -10px 20px rgba(255,255,255,0.16), 0 18px 40px rgba(31,92,255,0.28);
      backdrop-filter: blur(18px) saturate(180%);
      font-family: "Inter", sans-serif; font-weight: 500; font-size: 46px; color: #ffffff; white-space: nowrap;
      text-shadow: 0 1px 4px rgba(0,30,120,0.3);
    }
    /* riquadro in vetro chiaro */
    .glass {
      background: linear-gradient(160deg, rgba(255,255,255,0.78) 0%, rgba(255,255,255,0.5) 100%);
      border: 2px solid rgba(255,255,255,0.95);
      box-shadow: 0 26px 60px rgba(30,60,140,0.16), inset 0 2px 0 #ffffff, inset 0 -12px 24px rgba(31,92,255,0.05);
      backdrop-filter: blur(26px) saturate(180%);
    }
    .gsvg { filter: drop-shadow(0 22px 40px rgba(30,60,140,0.16)); }
    .cline { position: absolute; left: 0; width: 100%; text-align: center; }
    .serif { font-family: "Playfair Display", serif; font-style: italic; font-weight: 700; color: #1d1d1f; }
    .lbl { font-family: "Playfair Display", serif; font-style: italic; font-size: 54px; color: #1f5cff; }
    .big { font-family: "Inter", sans-serif; font-weight: 900; color: #1d1d1f; letter-spacing: -0.03em; }
    .blue { color: #1f5cff; }
    .red { color: #ff3b3b; }
    .xmark { position: absolute; overflow: visible; opacity: 0; }
    .xmark path { fill: none; stroke: #ff3b30; stroke-width: 12; stroke-linecap: round; }
    .draw { position: absolute; overflow: visible; }
    .draw path, .draw circle, .draw ellipse { fill: none; stroke: #1d1d1f; stroke-width: 8; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }
    .draw.b path, .draw.b ellipse { stroke: #1f5cff; }
    .draw.wh path { stroke: #ffffff; }
    .w { display: inline-block; }
    .dash { position: absolute; inset: -14px -26px; border: 4px dashed #ff3b30; border-radius: 18px; opacity: 0; }
    .ab { position: absolute; }
    @font-face { font-family: "AppleEmoji"; src: local("Apple Color Emoji"); }
    .emo { font-family: "AppleEmoji", sans-serif; line-height: 1; }
    .green { color: #34c759; }
    .wid { position: absolute; border-radius: 44px; padding: 34px 36px; }
    .wt { font-family: "SF Pro Display", "Inter", sans-serif; font-weight: 600; font-size: 44px; color: #1d1d1f; }
    .ws { font-family: "SF Pro Display", "Inter", sans-serif; font-weight: 500; font-size: 34px; color: #6e6e73; }
    @font-face { font-family: "SF Pro Display"; src: url("assets/fonts/SF-Pro-Display-Semibold.otf"); font-weight: 600; }
    @font-face { font-family: "SF Pro Display"; src: url("assets/fonts/SF-Pro-Display-Medium.otf"); font-weight: 500; }
"""

JS = """
    const tl = gsap.timeline({ paused: true });
    // comparsa a molla stile iOS: da un po' più piccolo e sfocato, rimbalzo appena accennato
    function pop(sel, t, from) {
      from = from || {};
      const f = { opacity: 0, scale: 0.72, filter: "blur(10px)" };
      if (from.x) f.x = from.x * 0.6;
      if (from.y) f.y = from.y * 0.6;
      tl.fromTo(sel, f, { opacity: 1, scale: 1, x: 0, y: 0, rotation: 0, filter: "blur(0px)", duration: 0.55, ease: "back.out(1.2)" }, t);
    }
    function blurIn(sel, t) {
      tl.fromTo(sel, { opacity: 0, filter: "blur(10px)", y: 10, scale: 0.97 }, { opacity: 1, filter: "blur(0px)", y: 0, scale: 1, duration: 0.32, ease: "power3.out" }, t);
    }
    function draw(sel, t, d) {
      document.querySelectorAll(sel).forEach(function (p, i) {
        // nelle frecce la punta (secondo tratto) arriva subito dopo la linea
        const isHead = i > 0 && p.parentNode.classList.contains("arw");
        const t0 = isHead ? t + (d || 0.3) * 0.9 : t;
        const dd = isHead ? 0.12 : (d || 0.3);
        // tratteggio come attributo SVG (lunghezza normalizzata a 1): il tratto si disegna da 0 a 100%
        p.setAttribute("pathLength", "1");
        p.setAttribute("stroke-dasharray", "1 1");
        p.setAttribute("stroke-dashoffset", "1");
        tl.set(p, { opacity: 1 }, t0);
        tl.fromTo(p, { attr: { "stroke-dashoffset": 1 } }, { attr: { "stroke-dashoffset": 0 }, duration: dd, ease: isHead ? "power2.out" : "power1.inOut", immediateRender: false }, t0);
      });
    }
    function xOut(sel, t) {
      tl.fromTo(sel, { opacity: 1, clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.12, ease: "power2.out" }, t);
    }
    function hide(sel, t) {
      tl.to(sel, { opacity: 0, filter: "blur(10px)", scale: 0.96, duration: 0.2, ease: "power2.in" }, t);
    }
    // fluttuare morbido con un filo di profondità, come la parallasse dello sfondo di iPhone
    function shake(sel, dur) {
      const el = document.querySelector(sel);
      if (!el) return;
      const c = { t: 0 };
      tl.fromTo(c, { t: 0 }, { t: dur, duration: dur, ease: "none", immediateRender: false, onUpdate: function () {
        const t = c.t;
        gsap.set(el, {
          x: 4 * Math.sin(t * 2 * Math.PI / 5.0),
          y: 8 * Math.sin(t * 2 * Math.PI / 3.6),
          rotationX: 1.6 * Math.sin(t * 2 * Math.PI / 4.2 + 1),
          rotationY: 2.2 * Math.sin(t * 2 * Math.PI / 5.6),
          transformPerspective: 1600,
        });
      } }, 0);
    }
"""

_CFG = {"progetto": ".", "css": CSS_BASE, "macchie": MACCHIE["blu"], "accento": "#1f5cff"}


def imposta(progetto, colore="blu"):
    """Cartella del progetto HyperFrames (contiene assets/ e compositions/) e colore principale."""
    css = CSS_BASE
    for a, b in PRESET.get(colore) or []:
        css = css.replace(a, b)
    _CFG.update(progetto=progetto, css=css, macchie=MACCHIE.get(colore, MACCHIE["blu"]))
    _CFG["accento"] = dict(PRESET.get(colore) or [("#1f5cff", "#1f5cff")]).get("#1f5cff", "#1f5cff")
    os.makedirs(os.path.join(progetto, "compositions"), exist_ok=True)
    os.makedirs(os.path.join(progetto, "assets", "fonts"), exist_ok=True)
    # SF Pro dal Mac, se installato (altrimenti si usa Inter)
    for peso in ("Semibold", "Medium"):
        for base in ("/Library/Fonts", os.path.expanduser("~/Library/Fonts")):
            src = os.path.join(base, f"SF-Pro-Display-{peso}.otf")
            dst = os.path.join(progetto, "assets", "fonts", f"SF-Pro-Display-{peso}.otf")
            if os.path.exists(src) and not os.path.exists(dst):
                subprocess.run(["cp", src, dst])


# ------------------------------------------------------------------ pezzi HTML
XSVG = ('<svg class="xmark" id="{id}" style="{style}" viewBox="0 0 100 100" preserveAspectRatio="none">'
        '<path d="M4 10 L96 90" vector-effect="non-scaling-stroke" /><path d="M96 10 L4 90" vector-effect="non-scaling-stroke" /></svg>')


def freccia(id, style, d, fine, direzione, cls="draw", vb="0 0 400 300", punta=30):
    """Freccia tipo SF Symbols: un percorso `d` che termina in `fine` + punta a chevron simmetrica.
    `direzione` = verso in cui punta all'arrivo (dx, dy). cls: "draw" nero, "draw b" colore, "draw wh" bianco."""
    dx, dy = direzione
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    pts = []
    for a in (math.radians(140), math.radians(-140)):
        rx = ux * math.cos(a) - uy * math.sin(a)
        ry = ux * math.sin(a) + uy * math.cos(a)
        pts.append((fine[0] + rx * punta, fine[1] + ry * punta))
    head = f"M{pts[0][0]:.1f} {pts[0][1]:.1f} L{fine[0]} {fine[1]} L{pts[1][0]:.1f} {pts[1][1]:.1f}"
    return f'<svg class="{cls} arw" id="{id}" style="{style}" viewBox="{vb}"><path d="{d}" /><path d="{head}" /></svg>'


def _macchie(cid):
    h = sum(ord(c) for c in cid)
    out = []
    for i, (col, size) in enumerate(_CFG["macchie"]):
        x = (h * (i + 3) * 97) % 900 - 300
        y = (h * (i + 5) * 61) % 1500 - 200
        out.append(f'<div class="blob" id="{cid}-b{i}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
                   f'background:radial-gradient(circle, {col} 0%, rgba(255,255,255,0) 70%)"></div>')
    return "".join(out)


def _scrivi(cid, html):
    with open(os.path.join(_CFG["progetto"], "compositions", f"{cid}.html"), "w") as f:
        f.write(html)


def scena(cid, corpo, script, nera=False, durata=6):
    """Schermata a tutto schermo: bianca con macchie di colore che si muovono e contenuto che fluttua
    (parallasse iPhone), oppure nera (nera=True) per le frasi forti."""
    bg = '<div class="bg k"></div>' if nera else f'<div class="bg">{_macchie(cid)}</div>'
    extra = "" if nera else f"""
    shake("#{cid}-sk", {durata});
    [0, 1, 2].forEach(function (i) {{
      tl.fromTo("#{cid}-b" + i, {{ x: 0, y: 0 }}, {{ x: (i - 1) * 60, y: (1 - i) * 50, duration: {durata}, ease: "none" }}, 0);
    }});"""
    _scrivi(cid, f"""<template>
  <style>{_CFG['css']}  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-layout-allow-overlap>
    {bg}
    <div class="sk" id="{cid}-sk">
{corpo}
    </div>
  </div>
  <script>
    (function () {{{JS}
{script}{extra}
    window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
""")


def overlay(cid, corpo, script):
    """Grafica trasparente sopra la camera (notifiche, badge, moduli). Rispetta le zone vietate."""
    css = _CFG["css"].replace(".bg { position: absolute; inset: 0; background: #ffffff; overflow: hidden; }", ".bg { display: none; }")
    _scrivi(cid, f"""<template>
  <style>{css}  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-layout-allow-overlap>
{corpo}
  </div>
  <script>
    (function () {{{JS}
{script}
    window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
""")


# ------------------------------------------------------------------ analisi
def parole_da_whisper(json_whisper):
    """Converte l'output di `whisper-cli -ml 1 -sow -ojf` in [{id,text,start,end}]."""
    d = json.load(open(json_whisper))
    ws = [s for s in d["transcription"] if s["text"].strip()]
    return [{"id": f"w{i}", "text": s["text"].strip(), "start": s["offsets"]["from"] / 1000, "end": s["offsets"]["to"] / 1000}
            for i, s in enumerate(ws)]


def trova_tagli(video, soglia=4.0):
    """Tempi (s) dei cambi di inquadratura, con ffmpeg scdet."""
    out = subprocess.run(["ffmpeg", "-nostats", "-i", video, "-vf", "scale=270:480,scdet=threshold=0,metadata=print", "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    t, tagli = None, []
    for riga in out.splitlines():
        m = re.search(r"pts_time:([\d.]+)", riga)
        if m:
            t = float(m.group(1))
        m = re.search(r"scd\.score=([\d.]+)", riga)
        if m and t is not None and float(m.group(1)) > soglia and t > 0.1:
            tagli.append(round(t, 3))
    return tagli


def allinea_fine(inserts, parole, tagli=(), finestra=0.3):
    """Ogni schermata seguita dalla camera finisce sul taglio di inquadratura vicino (entro `finestra` s)
    o, se non c'è, quando ricomincia il parlato (prima parola −0,03 s). inserts = [(id, inizio, fine, tipo)]."""
    ins = sorted(inserts, key=lambda r: r[1])
    out = []
    for i, (cid, a, b, k) in enumerate(ins):
        nxt = ins[i + 1][1] if i + 1 < len(ins) else 1e9
        if nxt - b > 0.001:
            vicini = [c for c in tagli if b - 0.001 <= c <= b + finestra and c <= nxt]
            if vicini:
                b = vicini[0]
            else:
                w = next((p["start"] for p in parole if p["start"] >= b - 0.02), None)
                if w is not None and w < nxt:
                    b = max(b, w - 0.03)
        out.append((cid, a, round(b, 4), k))
    return out


# ------------------------------------------------------------------ timeline
def scrivi_index(video, durata, inserts, suoni, musica=None, vol_musica=0.1, vol_video=1.0, fps_nota=""):
    """index.html: video del cliente/girato + schermate (tipo «w» bianca, «o» overlay) + sottotitoli + musica + suoni.
    suoni = [((nome, src, durata, volume), tempo), ...]."""
    hosts = "\n".join(
        f'      <div id="{cid}" class="ins" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
        f'data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{5 if k == "w" else 6}" data-track-kind="graphics" '
        f'data-width="1080" data-height="1920"></div>' for cid, a, b, k in inserts)
    sfx = "\n".join(
        f'      <audio id="sx-{i:02d}" class="clip" src="{c[1]}" data-start="{t:.3f}" data-duration="{c[2]:.2f}" '
        f'data-track-index="{20 + i % 4}" data-volume="{c[3]}"></audio>' for i, (c, t) in enumerate(suoni, 1))
    mus = (f'      <audio id="musica" class="clip" src="{musica}" data-start="0" data-duration="{durata:.4f}" data-track-index="2" '
           f'data-volume="{vol_musica}" data-fade-in="0.6" data-fade-out="1.2"></audio>') if musica else ""
    html = f"""<!doctype html>
<html lang="it" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #girato {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 1; }}
      .ins {{ z-index: 5; }}
      #captions {{ z-index: 10; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{durata:.4f}" data-width="1080" data-height="1920">
      <video id="girato" class="clip" src="{video}" data-start="0" data-duration="{durata:.4f}" data-track-index="0" data-has-audio="true" data-volume="{vol_video}" playsinline></video>
{mus}
{hosts}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{durata:.4f}" data-track-index="7" data-track-kind="captions" data-width="1080" data-height="1920"></div>
{sfx}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    with open(os.path.join(_CFG["progetto"], "index.html"), "w") as f:
        f.write(html)
    mancanti = [s for s in re.findall(r'src="(assets/[^"]+)"', html) if not os.path.exists(os.path.join(_CFG["progetto"], s))]
    if mancanti:
        print("ATTENZIONE, file mancanti:", sorted(set(mancanti)))


def scrivi_sottotitoli(parole, inserts, y=1330, gruppi_camera=False, y_camera=1300):
    """Parole singole fluttuanti (SF Pro) sulle schermate bianche (tipo «w»). Con gruppi_camera=True aggiunge
    anche i sottotitoli in camera stile iPhone (bianchi, ombra morbida, parola detta che si accende):
    da usare solo se il girato NON ha già sottotitoli impressi."""
    win = [(a, b) for cid, a, b, k in inserts if k == "w"]
    blocc = [(a, b) for cid, a, b, k in inserts]
    singole, gruppi, g = [], [], []
    for p in parole:
        w = next(((a, b) for a, b in win if a - 0.02 <= p["start"] < b), None)
        if w:
            singole.append({"id": p["id"], "text": p["text"].rstrip(",:"), "on": max(p["start"], w[0]), "win": w})
        elif gruppi_camera and not any(a <= p["start"] < b for a, b in blocc):
            g.append(p)
            if len(g) == 3 or p["text"].endswith((".", "?", "!")):
                gruppi.append(g); g = []
    if g:
        gruppi.append(g)
    for i, s in enumerate(singole):
        nxt = singole[i + 1]["on"] if i + 1 < len(singole) and singole[i + 1]["win"] == s["win"] else s["win"][1]
        s["off"] = round(min(nxt, s["win"][1]), 3)
    G = []
    for i, g in enumerate(gruppi):
        start = g[0]["start"] - 0.05
        end = min(g[-1]["end"] + 0.15, gruppi[i + 1][0]["start"] - 0.05) if i + 1 < len(gruppi) else g[-1]["end"] + 0.3
        for a, b in blocc:
            if start < b and a < end:
                end = min(end, a) if start < a else end
        G.append({"id": f"cg{i}", "start": round(start, 3), "end": round(end, 3), "words": [{"id": p["id"], "on": p["start"]} for p in g]})
    items = "\n".join(f'    <div class="one" id="one-{s["id"]}"><span>{s["text"]}</span></div>' for s in singole)
    items += "\n" + "\n".join(
        f'    <div class="cg" id="{x["id"]}">' + " ".join(f'<span class="cw" id="cw-{w["id"]}">{next(p["text"] for p in parole if p["id"] == w["id"])}</span>' for w in x["words"]) + "</div>"
        for x in G)
    S = [{"id": s["id"], "on": round(s["on"], 3), "off": s["off"]} for s in singole]
    html = f"""<template>
  <style>
    @font-face {{ font-family: "SF Pro Display"; src: url("assets/fonts/SF-Pro-Display-Medium.otf"); font-weight: 500; }}
    @font-face {{ font-family: "SF Pro Display"; src: url("assets/fonts/SF-Pro-Display-Semibold.otf"); font-weight: 600; }}
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .one {{ position: absolute; left: 0; top: {y}px; width: 100%; text-align: center; font-family: "SF Pro Display", "Inter", sans-serif;
      font-weight: 500; font-size: 56px; line-height: 1; color: #1d1d1f; opacity: 0; visibility: hidden; }}
    .cg {{ position: absolute; left: 90px; top: {y_camera}px; width: 900px; text-align: center; opacity: 0; visibility: hidden; }}
    .cw {{ display: inline-block; margin: 0 6px; font-family: "SF Pro Display", "Inter", sans-serif; font-weight: 600; font-size: 66px;
      line-height: 1.1; color: #fff; opacity: 0.5; text-shadow: 0 2px 4px rgba(0,0,0,0.35), 0 8px 28px rgba(0,0,0,0.45); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{items}
  </div>
  <script>
    (function () {{
      const S = {json.dumps(S)};
      const G = {json.dumps(G)};
      const tl = gsap.timeline({{ paused: true }});
      S.forEach(function (s) {{
        const el = document.getElementById("one-" + s.id);
        const d = Math.max(0.1, s.off - s.on);
        tl.set(el, {{ visibility: "visible" }}, s.on);
        tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: Math.min(0.08, d / 2), ease: "power2.out" }}, s.on);
        tl.fromTo(el, {{ y: 7, rotation: -0.6 }}, {{ y: -7, rotation: 0.6, duration: d, ease: "sine.inOut" }}, s.on);
        tl.set(el, {{ opacity: 0, visibility: "hidden" }}, s.off);
      }});
      G.forEach(function (g) {{
        const el = document.getElementById(g.id);
        if (g.end - g.start < 0.12) return;
        tl.set(el, {{ visibility: "visible" }}, g.start);
        tl.fromTo(el, {{ opacity: 0, y: 14, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "power3.out" }}, g.start);
        g.words.forEach(function (w) {{ tl.fromTo("#cw-" + w.id, {{ opacity: 0.5 }}, {{ opacity: 1, duration: 0.1 }}, w.on); }});
        tl.to(el, {{ opacity: 0, duration: 0.08 }}, g.end - 0.08);
        tl.set(el, {{ visibility: "hidden" }}, g.end);
      }});
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""
    with open(os.path.join(_CFG["progetto"], "compositions", "captions.html"), "w") as f:
        f.write(html)


# ------------------------------------------------------------------ suoni pronti (cartelle assets/sfx e assets/sfx8)
WS = ("whoosh-short", "assets/sfx/whoosh-short.mp3", 0.5, 0.2)      # entrata schermata
WH = ("whoosh", "assets/sfx/whoosh.mp3", 0.57, 0.13)                # passaggio
POP = ("pop", "assets/sfx/pop.mp3", 0.7, 0.24)                      # comparsa
CLK = ("click", "assets/sfx/click.mp3", 0.37, 0.3)                  # X, interruttore, pulsante
SOFT = ("click-soft", "assets/sfx/click-soft.mp3", 0.37, 0.32)      # dettaglio
IMP = ("impact", "assets/sfx/impact-bass-1.mp3", 0.9, 0.2)          # numero grande, timbro
PING = ("ping", "assets/sfx/ping.mp3", 0.8, 0.18)                   # dato rivelato
SPK = ("sparkle", "assets/sfx/sparkle.mp3", 1.2, 0.14)              # momento «wow»
CHIME = ("chime", "assets/sfx/chime.mp3", 1.5, 0.2)                 # conferma
NOTIF = ("notification", "assets/sfx/notification.mp3", 1.6, 0.35)  # notifica, CTA
TYPE = ("key-press", "assets/sfx/key-press.mp3", 0.4, 0.22)         # tasto
TYPING = ("typing", "assets/sfx/typing.mp3", 1.2, 0.14)             # contatore/testo che si scrive
ERR = ("error", "assets/sfx/error.mp3", 0.6, 0.12)                  # problema
PEN = ("tratto", "assets/sfx8/tratto.mp3", 0.38, 0.3)               # freccia/cerchio che si disegna
BOL = ("bolla", "assets/sfx8/bolla.mp3", 0.18, 0.3)                 # bollicine
TICK = ("tick", "assets/sfx8/tick.mp3", 0.05, 0.24)                 # cascate
