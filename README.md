# Sito M-Solar Group Srl

Sito statico: niente database, niente abbonamenti. Si scrive nei file `src/`, si lancia
`python build.py` e dentro `site/` compaiono le pagine finite, pronte da mettere online.

## Come si cambia qualcosa

| Cosa vuoi cambiare | File da aprire |
|---|---|
| Telefono, mail, P.IVA, REA, PEC, indirizzo, partner | `src/dati.json` |
| I testi delle pagine dei servizi | `src/servizi.json` |
| Home, Chi siamo, Servizi, Contatti, Privacy | `src/pagine/*.html` |
| Colori, caratteri, spaziature | `src/stile.css` |
| Animazioni e calcolatore | `src/script.js` |
| Logo, favicon, immagine per WhatsApp | `docs/img/` |

Dopo ogni modifica:

```bash
python build.py
```

## Le pagine

`index.html` · `chi-siamo.html` · `servizi.html` · `pompe-di-calore.html` ·
`climatizzazione.html` · `geotermico.html` · `fotovoltaico.html` ·
`assistenza.html` (manutenzione) · `contatti.html` · `privacy.html`

Più `sitemap.xml` e `robots.txt`, che servono a Google.

## Dati ancora da mettere

Stanno tutti in `src/dati.json` e si riconoscono perché sono scritti fra parentesi quadre:
P.IVA, REA, PEC, civico della sede. In più, dentro `src/pagine/chi-siamo.html`:
abilitazione DM 37/08, patentino F-Gas, assicurazione, foto di Massimiliano e i tre lavori
da raccontare.

## Il modulo dei contatti

Non c'è un server dietro: il tasto "Invia la richiesta" apre la posta del visitatore con il
messaggio già scritto e indirizzato a `email_modulo` (in `src/dati.json`). Funziona ovunque e
non costa niente. Se un giorno si vuole che la mail parta da sola senza aprire il client, si
aggiunge un servizio tipo Formspree cambiando solo il `<form>` in `src/pagine/contatti.html`.

## Per guardarlo sul computer

```bash
python -m http.server 8913 --directory docs
```

Poi si apre `http://127.0.0.1:8913` nel browser. Aprire i file con un doppio clic funziona
a metà: le animazioni hanno bisogno di un server, anche finto come questo.

## Per metterlo online

Il sito è fatto di soli file: va bene GitHub Pages, Cloudflare Pages o qualunque hosting.
Il dominio comprato da Massimiliano è `msolargroupsrl.it`.
