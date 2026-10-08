# -*- coding: utf-8 -*-
"""Costruisce il sito di M-Solar Group dentro la cartella site/.

Come si usa:  python build.py
Cosa si tocca per cambiare i contenuti:
  src/dati.json      -> dati dell'azienda (telefono, mail, P.IVA, partner...)
  src/servizi.json   -> le pagine dei servizi
  src/pagine/*.html  -> home, chi siamo, servizi, contatti, privacy
  src/stile.css      -> grafica
  src/script.js      -> animazioni e calcolatore
"""
import hashlib
import io
import json
import os
import shutil

QUI = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, "/")
SRC = QUI + "/src"
SITE = QUI + "/docs"


def leggi(percorso):
    with io.open(percorso, encoding="utf-8") as f:
        return f.read()


def scrivi(percorso, testo):
    cartella = os.path.dirname(percorso)
    if cartella and not os.path.isdir(cartella):
        os.makedirs(cartella)
    with io.open(percorso, "w", encoding="utf-8", newline="\n") as f:
        f.write(testo)


def impronta(percorso):
    """Otto caratteri che cambiano quando cambia il file: servono a far
    scaricare al browser la versione nuova invece di quella in memoria."""
    with io.open(percorso, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


DATI = json.loads(leggi(SRC + "/dati.json"))
SERVIZI = json.loads(leggi(SRC + "/servizi.json"))["servizi"]

ICONE = {
    "pompe-di-calore": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="9" width="38" height="30" rx="4"/><circle cx="24" cy="24" r="9"/><path d="M24 15c4 3 4 6 0 9s-4 6 0 9"/><path d="M15 24c3-4 6-4 9 0s6 4 9 0"/></svg>',
    "climatizzazione": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="10" width="38" height="14" rx="5"/><path d="M12 17h24"/><path d="M14 30c0 4 4 4 4 8"/><path d="M24 30c0 5 4 5 4 9"/><path d="M34 30c0 4 4 4 4 8"/></svg>',
    "geotermico": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18h40"/><path d="M14 18v16a6 6 0 0 0 12 0V18"/><path d="M34 18v22"/><path d="M8 26h2M8 33h2M38 26h2M38 33h2"/><path d="M24 4v8M18 8l6-4 6 4"/></svg>',
    "fotovoltaico": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="24" cy="14" r="6"/><path d="M24 2v3M24 23v3M12 14H9M39 14h-3M15.5 5.5 13.4 3.4M34.6 24.6l-2.1-2.1M32.5 5.5l2.1-2.1M13.4 24.6l2.1-2.1"/><path d="M10 44h28l-4-14H14z"/><path d="M12 37h24M22 30l-2 14M28 30l2 14"/></svg>',
    "assistenza": '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M30 6a10 10 0 0 0-9.3 13.7L6.6 33.8a4 4 0 1 0 5.6 5.6l14.1-14.1A10 10 0 1 0 30 6z"/><path d="M10 36.5h.02"/></svg>',
}


def scheda_servizio(s, chiara=False):
    return (
        '<a class="scheda rivela" href="{file}.html">'
        '<span class="icona" aria-hidden="true">{icona}</span>'
        '<h3>{titolo}</h3>'
        '<p class="grigio">{occhiello}</p>'
        '<span class="scheda-link">Vedi come lavoriamo <span class="freccia">&rarr;</span></span>'
        '</a>'
    ).format(file=s["file"], icona=ICONE.get(s["file"], ""), titolo=s["titolo"], occhiello=s["occhiello"])


SCHEDE_SERVIZI = "".join(scheda_servizio(s) for s in SERVIZI)

PARTNER_PRODOTTI = "".join(
    '<div><b>{nome}</b><span>{cosa}</span></div>'.format(**p) for p in DATI["partner_prodotti"]
)
PARTNER_FINANZA = "".join(
    '<div><b>{nome}</b><span>{cosa}</span></div>'.format(**p) for p in DATI["partner_finanza"]
)
CITTA_SERVITE = " &middot; ".join(DATI["citta_servite"])

NAV = [
    ("index.html", "Home"),
    ("chi-siamo.html", "Chi siamo"),
    ("servizi.html", "Servizi"),
    ("assistenza.html", "Manutenzione"),
    ("incentivi.html", "Incentivi"),
    ("contatti.html", "Contatti"),
]


def menu(attiva):
    voci = []
    for file, nome in NAV:
        classe = ' class="attivo"' if file == attiva else ""
        voci.append('<a href="{0}"{1}>{2}</a>'.format(file, classe, nome))
    return "".join(voci)


RICHIAMO = """
<section class="sezione">
  <div class="contenitore">
    <div class="richiamo rivela">
      <p class="occhiello">Parliamone</p>
      <h2>Raccontateci la vostra casa.<br>Al resto pensiamo noi.</h2>
      <p class="guida grigio" style="margin-top:20px">Sopralluogo, calcolo del fabbisogno e un preventivo che si capisce, voce per voce. Senza impegno e senza fretta.</p>
      <div class="bottoni">
        <a class="bottone bottone-oro" href="contatti.html">Richiedi un sopralluogo <span class="freccia">&rarr;</span></a>
        <a class="bottone bottone-chiaro" href="tel:{tel_link}">{tel}</a>
      </div>
    </div>
  </div>
</section>
"""

GUSCIO = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo_seo}</title>
<meta name="description" content="{descrizione}">
<link rel="canonical" href="{sito}/{file}">
<meta property="og:type" content="website">
<meta property="og:title" content="{titolo_seo}">
<meta property="og:description" content="{descrizione}">
<meta property="og:image" content="{sito}/img/social.jpg">
<meta property="og:locale" content="it_IT">
<meta name="theme-color" content="#07121f">{anteprima}
<link rel="icon" href="img/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="img/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&display=swap">
<link rel="stylesheet" href="stile.css?v={ver_css}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HVACBusiness",
  "name": "{azienda}",
  "image": "{sito}/img/social.jpg",
  "url": "{sito}",
  "telephone": "{tel}",
  "email": "{email}",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{via}",
    "postalCode": "{cap}",
    "addressLocality": "{citta}",
    "addressRegion": "{prov}",
    "addressCountry": "IT"
  }},
  "areaServed": "Nord Italia",
  "founder": "{titolare}",
  "knowsAbout": ["Pompe di calore", "Geotermico", "Climatizzazione", "Fotovoltaico", "Conto Termico"]
}}
</script>
</head>
<body>
<a class="salta-al-contenuto" href="#contenuto">Vai al contenuto</a>

