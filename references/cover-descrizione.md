# Cover e descrizione

## Scegliere il fotogramma

`scripts/cover/` contiene strumenti Swift per Mac (compila con `swiftc -O`):

1. `analizza.swift` — dà un punteggio ai fotogrammi delle clip in camera: qualità del volto, occhi, bocca, sorriso.
2. `provino.swift` — foglio numerato per confrontarli.
3. `estrai.swift` — estrae il fotogramma alla massima qualità.

Il punteggio scrematura, ma la scelta si fa guardando. Rifinisci fotogramma per fotogramma attorno ai migliori. Le riprese con il telefono più in alto e luce uniforme rendono meglio di quelle dal basso.

**Controlla le scritte**: se il video è specchiato, le scritte sui vestiti si leggono al contrario. Per la cover usa la versione non specchiata.

## Il prompt per la cover

Prima di scriverlo chiedi: **foto**, **titolo** con eventuale sottotitolo «A ⚖ B», **elementi** (di solito 3 icone), **sfondo**. Proponi 3–4 opzioni basate sul testo del video. Chiedi se togliere oggetti di disturbo, come un microfono.

La persona allega al generatore la foto e una cover precedente come riferimento di stile. Struttura del prompt in inglese:

```
Create a vertical 9:16 cover (1080x1920) in EXACTLY the same style, colors and layout as the second attached image.
PERSON: use the man/woman from the first attached photo ([vestiti e accessori visibili]). Keep face, hair, expression and clothes exactly as they are. Centered, from the chest up. [Oggetti da togliere].
BACKGROUND: [sfondo], slightly blurred and darkened, 40–50% visible, must not compete with the face.
COLOR: [palette]. Keep skin tones natural.
ICONS: three small frosted-glass rounded-square icons around the head, not touching the face: 1. … 2. … 3. …
MAIN TITLE (exact text, keep accents and punctuation): "[TITOLO]". Big bold sans-serif, all caps, white, on two lines.
SUBTITLE under the title, thin, wide letter spacing: "[A ⚖ B]"
SAFE AREAS: title must end above 78% of the height; keep the bottom 20% empty. Nothing over eyes or mouth.
No extra text, no watermarks, no logos.
```

## La descrizione

1. Prima riga: riprende il titolo della cover.
2. Il contenuto in frasi corte, con i dati.
3. CTA.
4. Note di correzione se nel video c'è un'imprecisione.
5. Fonti: controllale prima di citarle e dì quali hai scritto a memoria.
6. Pochi hashtag pertinenti.

Mostrala in chat in un blocco da copiare e salvala anche in un file.
