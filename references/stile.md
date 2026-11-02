# Lo stile (versione completa)

Nato analizzando reel di creator faceless (voce veloce, schermate bianche con grafiche, una parola alla volta) e poi «iPhonizzato» con le correzioni di un editor in 7 versioni di un reel e 2 ads. Ogni regola qui sotto ha un perché: spiegalo se la persona chiede.

## Indice
1. Struttura del video
2. Regole del montaggio (le più importanti)
3. Look iPhone: vetro, colori, font
4. Movimento
5. Sottotitoli
6. Suoni e musica
7. Personaggi ed emoji
8. Scene pixel (opzionali)
9. Errori già fatti da non ripetere

## 1 · Struttura del video

- **Ibrido**: la persona in camera + **schermate bianche** che illustrano la frase in corso (circa il 35–45% del tempo). Negli ads la faccia nei primi 2 secondi aggancia: il gancio resta in camera.
- **Overlay in camera**: quando la frase si presta (notifica, badge, modulo), la grafica va *sopra* la camera invece che su bianco: varia il ritmo e mostra la persona.
- **Nero con una parola** per frasi forti («smetti.», «di nascosto»), opzionale con un boom cinematografico e la musica che si interrompe.
- Struttura testi (se la persona scrive anche i copioni): gancio con numero choc → «3 mosse/trucchi» → mossa 1-2-3 con nome + storia + principio psicologico → meta-finale («se sei arrivato fin qui…») → CTA «commenta [parola]».

## 2 · Regole del montaggio

- **La faccia compare solo per dire frasi intere.** Niente stacchi in camera sotto ~1,2 s o che mostrano la persona zitta: allunga la schermata vicina.
- **Una schermata finisce esattamente quando riprende il parlato** nella clip dopo (inizio della prima parola −0,03 s) **o sul taglio di inquadratura**, se arriva entro ~0,25 s: altrimenti si vede un pezzetto di clip muta o della vecchia inquadratura e poi subito il taglio («taglio bruttissimo»). Usa `allinea_fine()` della libreria.
- **Mai grafiche sopra b-roll importanti** (prodotti, telecamere, dimostrazioni) né sopra flash/transizioni già montate dal cliente.
- **Ogni tipo di grafica al massimo una volta per video** (pillole numerate, X rosse, lente, grafico…): inventa visualizzazioni diverse.
- **Mai sottotitoli sovrapposti**, né tra loro né con le grafiche; mai sottotitoli «da camera» su sfondo bianco (attenzione ai «buchi» dentro una schermata).
- **Zone vietate** ai testi: 14% in alto (y < 270 su 1920) e 20% in basso (y > 1536): ci sono i pulsanti dei social. Mai coprire la faccia.
- **Tagli stretti**: niente respiri o false partenze tra le clip (se si monta da girato grezzo).
- Video del cliente con **sottotitoli già impressi**: niente sottotitoli nostri in camera; overlay sopra o sotto i loro (misura dove stanno dalla griglia).

## 3 · Look iPhone

- **Liquid Glass**: pillole e cerchi in vetro colorato con bordo bianco luminoso, riflesso interno, ombra morbida colorata, `backdrop-filter: blur saturate`; riquadri/widget in vetro chiaro. Dietro: 2–3 **macchie di colore sfumate** che si muovono piano (senza, il vetro su bianco non si vede).
- **Colore principale** scelto dalla persona (preset in libreria: blu `#1f5cff`, arancione `#ff9500`, verde, rosso, viola). Verde iOS `#34c759` per «ok/attivo», rosso iOS `#ff3b30` per errori/X.
- **Font**: titoli e citazioni in **corsivo serif** (Playfair Display italic 700) — mai titoli in bastone maiuscolo; numeri grandi Inter 900; UI e sottotitoli **SF Pro** (fallback Inter).
- **Frecce stile Apple/SF Symbols**: una curva pulita + punta a chevron simmetrica (`arrow()`), mai scarabocchi.
- Elementi UI iOS molto efficaci: interruttore che diventa verde, notifica che scende dall'alto, lista Impostazioni, widget con «● LIVE», modulo con campi che si compilano e pulsante premuto, scontrino €0 con timbro.

## 4 · Movimento