<header class="intestazione">
  <div class="contenitore barra">
    <a class="marchio" href="index.html" aria-label="{azienda}, torna alla home">
      <img src="img/logo-chiaro.png" alt="{azienda}" width="730" height="220">
    </a>
    <button class="menu-tasto" type="button" aria-label="Apri il menu" aria-expanded="false"><span></span></button>
    <nav class="nav">{menu}</nav>
  </div>
</header>

<main id="contenuto">
{corpo}
</main>

<footer class="piede">
  <div class="contenitore">
    <div class="piede-griglia">
      <div>
        <img src="img/logo-chiaro.png" alt="{azienda}" width="730" height="220">
        <p class="grigio">Impianti termici e fotovoltaici in tutto il {zona}. Progettati, installati e seguiti nel tempo.</p>
      </div>
      <div>
        <h4>Servizi</h4>
        <ul>
          <li><a href="pompe-di-calore.html">Pompe di calore</a></li>
          <li><a href="climatizzazione.html">Climatizzazione</a></li>
          <li><a href="geotermico.html">Geotermico</a></li>
          <li><a href="fotovoltaico.html">Fotovoltaico e accumulo</a></li>
          <li><a href="assistenza.html">Manutenzione e assistenza</a></li>
        </ul>
      </div>
      <div>
        <h4>Azienda</h4>
        <ul>
          <li><a href="chi-siamo.html">Chi siamo</a></li>
          <li><a href="servizi.html">Tutti i servizi</a></li>
          <li><a href="incentivi.html">Normativa e incentivi</a></li>
          <li><a href="contatti.html">Contatti</a></li>
          <li><a href="privacy.html">Privacy</a></li>
        </ul>
      </div>
      <div>
        <h4>Contatti</h4>
        <ul>
          <li><a href="tel:{tel_link}">{tel}</a></li>
          <li><a href="mailto:{email}">{email}</a></li>
          <li class="grigio">{via}<br>{cap} {citta} ({prov})</li>
          <li class="grigio">{orari}</li>
        </ul>
      </div>
    </div>
    <div class="piede-basso">
      <span>&copy; 2026 {azienda} &middot; P.IVA {piva} &middot; REA {rea}</span>
      <span>PEC {pec}</span>
    </div>
  </div>
