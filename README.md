# Regia video con l'AI

Una skill per [Claude Code](https://claude.com/claude-code) che ti guida, passo dopo passo e in italiano, a fare video di alto livello dirigendo Claude.

Non è un prompt magico. Dentro ci sono il metodo di lavoro e gli errori già corretti su video veri, scritti come regole.

## Cosa fa

**Prima di iniziare ti dice tutto quello che va scaricato.** Controlla cosa hai già sul Mac e ti mostra cosa manca, a cosa serve, quanto costa e che licenza ha. Installa solo dopo il tuo ok.

Poi segue il lavoro dall'inizio alla fine:

1. Che video facciamo: film animato, parlato corto con grafiche o parlato lungo
2. Analisi del video da cui ti ispiri (si prende lo stile, non il video)
3. Copy, con fatti e numeri veri
4. Voce: la tua, ElevenLabs o VoiceStudio
5. Idea e scaletta
6. Costruzione delle scene
7. Effetti sonori e musica
8. Bozza e correzioni
9. Export finale
10. Cover e descrizione

Dentro c'è anche un modello di film 3D in 16:9 da adattare, la «stanza a cubetti», in `assets/stanza/`.

## Come si installa

Ti serve un Mac con Claude Code. Apri il Terminale e lancia:

```bash
git clone https://github.com/sannafrancescobusiness-maker/regia-video-ai.git ~/.claude/skills/regia-video-ai
```

Riavvia Claude Code e scrivi:

> Voglio fare un video. Parti dalla Fase 0 della skill regia-video-ai.

## Cosa va scaricato

La Fase 0 controlla tutto da sola. Questo è l'elenco completo.

| Cosa | A cosa serve | Licenza | Costo |
|---|---|---|---|
| [HyperFrames](https://github.com/heygen-com/hyperframes) | Montaggio di parlati, grafiche, render | Apache-2.0 | Gratis |
| [onetake](https://github.com/feitangyuan/onetake) | Film animati: movimenti, motion blur, controlli di ritmo | **PolyForm Noncommercial 1.0.0** | Gratis solo per uso non commerciale |
| [three.js](https://github.com/mrdoob/three.js) e [esbuild](https://github.com/evanw/esbuild) | Il 3D dei film animati | MIT | Gratis |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Trascrizione parola per parola sul Mac | MIT | Gratis |
| [VoiceStudio](https://github.com/debpalash/VoiceStudio) (facoltativo) | Voci generate sul Mac | AGPL-3.0 | Gratis |
| ffmpeg, Node, Python, Homebrew | Gli strumenti di base | Varie | Gratis |
| Claude Code e Claude in Chrome | Dirigono tutto | Termini Anthropic | Abbonamento o API |
| ElevenLabs (facoltativo) | Voci premium e musica | Termini ElevenLabs | A crediti |

Il dettaglio, con tutti i comandi, è in [`references/installa.md`](references/installa.md).

## Prima di usarla per lavoro

- **onetake non è per uso commerciale.** Se il video promuove un'attività o è per un cliente, valuta [onetake Pro](https://onetakemotion.com) oppure usa HyperFrames. Il codice di onetake non è dentro questa skill: lo scarichi tu dalla fonte.
- **ElevenLabs:** controlla che il tuo piano copra l'uso commerciale di voci e musica.
- **Clienti:** chiedi il loro consenso prima di mostrarli.

Le licenze cambiano: controlla sempre il link. Questa pagina non è consulenza legale.

## A che punto è

Gli script sono stati provati su progetti veri, su un solo Mac. Non è ancora stata provata l'installazione su un Mac pulito, né un video intero fatto da zero partendo dalla skill. È pensata per Mac. Claude non può ascoltare l'audio: voce, effetti e musica li giudichi tu.
