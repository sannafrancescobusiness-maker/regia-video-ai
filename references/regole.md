# La lista degli errori

Ogni riga è un errore già fatto su un video vero e corretto da chi dirigeva. Partire da qui evita di ripeterli.

## Copy e contenuti
- Hook a domanda, CTA alla fine, sempre.
- Un fatto non verificato non entra: un'animazione bellissima può essere storicamente sbagliata. Controlla le fonti.
- Se citi numeri o un risultato, devono essere veri al momento della pubblicazione. Niente grafici con dati inventati.
- I nomi dei clienti si controllano sempre, e serve il loro consenso per mostrarli.

## Voce
- Voci che suonano finte rovinano un video bello: fai scegliere dopo una prova corta.
- Mai accelerare la voce dopo: si sente distorta. Stringi le pause.
- Mai toccare l'audio originale di un girato: niente filtri o ricompressione. Solo micro-dissolvenze di 0,01 s sui tagli.

## Tagli
- Stretti, senza respiri, ma non robotici: si tagliano le pause da 0,35 s in su, le micro-pause dentro la frase restano.
- Mai un pezzo di parola tagliato. Ogni frase deve avere senso compiuto.
- Whisper nasconde ripetizioni e false partenze: controlla il volume e ritrascrivi le clip da sole.
- Se la persona ha cancellato una clip nello Studio, c'è un motivo.

## Immagine
- Colori originali: niente conversione HDR con ffmpeg, esce bruciata. Sui file iPhone usa `avconvert -p PresetHighestQuality`.
- Mai coprire la faccia. In camera: sottotitoli sotto il mento, bollini sul petto.
- Zone vietate nei verticali: 14% in alto, 20% in basso.
- Niente stacchi in camera sotto ~1,2 s: la faccia compare per frasi intere.
- Ogni tipo di grafica al massimo una volta per video.
- Una grafica finisce esattamente quando riprende il parlato.
- Un contatore parte sulla parola che lo nomina.
- Testi che fluttuano piano, mai che tremano. Movimenti a molla morbidi.
- Mai sottotitoli sovrapposti.
- I bollini non ripetono il sottotitolo: danno un'informazione nuova.
- Simboli astratti senza spiegazione non si capiscono: dagli un nome o parti da cose vere.
- Le scritte sui vestiti si leggono al contrario se il video è specchiato.

## Suono
- Molti effetti hanno silenzio iniziale: taglialo, o arrivano in ritardo.
- Effetto su ogni animazione importante, musica bassa sotto la voce.
- Una canzone protetta va segnalata alla persona prima di pubblicare.

## Tecnica
- Con circa 400 `<video>` nella timeline HyperFrames va in crash: monta prima i tagli in un file unico.
- Render al massimo con 4 processi.
- L'audio deve durare almeno quanto il video, o il finale viene tagliato.
- Prima di ogni render controlla che tutti i file esistano. Guarda i fotogrammi, non fidarti del codice.
- Bozza in qualità ridotta e Studio aperto prima dell'export finale.