</footer>

<script src="script.js?v={ver_js}"></script>
</body>
</html>
"""


def sostituisci(testo):
    coppie = {
        "{{AZIENDA}}": DATI["azienda"],
        "{{NOME_BREVE}}": DATI["nome_breve"],
        "{{TEL}}": DATI["telefono"],
        "{{TEL_LINK}}": DATI["telefono_link"],
        "{{WHATSAPP}}": DATI["whatsapp"],
        "{{EMAIL}}": DATI["email"],
        "{{EMAIL_MODULO}}": DATI["email_modulo"],
        "{{PEC}}": DATI["pec"],
        "{{VIA}}": DATI["via"],
        "{{CAP}}": DATI["cap"],
        "{{CITTA}}": DATI["citta"],
        "{{PROV}}": DATI["provincia"],
        "{{ZONA}}": DATI["zona"],
        "{{CITTA_SERVITE}}": CITTA_SERVITE,
        "{{PIVA}}": DATI["piva"],
        "{{REA}}": DATI["rea"],
        "{{ORARI}}": DATI["orari"],
        "{{TITOLARE}}": DATI["titolare"],
        "{{RUOLO_TITOLARE}}": DATI["ruolo_titolare"],
        "{{SERVIZI_SCHEDE}}": SCHEDE_SERVIZI,
        "{{PARTNER_PRODOTTI}}": PARTNER_PRODOTTI,
        "{{PARTNER_FINANZA}}": PARTNER_FINANZA,
    }
    for chiave, valore in coppie.items():
        testo = testo.replace(chiave, valore)
    return testo


ANTEPRIMA = DATI.get("anteprima", False)
META_ANTEPRIMA = (chr(10) + '<meta name="robots" content="noindex, nofollow">') if ANTEPRIMA else ""


def pagina(file, titolo_seo, descrizione, corpo, con_richiamo=True):
    if con_richiamo:
        corpo += RICHIAMO.format(tel=DATI["telefono"], tel_link=DATI["telefono_link"])
    html = GUSCIO.format(
        titolo_seo=titolo_seo,
        anteprima=META_ANTEPRIMA,
        descrizione=descrizione,
        file=file,
        sito=DATI["sito"],
        azienda=DATI["azienda"],
        tel=DATI["telefono"],
        tel_link=DATI["telefono_link"],
        email=DATI["email"],
        pec=DATI["pec"],
        via=DATI["via"],
        cap=DATI["cap"],
        citta=DATI["citta"],
        prov=DATI["provincia"],
        zona=DATI["zona"],
        piva=DATI["piva"],
        rea=DATI["rea"],
        orari=DATI["orari"],
        titolare=DATI["titolare"],
        ver_css=impronta(SRC + "/stile.css"),
        ver_js=impronta(SRC + "/script.js"),
        menu=menu(file),
        corpo=corpo,
    )
    scrivi(SITE + "/" + file, sostituisci(html))


def pagina_servizio(s):
    comprende = "".join(
        '<div class="scheda rivela"><h3>{titolo}</h3><p class="grigio">{testo}</p></div>'.format(**c)
        for c in s["comprende"]
    )
    numeri = "".join(
        '<div class="numero"><b>{valore}</b><span>{etichetta}</span></div>'.format(**d)
        for d in s["dettagli"]
    )
    faq = "".join(
        "<details><summary>{d}</summary><p>{r}</p></details>".format(**f) for f in s["faq"]
    )
    correlati = "".join(
        scheda_servizio(next(x for x in SERVIZI if x["file"] == c)) for c in s["correlati"]
    )

    corpo = """
<section class="eroe-interno">
  <div class="contenitore">
    <p class="briciole"><a href="index.html">Home</a> &rsaquo; <a href="servizi.html">Servizi</a> &rsaquo; {titolo}</p>
    <p class="occhiello">{occhiello}</p>
    <h1>{sottotitolo}</h1>
  </div>
</section>

<section class="sezione">
  <div class="contenitore">
    <div class="griglia griglia-2" style="gap:clamp(30px,5vw,70px);align-items:start">
      <div class="rivela">
        <h2>{titolo}</h2>
      </div>
      <div class="rivela">
        <p class="guida">{intro}</p>
      </div>
    </div>
  </div>
</section>

<section class="sezione-stretta">
  <div class="contenitore">
    <div class="numeri rivela">{numeri}</div>
  </div>
</section>

