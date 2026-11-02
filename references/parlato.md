# Parlato lungo (YouTube)

Metodo che ha portato un girato di 39 minuti a 20 minuti, circa 400 tagli, senza frasi spezzate.

## Tagli

1. Conversione: se il girato è HDR iPhone, usa `avconvert`; altrimenti i colori si bruciano.
2. Volume ogni 10 ms. Divide in pezzi alle pause da 0,25 s in su.
3. Trascrivi **ogni pezzo da solo** con whisper-server (`-ml 1 -sow -dtw large.v3`): sull'intero file whisper nasconde ripetizioni e sbaglia i tempi.
4. Scegli i tagli **sul testo**, frase per frase, tenendo l'ultima presa delle ripetizioni.
5. Taglia nel punto più silenzioso tra le parole. Soglie adattate al rumore di ogni punto: attacco sopra max(rumore+8, picco−30) dB, fine sopra max(rumore+10, picco−24) dB.
6. **Doppio controllo**: ritrascrivi tutte le giunte (2,5 s prima e dopo) e tutte le clip da sole. Cerca ripetizioni e parole mozzate.

Scrivi un resoconto leggibile di ogni taglio con il motivo, così la persona può controllare senza riguardare tutto.

## Capitoli e sottotitoli

- Orizzontale 1920×1080. Dividi per argomento.
- Titolo capitolo a schermo intero: ~2,6 s, nero, titolo bianco, un colore di accento e un whoosh.
- Sottotitoli da cinema: piccoli (~37 px), giallo chiaro `#f4df8b`, ombra sottile, una riga, ~58 px dal fondo, senza intercalari. Correggili a mano sul testo.

## Grafiche e schermo

- Aggancia ogni grafica a una frase detta.
- Per mostrare siti e pagine usa il browser. Nelle catture niente nomi di contatti, commenti di altri, ordini o dati privati.

## Tecnica

- Monta i tagli in un file unico allineato ai fotogrammi (ogni pezzo N fotogrammi esatti, audio N×campioni, micro-dissolvenza di 10 ms) e metti in timeline solo un pezzo per capitolo.
- Scrivi un `RIPRENDI.md` con stato, file e comandi, così il lavoro si può riprendere in qualsiasi momento.
