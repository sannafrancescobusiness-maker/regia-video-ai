# Cosa scaricare e perché

Mostra questa tabella alla persona dopo `scripts/controlla.sh`, segnando cosa c'è già e cosa manca. Le licenze cambiano: se dubiti, apri il link e controlla. Non è consulenza legale.

## Repository GitHub e skill

| Cosa | A cosa serve | Link | Licenza | Costo |
|---|---|---|---|---|
| **HyperFrames** | Video da pagine HTML: montaggio di parlati, grafiche, render. Include skill e suoni | github.com/heygen-com/hyperframes | Apache-2.0 | Gratis |
| **onetake** | Film animati di alto livello: libreria di movimenti, motion blur, controlli di ritmo | github.com/feitangyuan/onetake | **PolyForm Noncommercial 1.0.0: non commerciale.** Per uso commerciale c'è onetake Pro (onetakemotion.com) | Gratis se non commerciale |
| **three.js + esbuild** | Il 3D dei film animati | github.com/mrdoob/three.js · github.com/evanw/esbuild | MIT | Gratis |
| **whisper.cpp** | Trascrizione parola per parola sul Mac | github.com/ggml-org/whisper.cpp | MIT | Gratis |
| **VoiceStudio** (facoltativo) | Voci generate sul Mac, senza crediti | github.com/debpalash/VoiceStudio | AGPL-3.0 | Gratis |

## Programmi

| Cosa | A cosa serve | Come |
|---|---|---|
| **Homebrew** | Installa gli altri programmi | Comando su brew.sh: chiede la password, lo lancia la persona |
| **ffmpeg, ffmpeg-full** | Legge, taglia e misura video e audio | `brew install ffmpeg ffmpeg-full` |
| **Node** | Fa girare HyperFrames, three.js ed esbuild | `brew install node` |
| **Python 3 e librerie** | Script di suono, analisi e render | `brew install python` poi il comando sotto |
| **whisper-cpp** | Comando per trascrivere | `brew install whisper-cpp` |
| **Modello large-v3** (≈3 GB) | Il più preciso per l'italiano. Chiedi l'ok prima di scaricare | comando sotto |
| **Xcode Command Line Tools** | Swift, per scegliere i fotogrammi delle cover | `xcode-select --install` |
| **yt-dlp** (facoltativo) | Scaricare video di riferimento, solo con permesso e rispettando i diritti | `brew install yt-dlp` |

```bash
python3 -m pip install --user numpy scipy pillow matplotlib fonttools brotli opencv-python playwright
python3 -m playwright install chromium
mkdir -p models && curl -L -o models/ggml-large-v3.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin
npx hyperframes skills
git clone https://github.com/feitangyuan/onetake.git ~/.claude/skills/onetake
```

Dopo aver installato nuove skill va riavviata la sessione di Claude Code.

## Account e servizi

| Cosa | A cosa serve | Costo |
|---|---|---|
| **Claude Code** (app desktop o terminale) | Dirige tutto | Abbonamento o API Anthropic |
| **Claude in Chrome** (estensione) | Usa ElevenLabs e i siti dal Chrome della persona | Incluso, va installata |
| **ElevenLabs** (facoltativo, consigliato) | Voci premium e musica originale. Controlla i diritti commerciali del tuo piano | A crediti: un carattere di voce = un credito; musica circa 15 crediti al secondo (valori visti nell'app) |
| **GPT Image o simili** (facoltativo) | Generare le cover | Secondo il servizio |

## Font

- **Playfair Display** (titoli in corsivo, licenza OFL): `bash scripts/prepara_font.sh <cartella>/assets`.
- **SF Pro** (sottotitoli stile iPhone): si scarica da developer.apple.com/fonts. Leggi i termini di Apple, che ne limitano l'uso; in alternativa usa Inter (OFL).

## Da non distribuire dentro questa skill

Il codice di onetake, le voci, i video altrui e la musica non stanno qui dentro: ognuno li scarica dalla fonte e ne accetta le condizioni. Se ridistribuisci parti di onetake, la sua licenza chiede di includerne i termini.
