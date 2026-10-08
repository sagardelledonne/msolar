/* M-Solar Group — animazioni e piccoli strumenti del sito */
(function () {
  "use strict";

  var fermoTutto = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- intestazione che si riduce ---------- */
  var testa = document.querySelector(".intestazione");
  function guardaScorrimento() {
    if (!testa) return;
    testa.classList.toggle("ridotta", window.scrollY > 24);
  }
  guardaScorrimento();
  window.addEventListener("scroll", guardaScorrimento, { passive: true });

  /* ---------- menu del telefono ---------- */
  var tasto = document.querySelector(".menu-tasto");
  var nav = document.querySelector(".nav");
  if (tasto && nav) {
    tasto.addEventListener("click", function () {
      var aperto = nav.classList.toggle("aperta");
      tasto.setAttribute("aria-expanded", aperto ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("aperta");
        tasto.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- comparsa al passaggio ---------- */
  var daRivelare = document.querySelectorAll(".rivela");
  if (!("IntersectionObserver" in window) || fermoTutto) {
    Array.prototype.forEach.call(daRivelare, function (el) { el.classList.add("visibile"); });
  } else {
    var osservatore = new IntersectionObserver(function (voci) {
      voci.forEach(function (v) {
        if (v.isIntersecting) {
          v.target.classList.add("visibile");
          osservatore.unobserve(v.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -60px 0px" });
    Array.prototype.forEach.call(daRivelare, function (el) { osservatore.observe(el); });
  }

  /* ---------- sfondo animato dell'eroe ---------- */
  var tela = document.querySelector(".eroe-tela");
  if (tela && tela.getContext) {
    var ctx = tela.getContext("2d");
    var larg = 0, alt = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
    var tempo = 0;
    var particelle = [];

    function misura() {
      var r = tela.getBoundingClientRect();
      larg = Math.max(1, r.width);
      alt = Math.max(1, r.height);
      tela.width = Math.round(larg * dpr);
      tela.height = Math.round(alt * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      particelle = [];
      var quante = Math.min(46, Math.round(larg / 26));
      for (var i = 0; i < quante; i++) {
        particelle.push({
          x: Math.random() * larg,
          y: Math.random() * alt,
          r: 0.6 + Math.random() * 1.7,
          v: 0.12 + Math.random() * 0.42,
          o: 0.08 + Math.random() * 0.3
        });
      }
    }

    function onda(indice, fase, ampiezza, base, colore, spessore) {
      ctx.beginPath();
      for (var x = -40; x <= larg + 40; x += 14) {
        var y = base
          + Math.sin((x / (240 + indice * 70)) + fase) * ampiezza
          + Math.sin((x / 95) + fase * 1.7) * (ampiezza * 0.22);
        if (x === -40) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      var sfuma = ctx.createLinearGradient(0, 0, larg, 0);
      sfuma.addColorStop(0, "rgba(2, 53, 110, 0)");
      sfuma.addColorStop(0.35, colore);
      sfuma.addColorStop(0.72, colore);
      sfuma.addColorStop(1, "rgba(2, 53, 110, 0)");
      ctx.strokeStyle = sfuma;
      ctx.lineWidth = spessore;
      ctx.stroke();
    }

    function disegna() {
      ctx.clearRect(0, 0, larg, alt);

      var alone = ctx.createRadialGradient(
        larg * 0.78, alt * (0.3 + Math.sin(tempo * 0.4) * 0.03), 0,
        larg * 0.78, alt * 0.3, Math.max(larg, alt) * 0.55
      );
      alone.addColorStop(0, "rgba(242, 177, 37, 0.17)");
      alone.addColorStop(0.45, "rgba(242, 177, 37, 0.05)");
      alone.addColorStop(1, "rgba(242, 177, 37, 0)");
      ctx.fillStyle = alone;
      ctx.fillRect(0, 0, larg, alt);

      var righe = [
        { amp: 30, base: alt * 0.30, col: "rgba(255, 211, 107, 0.3)", sp: 1 },
        { amp: 24, base: alt * 0.42, col: "rgba(242, 177, 37, 0.72)", sp: 1.6 },
        { amp: 36, base: alt * 0.53, col: "rgba(255, 211, 107, 0.42)", sp: 1.1 },
        { amp: 26, base: alt * 0.63, col: "rgba(120, 170, 225, 0.45)", sp: 1.2 },
        { amp: 42, base: alt * 0.73, col: "rgba(66, 126, 196, 0.5)", sp: 1.8 },
        { amp: 22, base: alt * 0.84, col: "rgba(159, 176, 194, 0.26)", sp: 1 }
      ];
      for (var i = 0; i < righe.length; i++) {
        onda(i, tempo * (0.5 + i * 0.13), righe[i].amp, righe[i].base, righe[i].col, righe[i].sp);
      }

      for (var p = 0; p < particelle.length; p++) {
        var q = particelle[p];
        q.y -= q.v;
        q.x += Math.sin((q.y / 70) + tempo) * 0.25;
        if (q.y < -10) { q.y = alt + 10; q.x = Math.random() * larg; }
        ctx.beginPath();
        ctx.arc(q.x, q.y, q.r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(255, 211, 107, " + q.o + ")";
        ctx.fill();
      }
    }

    function giro() {
      tempo += 0.006;
      disegna();
      window.requestAnimationFrame(giro);
    }

    misura();
    window.addEventListener("resize", misura);
    if (fermoTutto) { disegna(); } else { giro(); }
  }

  /* ---------- cursori con la barra colorata ---------- */
  function riempiBarra(el) {
    var min = parseFloat(el.min || 0), max = parseFloat(el.max || 100);
    var q = ((parseFloat(el.value) - min) / (max - min)) * 100;
    el.style.setProperty("--riempi", q + "%");
  }

  /* ---------- calcolo pompa di calore / caldaia ---------- */
  var calc = document.querySelector("[data-calcolatore]");
  if (calc) {
    var campi = {
      fabbisogno: calc.querySelector("#fabbisogno"),
      gas: calc.querySelector("#prezzo-gas"),
      luce: calc.querySelector("#prezzo-luce"),
      scop: calc.querySelector("#scop")
    };
    var mostra = {
      fabbisogno: calc.querySelector("#v-fabbisogno"),
      gas: calc.querySelector("#v-gas"),
      luce: calc.querySelector("#v-luce"),
      scop: calc.querySelector("#v-scop"),
      costoGas: calc.querySelector("#costo-gas"),
      costoPdc: calc.querySelector("#costo-pdc"),
      differenza: calc.querySelector("#differenza"),
      etichetta: calc.querySelector("#etichetta-differenza")
    };

    var euro = new Intl.NumberFormat("it-IT", { style: "currency", currency: "EUR", maximumFractionDigits: 0 });
    var numero = new Intl.NumberFormat("it-IT");
    var decimali = new Intl.NumberFormat("it-IT", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

    function conta() {
      var fabbisogno = parseFloat(campi.fabbisogno.value);   // kWh termici all'anno
      var prezzoGas = parseFloat(campi.gas.value) / 100;      // euro al metro cubo
      var prezzoLuce = parseFloat(campi.luce.value) / 100;    // euro al kWh
      var scop = parseFloat(campi.scop.value) / 10;

      var smc = fabbisogno / (9.45 * 0.92);                   // potere calorifico x rendimento caldaia
      var costoGas = smc * prezzoGas;
      var kwhElettrici = fabbisogno / scop;
      var costoPdc = kwhElettrici * prezzoLuce;
      var differenza = costoGas - costoPdc;

      mostra.fabbisogno.textContent = numero.format(fabbisogno) + " kWh";
      mostra.gas.textContent = decimali.format(prezzoGas) + " €/Smc";
      mostra.luce.textContent = decimali.format(prezzoLuce) + " €/kWh";
      mostra.scop.textContent = decimali.format(scop);

      mostra.costoGas.textContent = euro.format(costoGas);
      mostra.costoPdc.textContent = euro.format(costoPdc);
      mostra.differenza.textContent = euro.format(Math.abs(differenza));
      mostra.etichetta.textContent = differenza >= 0
        ? "Risparmio con la pompa di calore"
        : "In questo caso costa di più la pompa di calore";
    }

    Object.keys(campi).forEach(function (k) {
      riempiBarra(campi[k]);
      campi[k].addEventListener("input", function () { riempiBarra(campi[k]); conta(); });
    });
    conta();
  }

  /* ---------- modulo contatti: apre la posta con il messaggio gia' scritto ---------- */
  var modulo = document.querySelector("[data-modulo-mail]");
  if (modulo) {
    var etichette = {
      nome: "Nome", telefono: "Telefono", email: "Email", comune: "Comune dell'immobile",
      interesse: "Interessato a", oggi: "Impianto attuale", messaggio: "Messaggio"
    };
    modulo.addEventListener("submit", function (e) {
      e.preventDefault();
      var dati = new FormData(modulo);
      var righe = [];
      Object.keys(etichette).forEach(function (chiave) {
        var valore = (dati.get(chiave) || "").toString().trim();
        if (valore) righe.push(etichette[chiave] + ": " + valore);
      });
      righe.push("", "— richiesta inviata dal sito —");
      var oggetto = "Richiesta dal sito" + (dati.get("nome") ? " — " + dati.get("nome") : "");
      window.location.href = "mailto:" + modulo.getAttribute("data-destinatario")
        + "?subject=" + encodeURIComponent(oggetto)
        + "&body=" + encodeURIComponent(righe.join("\n"));
    });
  }
})();