<section class="sezione chiara">
  <div class="contenitore">
    <div class="riga-titolo">
      <p class="occhiello">Cosa comprende</p>
      <h2>Il lavoro, voce per voce</h2>
    </div>
    <div class="griglia griglia-3">{comprende}</div>
  </div>
</section>

<section class="sezione">
  <div class="contenitore">
    <div class="riga-titolo">
      <p class="occhiello">Domande frequenti</p>
      <h2>Quello che ci chiedono sempre</h2>
    </div>
    <div class="faq rivela">{faq}</div>
  </div>
</section>

<section class="sezione-stretta">
  <div class="contenitore">
    <div class="riga-titolo"><p class="occhiello">Vedi anche</p></div>
    <div class="griglia griglia-2">{correlati}</div>
  </div>
</section>
""".format(
        titolo=s["titolo"],
        occhiello=s["occhiello"],
        sottotitolo=s["sottotitolo"],
        intro=s["intro"],
        numeri=numeri,
        comprende=comprende,
        faq=faq,
        correlati=correlati,
    )

    pagina(
        s["file"] + ".html",
        "{0} a {1} e in {2} | {3}".format(s["titolo"], DATI["citta"], DATI["zona"], DATI["nome_breve"]),
        s["sottotitolo"],
        corpo,
    )


PAGINE_SEMPLICI = [
    ("index.html", "{azienda} | Impianti termici e fotovoltaici in Nord Italia",
     "Pompe di calore, geotermico, climatizzazione e fotovoltaico. Progettiamo prima di installare: sopralluogo, calcolo del fabbisogno e preventivo chiaro. Saronno e tutto il Nord Italia."),
    ("chi-siamo.html", "Chi siamo | {azienda}",
     "M-Solar Group nasce dall'esperienza di un termotecnico: specializzazione sul termico, precisione in cantiere e un cliente seguito davvero, prima e dopo l'impianto."),
    ("servizi.html", "Servizi | {azienda}",
     "Tutti i lavori di M-Solar Group: pompe di calore, climatizzazione, geotermico, fotovoltaico e accumulo, manutenzione, progettazione e pratiche per gli incentivi."),
    ("incentivi.html", "Normativa e incentivi | {azienda}",
     "Detrazioni fiscali, Conto Termico, pratica ENEA e incentivi per il fotovoltaico: come funzionano e quale conviene. Piu gli obblighi di legge del vostro impianto."),
    ("contatti.html", "Contatti | {azienda}",
     "Telefono, WhatsApp, email e sede di M-Solar Group. Richiedi un sopralluogo per il tuo impianto termico o fotovoltaico."),
    ("privacy.html", "Privacy | {azienda}",
     "Informativa sul trattamento dei dati personali del sito di M-Solar Group Srl."),
]


def costruisci():
    if os.path.isdir(SITE):
        for nome in os.listdir(SITE):
            if nome != "img":
                percorso = SITE + "/" + nome
                if os.path.isdir(percorso):
                    shutil.rmtree(percorso)
                else:
                    os.remove(percorso)

    shutil.copyfile(SRC + "/stile.css", SITE + "/stile.css")
    shutil.copyfile(SRC + "/script.js", SITE + "/script.js")

    for file, titolo, descrizione in PAGINE_SEMPLICI:
        corpo = leggi(SRC + "/pagine/" + file)
        pagina(file, titolo.format(azienda=DATI["azienda"]), descrizione, corpo,
               con_richiamo=(file not in ("contatti.html", "privacy.html")))

    for s in SERVIZI:
        pagina_servizio(s)

    tutte = [p[0] for p in PAGINE_SEMPLICI] + [s["file"] + ".html" for s in SERVIZI]
    mappa = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f in tutte:
        mappa.append("  <url><loc>{0}/{1}</loc></url>".format(DATI["sito"], f))
    mappa.append("</urlset>")
    scrivi(SITE + "/sitemap.xml", "\n".join(mappa) + "\n")
    if ANTEPRIMA:
        scrivi(SITE + "/robots.txt", "User-agent: *\nDisallow: /\n")
    else:
        scrivi(SITE + "/robots.txt",
               "User-agent: *\nAllow: /\nSitemap: {0}/sitemap.xml\n".format(DATI["sito"]))

    print("fatte {0} pagine in {1}".format(len(tutte), SITE))
    for f in sorted(tutte):
        print("  -", f)


if __name__ == "__main__":
    costruisci()
