#!/bin/bash
# Analisi di un girato: info tecniche, griglia di fotogrammi, trascrizione parola per parola, tagli, volume.
# Uso: bash analizza.sh "<video>" "<cartella di uscita>" [modello whisper]
set -e
VIDEO="$1"; OUT="$2"
MODELLO="${3:-$HOME/editing video/models/ggml-large-v3.bin}"
mkdir -p "$OUT"
FF=ffmpeg; [ -x /opt/homebrew/opt/ffmpeg-full/bin/ffmpeg ] && FF=/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg

echo "== 1/5 informazioni"
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate,color_transfer -of compact=p=0 "$VIDEO" | tee "$OUT/info.txt"

echo "== 2/5 griglia (2 fotogrammi al secondo, con il tempo scritto sopra)"
$FF -v error -y -i "$VIDEO" -vf "fps=2,scale=180:320,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=14:fontcolor=yellow:box=1:boxcolor=black,tile=10x6" -frames:v 1 "$OUT/griglia.jpg" \
  || $FF -v error -y -i "$VIDEO" -vf "fps=2,scale=180:320,tile=10x6" -frames:v 1 "$OUT/griglia.jpg"

echo "== 3/5 trascrizione (può richiedere qualche minuto)"
ffmpeg -v error -y -i "$VIDEO" -ar 16000 -ac 1 "$OUT/audio.wav"
whisper-cli -m "$MODELLO" -l it -ml 1 -sow -ojf -of "$OUT/parole" -f "$OUT/audio.wav" >/dev/null 2>&1
python3 - "$OUT" <<'EOF'
import json, sys
o = sys.argv[1]
d = json.load(open(f"{o}/parole.json"))
ws = [s for s in d["transcription"] if s["text"].strip()]
w = [{"id": f"w{i}", "text": s["text"].strip(), "start": s["offsets"]["from"] / 1000, "end": s["offsets"]["to"] / 1000} for i, s in enumerate(ws)]
json.dump(w, open(f"{o}/words.json", "w"), ensure_ascii=False)
print(" ".join(f"{x['text']}[{x['start']:.2f}]" for x in w))
EOF

echo "== 4/5 tagli di inquadratura"
ffmpeg -nostats -i "$VIDEO" -vf "scale=270:480,scdet=threshold=0,metadata=print" -an -f null - 2>&1 \
  | grep -o "pts_time:[0-9.]*\|scd.score=[0-9.]*" | paste - - | awk -F'[:=\t]' '$4>4 && $2>0.1 {printf "%.3f ", $2}' | tee "$OUT/tagli.txt"; echo

echo "== 5/5 volume (LUFS) e silenzi"
ffmpeg -nostats -i "$VIDEO" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
echo "silenzi sotto -45 dB: $(ffmpeg -i "$OUT/audio.wav" -af silencedetect=n=-45dB:d=0.25 -f null - 2>&1 | grep -c silence_start) (0 = c'è un sottofondo/musica)"
echo "fatto: $OUT/griglia.jpg, $OUT/words.json, $OUT/tagli.txt"
