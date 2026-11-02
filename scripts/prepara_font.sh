#!/bin/bash
# Scarica Playfair Display corsivo da Google Fonts (licenza OFL) in <cartella>: playfair.css e i file woff2.
set -e; D="${1:?cartella}"; mkdir -p "$D"; UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
curl -sL -A "$UA" "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,600&display=block" -o "$D/playfair.css"
grep -oE "https://fonts.gstatic.com/[^)]+\.woff2" "$D/playfair.css" | sort -u | while read -r u; do curl -sL "$u" -o "$D/$(basename "$u")"; done
sed -i '' -E 's#https://fonts.gstatic.com/[^)]*/([^/)]+\.woff2)#\1#g' "$D/playfair.css"; ls "$D" | wc -l
