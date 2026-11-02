# Il suono

Il suono tiene incollati quanto l'immagine. Non puoi ascoltarlo: misura ciò che si misura e fatti dire il resto.

## Effetti

- Usa i suoni registrati di HyperFrames: `.agents/skills/media-use/audio/assets/sfx/` (licenza Pixabay, vedi `CREDITS.md`). Puoi aggiungerne con `media-use`, controllando la licenza.
- **Togli il silenzio iniziale**: molti partono in ritardo (chime 0,4 s, ping 0,3 s, error 0,6 s). `scripts/score_esempio.py` lo fa da solo.
- **Stratifica**: un impatto è basso + corpo + un pizzico di glitch.
- **Una stanza sola**: stesso riverbero per tutti, altrimenti sembrano incollati sopra.
- **Varia l'altezza** nelle raffiche, così non sembra lo stesso suono ripetuto.
- **Dosa**: gli impatti forti sono pochi. Se due suoni cadono entro 40 ms, tienine uno.

## Da dove partono

Fai uscire gli eventi dalla composizione (`window.__events()`), con `scripts/dump_events.py`: se cambia la voce, i suoni seguono da soli.

## Musica

- **Licenza chiara.** Una canzone protetta non si inserisce di tua iniziativa: se la porta la persona, avvisala dei rischi sui social.
- **ElevenLabs Music** crea un brano originale su misura. Costo visibile prima di generare (circa 15 crediti al secondo nelle nostre prove), e la durata può uscire diversa da quella chiesta: misura il file. Controlla i diritti del proprio piano.
- Descrivi: solo strumentale, genere, BPM, cosa succede e quando.
- **Allinea**: cerca le sue pause e i suoi punti forti con l'analisi del volume, poi scegli il punto di partenza perché cadano sui momenti chiave del video.
- **Sotto la voce**: circa −15 dB quando si parla, −7 dB nelle pause (`score_esempio.py`).

## Volume finale

−16 LUFS per i film, −14 LUFS per gli ads, picco sotto −3 dB. Controlla con `ebur128` di ffmpeg.

## Cosa chiedere alla persona

Non potendo ascoltare, chiedi: la musica copre la voce? Gli effetti sono troppi? Qualcuno arriva in ritardo? Il passaggio tra due voci si sente?
