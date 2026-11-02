#!/usr/bin/env python3
"""Esempio di suono completo: si copia in <progetto>/audio/ e si adatta. Richiede onetake (sfx_palette) e HyperFrames (suoni).
Effetti registrati (libreria HyperFrames, licenza Pixabay) con materiali sintetici, in una stanza.
La canzone originale (ElevenLabs Music) è allineata al film e si abbassa da sola sotto la voce."""
import json, os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.expanduser("~/.claude/skills/onetake/scripts"))
from sfx_palette import Score, air, glass, wood, sub, bubble, SR
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(HERE + "/events.json")); DUR = D["dur"] + .4; SEZ = D["sezioni"]
LIB = next(p for p in [os.environ.get("SFX_DIR", ""), ".agents/skills/media-use/audio/assets/sfx/", ".claude/skills/media-use/audio/assets/sfx/", "../.agents/skills/media-use/audio/assets/sfx/", "../.claude/skills/media-use/audio/assets/sfx/"] if p and os.path.isdir(p))
def sf(nome, cerca=-42):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", nome if nome.startswith("/") else LIB + nome, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, dtype=np.float32).copy()
    h = int(.005 * SR); e = np.array([np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(0, len(x) - h, h)]); on = np.where(20 * np.log10(e + 1e-9) > cerca)[0]
    x = x[max(0, on[0] * h - h):] if len(on) else x   # via il silenzio iniziale: il suono deve partire sull'immagine
    return x / (np.abs(x).max() + 1e-6)
def corto(x, d):
    x = x[:int(d * SR)].copy(); f = min(len(x), int(.03 * SR)); x[-f:] *= np.linspace(1, 0, f); return x
def tono(x, r):  # cambia altezza ricampionando
    return np.interp(np.arange(0, len(x), r), np.arange(len(x)), x).astype(np.float32)
