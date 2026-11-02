# La stanza a cubetti: modello di film 16:9

Un film completo: si parte dal muro dei video veri, poi commenti, prompt copiato, errori con il nome scritto sopra, poi una stanza 3D che si costruisce con quegli errori e alla fine si richiude in un cubo. È un punto di partenza: cambia testo, personaggi, colori e scene.

## Preparazione

```bash
mkdir -p comp/assets comp/vendor audio voce
cp <skill>/assets/stanza/comp.html <skill>/assets/stanza/look.json comp/
cp ~/.claude/skills/onetake/lib/motion.js comp/          # richiede onetake: rispettane la licenza
cp <skill>/assets/stanza/three-entry.js comp/vendor/
(cd comp/vendor && npm init -y >/dev/null && npm i three@0.180.0 esbuild@0.25.10 && npx esbuild three-entry.js --bundle --format=iife --minify --outfile=three.bundle.js)
bash <skill>/scripts/prepara_font.sh comp/assets
python3 <skill>/scripts/prepara_clip.py clip.json comp/assets
python3 <skill>/scripts/allinea.py voce/voce.wav copy.txt comp
python3 ~/.claude/skills/onetake/scripts/look.py apply comp/look.json comp/comp.html
```

## Cosa cambiare in `comp.html`

- `ORE, GIORNI, MSG, PROVE`: i numeri veri.
- `CUE`: i testi. Ogni voce indica frase e numero di parola nel copy (`f`, indice). `copy_esempio.txt` è il testo su cui è stato costruito: se la struttura del tuo è diversa, adatta `CUE`, `K` (camera) e i tempi con `T(frase, parola)`.
- `FRAN`, `PC`, `CB`: i personaggi, disegnati carattere per carattere. Ridisegna il protagonista sulla persona.
- `NOTE`: gli errori veri da scrivere sui cubi. Chiedili alla persona.
- `anim()` e `disegnaSchermo()`: quello che appare nel monitor.

## Controllo, suono, render

```bash
cp <skill>/scripts/dump_events.py <skill>/scripts/score_esempio.py audio/
python3 ~/.claude/skills/onetake/scripts/stills.py comp/comp.html --times 1,6,10,30,50,70 --cols 3 --out prova.png
python3 audio/dump_events.py && python3 audio/score_esempio.py
python3 ~/.claude/skills/onetake/scripts/render.py comp/comp.html --out bozza.mp4 --sfx audio/mix.wav --gpu --workers 4
python3 ~/.claude/skills/onetake/scripts/render.py comp/comp.html --out finale.mp4 --sfx audio/mix.wav --gpu --workers 4 --fps 60 --crf 16
```

La canzone va in `audio/canzone.wav`, la voce in `voce/voce.wav`.
