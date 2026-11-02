# La voce

## Quale voce

1. **La voce vera della persona**: la più riconoscibile.
2. **ElevenLabs**: la qualità migliore tra quelle generate. Costa crediti.
3. **VoiceStudio**: gratis e sul Mac, ma spesso si sente che è artificiale. Bene come voce guida per dare i tempi.

Chiedi che carattere vuole, ad esempio narratore profondo da documentario. Una voce sbagliata rovina tutto il resto.

## ElevenLabs dal Chrome della persona (Claude in Chrome)

1. Apri `elevenlabs.io/app/speech-synthesis/text-to-speech`. Dentro c'è il suo account: non toccare impostazioni dell'account e non comprare nulla.
2. Se nella casella c'è già un testo, salvane una copia prima di sostituirlo.
3. Filtra le voci per lingua, genere, età e categoria.
4. **Prova corta prima**, una o due frasi (≈100 crediti), con 2–3 voci. Manda i file e lascia decidere alla persona.
5. Solo dopo l'ok genera tutto il testo. Dì i crediti prima.
6. Scarica in `voce/eleven/` e controlla le parole con whisper.

### Scrivere il testo per la voce

Il testo per la voce può differire da quello a schermo. Scrivi come si pronuncia: `Clod` per Claude, `l'A.I.` per AI, `Bi Emme Vu` per le sigle, accenti sulle parole difficili (`medicìna`). I numeri in lettere.

## Velocità

**Mai accelerare la voce dopo averla generata**: anche con strumenti buoni si sente distorta. Per dare ritmo:

1. Stringi le pause con `scripts/monta_voce.py`: guadagni circa il 10% senza toccare la voce.
2. Se serve, usa una generazione con velocità nativa. Nell'app il cursore c'era su Multilingual v2 e non su v4, ma la voce può cambiare carattere.

## Una seconda voce

Una domanda detta da un'altra voce sembra fatta da un'altra persona: tiene viva l'attenzione. Generala a parte con un tag come `[curious]` e incollala con `monta_voce.py`, che la porta allo stesso volume.

## Correggere una frase

Non rigenerare tutto: rifai solo la frase e sostituiscila con `monta_voce.py`. Costa pochi crediti.

## I tempi

```bash
python3 scripts/monta_voce.py voce/montaggio.json
python3 scripts/allinea.py voce/voce.wav copy.txt comp/
```

`allinea.py` scrive `parole.js` e `frasi.js`. Se whisper sbaglia una parola, la posizione viene stimata dalle vicine; se meno dell'85% delle parole è agganciato, controlla il testo.

## Dillo

Se la voce è generata e la persona parla in prima persona, proponi di dirlo nel video: è onesto e può diventare un bel momento.