W = sf("whoosh.mp3"); WC = sf("whoosh-cinematic.mp3"); WS = sf("whoosh-short.mp3"); I1 = sf("impact-bass-1.mp3"); I2 = sf("impact-bass-2.mp3"); RIS = sf("riser.mp3")
PO = sf("pop.mp3"); PI = sf("ping.mp3"); CH = sf("chime.mp3"); NT = sf("notification.mp3"); ER = corto(sf("error.mp3"), .42); SP = sf("sparkle.mp3"); CL = sf("click.mp3"); CS = sf("click-soft.mp3"); KP = sf("key-press.mp3"); TY = sf("typing.mp3")
GL = [sf(f"glitch-{i}.mp3") for i in (1, 2, 3)]; BO = I2
r = np.random.default_rng(5); s = Score(dur=DUR, T60=.8); pl = s.place
for e in D["ev"]:
    k, t, a, pan = e["k"], e["t"], e.get("a", 1), e.get("pan", 0); d = e.get("d", .5)
    if k == "colpo":
        pl(I1, t - .005, .7 * a, 0, .22); pl(sub(50, .7), t, .42 * a, 0, .08); pl(corto(GL[0], .12), t, .12 * a, 0, .15)
    elif k == "colpoM":
        pl(I2, t, .55 * a, 0, .3); pl(BO, t, .32 * a, 0, .3); pl(corto(SP, .9), t + .02, .16 * a, 0, .5)
    elif k == "accento":
        pl(corto(tono(WS, 1.25), .2), t - .05, .1 * a, 0, .25); pl(CS, t, .1 * a, 0, .15)
    elif k == "clic":
        pl(corto(GL[int(t * 10) % 3], .08), t, .14 * a, pan, .18); pl(CL, t, .14 * a, pan, .12)
    elif k == "riser":
        q = corto(RIS, 1.1); pl(q, e["fine"] - len(q) / SR, .34 * a, 0, .35)
    elif k == "bolla":
        pl(tono(PO, r.uniform(.85, 1.35)), t, r.uniform(.12, .22) * a, pan, .22)
    elif k == "ping":
        pl(PI, t, .26 * a, 0, .38); pl(corto(NT, .4), t, .1 * a, .2, .3)
    elif k == "cade":
        pl(corto(tono(WC, 1.3), d + .2), t, .3 * a, 0, .3)
    elif k == "barra":
        pl(corto(tono(WS, 1.5), .22), t, .3 * a, 0, .2)
    elif k == "digita":
        pl(corto(TY, d), t, .3 * a, -.05, .12)
    elif k == "copia":
        pl(KP, t, .4 * a, 0, .15); pl(CL, t + .03, .28 * a, 0, .15); pl(tono(PO, 1.1), t + .04, .18 * a, 0, .2)
    elif k == "clone":
        pl(corto(tono(WS, 1 + e["i"] * .06), .26), t, .2 * a, pan, .22)
    elif k == "tic":
        pl(wood(330 + e["i"] * 42, .05), t, .3 * a, 0, .16); pl(glass(1100 + e["i"] * 95, .13, 1), t, .05 * a, 0, .3)
    elif k == "whoosh":
        q = corto(WC if d >= .6 else W, d + .25); pl(q, t, .5 * a, -.3 if not pan else pan, .3, pan_to=.3)
    elif k == "pioggia":
        pl(BO, t + .25, .46 * a, 0, .35)
        for i in range(250):
            u = r.uniform() ** .8; pl(wood(r.uniform(110, 300), r.uniform(.05, .09)), t + u * d, r.uniform(.03, .1) * a, r.uniform(-.6, .6), .3)
        pl(sub(44, d + .4), t + .2, .26 * a, 0, .12)
    elif k == "errore":
        pl(tono(ER, r.uniform(.94, 1.06)), t, .24 * a, pan, .22)
    elif k == "orologio":
        for i in range(26):
            u = 1 - (1 - i / 26) ** 2.2; pl(wood(620, .03), t + u * d, .12 * a, pan, .12)
    elif k == "blocchi":
        for i in range(16): pl(wood(r.uniform(130, 260), .08), t + r.uniform(0, .5), r.uniform(.07, .16) * a, pan + r.uniform(-.2, .2), .25)
        pl(I2, t + .32, .22 * a, pan, .25)
    elif k == "schermo":
        pl(corto(GL[1], .22), t, .22 * a, 0, .22); pl(glass(880, .5, .7), t + .02, .11 * a, 0, .4)
    elif k == "brucia":
        pl(corto(GL[2], .4), t - .03, .36 * a, 0, .25); pl(air(.42, 500, 5200, 1.1, .35), t - .05, .26 * a, 0, .3); pl(I2, t, .3 * a, 0, .2)
    elif k == "clip":
        for i in range(6): pl(tono(PO, 1 + i * .08), t + i * .05, .13 * a, -.3 + i * .12, .18)
    elif k == "taglio":
        pl(corto(GL[0], .26), t, .36 * a, 0, .2); pl(I1, t + .02, .34 * a, 0, .2); pl(wood(160, .1), t + .24, .22 * a, -.2, .25)
    elif k == "salto":
        pl(tono(PO, .78), t, .24 * a, pan, .2); pl(wood(170, .09), t, .2 * a, pan, .2)
    elif k == "ciak":
        pl(wood(1250, .045), t, .66 * a, pan, .3); pl(wood(620, .07), t, .44 * a, pan, .3); pl(CL, t, .4 * a, pan, .22); pl(air(.05, 4200, 7000, 1), t, .28 * a, pan, .25); pl(sub(90, .16), t, .24 * a, pan, .1)
    elif k == "magia":
        pl(corto(SP, .8), t, .26 * a, pan, .45); pl(tono(PO, 1.2), t, .18 * a, pan, .2)
    elif k == "scheda":
        pl(CS, t, .22 * a, pan, .2); pl(corto(tono(WS, 1.4), .16), t, .12 * a, pan, .2)
    elif k == "monete":
        for i in range(70): pl(glass(r.uniform(2300, 4600), r.uniform(.08, .18), 1), t + r.uniform(0, d), r.uniform(.014, .05) * a, pan + r.uniform(-.3, .3), .3)
        for i in range(30): pl(wood(r.uniform(420, 760), .05), t + r.uniform(0, d), r.uniform(.04, .1) * a, pan + r.uniform(-.3, .3), .25)
        pl(corto(CH, 1), t + d * .55, .16 * a, pan, .45)
    elif k == "libri":
        for i in range(33): pl(wood(r.uniform(150, 240), .09), t + d * i / 33, r.uniform(.09, .16) * a, pan, .22)
    elif k == "chiudi":
        pl(wood(190, .13), t, .36 * a, pan, .32); pl(I2, t, .24 * a, pan, .25)
    elif k == "sale":
        q = corto(RIS, .55); pl(q, t, .26 * a, .3, .3); pl(corto(CH, 1), t + .42, .22 * a, .3, .45); pl(I2, t + .42, .26 * a, .3, .25)
    elif k == "stacco":
        pl(I2, t, .55 * a, 0, .35); pl(corto(GL[2], .14), t - .01, .22 * a, 0, .1)
    elif k == "conta":
        n = int(e["n"])
        for i in range(n): pl(wood(230 + r.uniform(-40, 60), .05), t + d * i / n, r.uniform(.07, .14) * a, pan + r.uniform(-.1, .1), .2)
        pl(I2, t, .3 * a, pan, .25)
    elif k == "volo":
        pl(WC, t, .55 * a, .5, .4, pan_to=-.4); pl(air(d, 200, 3400, 1.1, .5), t, .3 * a, .5, .4, pan_to=-.4)
    elif k == "risucchio":
        q = np.flip(corto(WC, d + .1)).copy(); pl(q, t, .5 * a, -.2, .35, pan_to=.1)
        for i in range(120):
            u = r.uniform() ** .75; pl(wood(r.uniform(140, 340), r.uniform(.04, .07)), t + u * d, r.uniform(.02, .07) * a, r.uniform(-.6, .6), .25)
    elif k == "invio":
        pl(PI, t, .36 * a, 0, .35); pl(corto(CH, 1.1), t + .03, .2 * a, 0, .5); pl(tono(PO, 1.2), t, .22 * a, 0, .2)
    else:
        print("evento senza suono:", k)
