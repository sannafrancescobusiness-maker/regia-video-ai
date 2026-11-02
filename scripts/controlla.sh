#!/bin/bash
# Controlla tutto quello che serve per lavorare. Non installa nulla.
c(){ if eval "$2" >/dev/null 2>&1; then printf "  OK     %s\n" "$1"; else printf "  MANCA  %s\n" "$1"; fi; }
echo "Sistema: macOS $(sw_vers -productVersion 2>/dev/null) · $(uname -m)"
echo; echo "PROGRAMMI"
c "Homebrew" "command -v brew"; c "ffmpeg" "command -v ffmpeg"; c "ffmpeg-full" "test -x /opt/homebrew/opt/ffmpeg-full/bin/ffmpeg || test -x /usr/local/opt/ffmpeg-full/bin/ffmpeg"
c "Node e npx" "command -v npx"; c "Python 3" "command -v python3"; c "git" "command -v git"; c "whisper-cli" "command -v whisper-cli"; c "Swift (cover)" "command -v swiftc"; c "yt-dlp (facoltativo)" "command -v yt-dlp"
echo; echo "LIBRERIE PYTHON"
for m in numpy scipy PIL matplotlib fontTools brotli cv2 playwright; do c "$m" "python3 -c 'import $m'"; done
c "Chromium per i render" "ls ~/Library/Caches/ms-playwright 2>/dev/null | grep -q chromium"
echo; echo "MODELLO DI TRASCRIZIONE"
c "ggml-large-v3.bin" "test -f models/ggml-large-v3.bin || test -f \"\$WHISPER_MODEL\" || find \"\$HOME\" -maxdepth 3 -name ggml-large-v3.bin 2>/dev/null | grep -q ."
echo; echo "SKILL E REPOSITORY"
c "HyperFrames (hyperframes, media-use...)" "test -d .agents/skills/hyperframes || test -d .claude/skills/hyperframes || test -d ~/.claude/skills/hyperframes"
c "onetake (licenza non commerciale)" "test -d ~/.claude/skills/onetake || test -d .claude/skills/onetake || test -d ~/.agents/skills/onetake"
echo; echo "FACOLTATIVI"
c "VoiceStudio" "test -d /Applications/VoiceStudio.app"
c "Font SF Pro" "ls /Library/Fonts ~/Library/Fonts 2>/dev/null | grep -qi 'SF-Pro'"
echo; echo "Da controllare a mano: estensione Claude in Chrome, account ElevenLabs."