- **Molle iOS**: comparse da scala 0,72 + sfocatura 10 px → nitido, `back.out(1.2)`, 0,55 s (`pop`). Niente rimbalzi da cartone.
- **Testi che entrano**: sfocatura + 10 px dal basso, 0,32 s (`blurIn`).
- **Uscite**: sfocano e rimpiccioliscono un poco, 0,2 s (`hide`).
- **Fluttuare**: tutta la schermata bianca fluttua piano (±8 px, periodo 3–6 s) con una lieve inclinazione 3D come la parallasse dello sfondo di iPhone. **Mai shake/tremolio** (è stato bocciato).
- Gli elementi comparsi **non restano fermi**: zoom lento (es. 1 → 1,16), contatori che salgono, cerchi radar.
- Le animazioni partono **sulla parola** che le nomina (contatore da 0 sulla parola «mezzo» di «mezzo milione», interruttore su «acceso»).
- Frecce e cerchi **si disegnano** (tratto progressivo, punta per ultima), non compaiono già fatti.

## 5 · Sottotitoli

- **In camera**: bianchi, SF Pro semibold 66 px, ombra morbida (niente riquadro, niente colori), gruppi di 2–4 parole sotto il mento (~y 1300); la parola detta passa da velata (50%) a piena; il gruppo entra salendo e sfocato come una notifica.
- **Su bianco/nero**: **una parola alla volta**, SF Pro medium ~56 px, centrata (~y 1330, sotto la grafica), che **fluttua** piano (±7 px, rotazione ±0,6°) finché arriva la parola dopo.
- Dove la grafica contiene già il testo (fumetto, dialogo, numeri grandi) i sottotitoli si spengono.

## 6 · Suoni e musica

- **Un suono per ogni animazione**: whoosh corto all'entrata di ogni schermata, pop sulle comparse, click su X e interruttori, «tratto di penna» su frecce/cerchi che si disegnano, bollicine sulla nuvoletta, tick sulle cascate, typing sui contatori/campi che si scrivono, notification su notifiche e CTA, ping sui dati rivelati, sparkle sui momenti «wow», impact sui numeri grandi.
- Volumi effetti 0,15–0,4 (sotto la voce). **Musica di sottofondo** bassa: ~−33 LUFS nel mix (voce ~−14). Misura il brano con ebur128 e calcola il volume.
- Mix finale ≈ **−14 LUFS**, picco sotto −3 dB (voce del cliente spesso a ~0,63 se arriva già forte). Se la persona dice «spacca i timpani», abbassa tutto in proporzione.
- Frase forte → la musica si interrompe (dissolvenza 0,08 s), boom cinematografico, la musica riparte dal punto in cui si era fermata quando si torna in camera.

## 7 · Personaggi ed emoji

- Personaggi e oggetti non-pixel = **emoji Apple** (👴 che «parla» col fumetto, 🧍, 🤔 con nuvoletta, 🧑‍🎓 in griglia, 🔨 💡 ⚙️, 🏠, 📹, 🚧…). Font locale «Apple Color Emoji».
- Fumetti e nuvolette in vetro chiaro; il testo dentro esce parola per parola sul parlato.

## 8 · Scene pixel (opzionali)

Stile **Pokémon Rosso Fuoco** (GBA) disegnato in codice su canvas (mondo 90×160 ×12 + interfaccia 180×320 ×6): vista dall'alto a riquadri, riquadro dialoghi bianco con freccia rossa, cartello del luogo, menu zaino, lotta con barre PS/ESP. Personaggi **originali** (mai personaggi o loghi veri). Suoni 8-bit da `sfx8.sh`. Negli ads di solito no: chiedi.

## 9 · Errori già fatti (non ripeterli)

- Tone-mapping FFmpeg su HDR iPhone → colori bruciati. Per HDR usa `avconvert -p PresetHighestQuality` (conversione Apple).
- Frecce disegnate con `getTotalLength()`/dash CSS → comparivano già complete: usa `pathLength="1"` + attributo `stroke-dashoffset` (già nella libreria).
- `immediateRender` dei `fromTo` → puntini/tratti visibili prima dell'animazione: usa `immediateRender:false` e opacità iniziale 0.
- Buchi «camera» dentro una schermata → si vedeva il bianco con i sottotitoli sbagliati.
- Export a 30 fps di un girato a 24 fps → movimento a scatti: usa `--fps` uguale al girato.
- Suono citato ma file mancante in `assets/` → render bloccato: controlla i file prima del render.
- Rimozione dei vecchi effetti sonori che ha tolto anche quello della CTA: dopo ogni ricostruzione ricontrolla che ogni animazione abbia il suo suono.
