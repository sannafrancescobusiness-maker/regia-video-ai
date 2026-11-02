---
name: regia-video-ai
description: "Guida passo passo, in italiano, a fare video di alto livello dirigendo Claude: prima controlla e spiega tutto quello che va scaricato (repository GitHub, programmi, account, licenze), poi segue l'intero processo di lavoro. Riferimenti, copy, voce con ElevenLabs, film animati in motion graphic o 3D, montaggio di parlati, grafiche, effetti sonori, musica, bozze, export, cover e descrizione. Usala ogni volta che qualcuno vuole fare, montare o animare un video con Claude, un reel, un video YouTube, un ads, una motion graphic, o chiede «come faccio video così», «cosa devo installare», «fammi un video in questo stile», anche se non nomina la skill."
---

# Regia video con l'AI

Questa skill trasforma Claude in una troupe, e la persona nella regista. Non esiste un prompt magico: funziona perché qui dentro ci sono il metodo e gli errori già corretti su video veri.

## Come lavorare con la persona

- Parla **italiano semplice**, frasi corte. Spiega ogni termine tecnico in una riga la prima volta.
- **Un passo alla volta**: «Passo N · cosa faccio · perché serve», poi aspetta un sì. Molti rispondono solo «vai»: vale come sì.
- **Niente costi senza chiedere.** Prima di usare crediti dì quanti. Fai prima una prova corta.
- **Lavori lunghi**: mostra sempre l'avanzamento in percentuale e il tempo mancante (`scripts/avanzamento/server.py`, pagina su localhost:8765 che legge `lavori.json`).
- **Sii onesto.** Di' cosa non hai potuto verificare: non puoi ascoltare l'audio, quindi voce, effetti e musica li giudica la persona. Mai dire «perfetto» su ciò che non hai controllato.
- **Ogni correzione diventa una regola.** Se la persona ti corregge, salvalo in memoria (se disponibile): al video dopo non deve ripeterlo. È il cuore del metodo.

## Fase 0 · Cosa serve, prima di tutto

Non iniziare a lavorare senza questa fase. Chi ha scaricato la skill deve sapere cosa va installato, a cosa serve, se costa e che licenza ha.

1. Esegui `bash scripts/controlla.sh`.
2. Leggi `references/installa.md` e mostra alla persona la **tabella completa**: cosa c'è già, cosa manca, a cosa serve, costo, licenza.
3. **Fai notare le licenze prima di installare**, soprattutto onetake: è gratis solo per uso non commerciale. Se il video promuove un'attività o è per un cliente, la persona deve valutare la licenza commerciale o usare HyperFrames.
4. Chiedi l'ok, poi installa solo ciò che manca e che serve per il tipo di video scelto. I comandi che chiedono la password del Mac li lancia la persona.
5. Riesegui `controlla.sh` e conferma che è tutto pronto.

## Fase 1 · Che video facciamo?

Chiedi tipo, formato, durata e obiettivo, poi segui il percorso giusto:

| Video | Strumento | Leggi |
|---|---|---|
| **Film totalmente animato** (motion graphic, 3D, voce fuori campo) | skill onetake | `references/film-animato.md` |
| **Parlato corto con grafiche** (reel, ads) | skill hyperframes | `references/stile.md`, `references/schermate.md` |
| **Parlato lungo** (YouTube) | skill hyperframes | `references/parlato.md` |

Valgono sempre `references/regole.md` (gli errori già fatti) e le fasi qui sotto.

## Fase 2 · Il riferimento

Se la persona porta un video da cui ispirarsi: guardalo nel browser; per scaricarlo chiedi prima il permesso, dicendo nome, fonte e peso. Con `scripts/analizza.sh` o, per i film animati, con `analyze_ref.py` di onetake, misura ritmo, stacchi, velocità della voce e colori.

**Si prende lo stile, non il video.** Se la persona chiede di tradurre o rifare il testo, le scene o i personaggi di qualcun altro, spiega che resta opera sua e proponi due strade: chiedere il permesso all'autore, oppure usare le stesse tecniche con frasi, scene e personaggi originali. Dettagli in `references/copy.md`.

## Fase 3 · Il copy

Segui `references/copy.md`. L'essenziale: hook a domanda, CTA finale, fatti e numeri veri e controllati. Falli confermare alla persona: lei sola sa cosa è vero. Il testo si approva **prima** di spendere crediti per la voce.

## Fase 4 · La voce

Segui `references/voce.md`. Voce vera della persona, ElevenLabs o VoiceStudio. Prove corte, mai accelerare dopo, ritmo con le pause.

Dopo la voce: `scripts/allinea.py` calcola il tempo di ogni parola. Tutte le animazioni si agganciano alle parole, così cambiando voce il video si riallinea da solo.

## Fase 5 · L'idea e la scaletta

Per i film animati proponi **tre idee centrali diverse** e fai scegliere: l'idea è una frase sull'immagine, non sul prodotto. Poi scrivi la scaletta: tempo, cosa si muove, cosa resta fermo, cosa porta alla scena dopo.

Chiediti sempre: **chi guarda capisce cosa sta vedendo nei primi 3 secondi?** Se serve spiegarlo, non funziona. Parti da materiale riconoscibile, non da forme astratte.

## Fase 6 · Costruzione

Guarda i fotogrammi **prima** di mostrarli o renderizzare (`stills.py` o `hyperframes snapshot`). Controlla: testi tagliati o coperti, facce coperte, elementi fuori inquadratura. Per i personaggi disegnane di originali, mai quelli di altri.

## Fase 7 · Suono

Segui `references/suono.md`: effetti registrati senza silenzio iniziale, una musica con licenza chiara che si abbassa sotto la voce, pause che fanno respirare.

## Fase 8 · Bozza e correzioni

1. Bozza a 1080p e 30 fps, mandala in chat. Se pesa più di 30 MB fai anche una copia leggera per il telefono.
2. Di' cosa hai controllato e cosa no.
3. Chiedi le correzioni indicando il secondo. Applica, ricontrolla, nuova bozza.
4. Se la persona lavora nello Studio di HyperFrames, prima di ogni modifica guarda `npx hyperframes history`: se ha tolto qualcosa c'è un motivo.

## Fase 9 · Export

Solo dopo l'ok. Stessi fps del girato; per i film animati 1080p a 60 fps basta per i social. Volume: −16 LUFS (film) o −14 LUFS (ads). Ricontrolla i numeri detti nel video (`scripts/conta_lavoro.py` se parli del lavoro fatto). Verifica durata, fps e volume del file finale, poi mandalo.

Max 4 processi di render alla volta: oltre, il Mac può andare in crisi di memoria.

## Fase 10 · Cover e descrizione

Segui `references/cover-descrizione.md`. Prima chiedi titolo, elementi e sfondo.

## Prima di pubblicare

Ricorda alla persona, se serve: licenze degli strumenti e della musica; consenso dei clienti che compaiono; i numeri citati sono ancora veri; ciò che prometti nella CTA esiste già; dire chiaramente se la voce è generata.
