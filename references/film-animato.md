# Film animato

Leggi prima la skill **onetake** e segui il suo protocollo: riferimento misurato, tre idee, scaletta, composizione, render, suono, verifica. Qui c'è ciò che si è aggiunto lavorando. Ricorda la licenza non commerciale di onetake.

## Il modello pronto: la stanza a cubetti

`assets/stanza/` contiene un film 16:9 completo: mondo 3D a cubetti in three.js, personaggi pixel estrusi, testi una parola alla volta, muro di video, commenti, scene agganciate alle parole. Vedi `assets/stanza/LEGGIMI.md`. È un punto di partenza da **cambiare**: l'ultimo film non deve diventare il look del prossimo, a meno che la persona non lo chieda.

## Far capire cosa si vede

Le forme astratte non si capiscono da sole. Un cubo rosso nel vuoto ha lasciato chi guardava senza capire. Ha funzionato così:

- **partire da materiale vero**, i video della persona su un muro;
- **illustrare la frase alla lettera**: «che prompt usi?» diventa una valanga di commenti; «si copia in dieci secondi» diventa una scheda che si moltiplica con un timer;
- **dare un'etichetta ai simboli**: i cubi hanno preso senso quando ognuno portava il nome di un errore.

## Tenere incollati

- Scatto di camera sulle parole chiave: uno stringersi breve di 2° che decade in circa 0,2 s, con il suo suono.
- Passaggi di camera veloci: lo schermo che si attraversa, il volo tra le scene.
- Una rottura netta a metà: stacco sul nero, pausa della musica, testo piccolo.
- Mostrare cose vere: lavori veri, numeri veri, cubi in numero esatto.
- Nessuna grafica finta: se non hai dati, confronta il prima e il dopo reali.

## Inquadrature

- Testo e soggetto non si sovrappongono: decidi prima dove va il testo e sposta la camera di conseguenza.
- Un personaggio non deve coprire ciò di cui si parla: spostalo tra una scena e l'altra.
- Prima di ogni render guarda 12 fotogrammi sparsi.

## Tecnica

- Render 3D: `render.py --gpu --workers 4`, circa 5 minuti per 72 s a 1080p30.
- Immagini per `file://`: incorporale in base64 in un file `.js` per non avere problemi di sicurezza su WebGL.
- Con `-shortest` il render taglia il video se l'audio è più corto: l'audio deve durare almeno quanto il video.
- `verify_promo.py` di onetake può bloccarsi su scene 3D pesanti: se accade, controlla a mano con fogli di fotogrammi e dillo alla persona.