s.write(HERE + "/sfx.wav", peak_db=-7)
# canzone: la sua pausa cade su «Ho contato tutto», la ripartenza sulla stanza finita
SONG_SILENZIO = 64.9   # secondo della canzone in cui cade la sua pausa: misuralo sulla tua canzone
off = SONG_SILENZIO - SEZ["vuoto"]; n = int(DUR * SR)
print("canzone da", round(off, 2), "s")
def st(p, ss=0):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout, dtype=np.float32).copy().reshape(-1, 2)
    y = np.zeros((n, 2), dtype=np.float32); m = min(n, len(x)); y[:m] = x[:m]; return y
MU = st(HERE + "/canzone.wav", off); FX = st(HERE + "/sfx.wav"); VO = st(HERE + "/../voce/voce.wav")
# si abbassa da sola sotto la voce
h = int(.01 * SR); e = np.sqrt(np.convolve(VO[:, 0] ** 2, np.ones(h) / h, "same")); on = (e > 10 ** (-46 / 20)).astype(np.float32)
env = np.zeros(n, dtype=np.float32); v = 0.; att = 1 - np.exp(-1 / (.03 * SR)); rel = 1 - np.exp(-1 / (.28 * SR))
for i in range(n):
    c = on[i]; v += (c - v) * (att if c > v else rel); env[i] = v
gain_db = -7.5 + (-15.5 + 7.5) * env
f0 = int(.06 * SR); fade = np.ones(n, dtype=np.float32); fade[:f0] = np.linspace(0, 1, f0); f1 = int(1.1 * SR); fade[-f1:] = np.linspace(1, 0, f1)
g = 10 ** (gain_db / 20) * fade
MIX = VO * 1.0 + FX * .92 + MU * g[:, None]
open(HERE + "/mix.raw", "wb").write(MIX.astype(np.float32).tobytes())
base = ["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", HERE + "/mix.raw"]
subprocess.run(base + ["-af", "alimiter=limit=.8:level=false", "-c:a", "pcm_s16le", HERE + "/mix_t.wav"], check=True)
o = subprocess.run(["ffmpeg", "-hide_banner", "-i", HERE + "/mix_t.wav", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", o)[-1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", HERE + "/mix_t.wav", "-af", f"volume={-16 - I}dB,alimiter=limit=.7:level=false", "-ar", "48000", "-c:a", "pcm_s16le", HERE + "/mix.wav"], check=True)
os.remove(HERE + "/mix_t.wav"); os.remove(HERE + "/mix.raw")
print("mix pronto, partiva da", I, "LUFS")
