# mellemmoederne-web

Offentlig landingsside for Mellem Møderne (Lasse B. Schnipper). Ren statisk HTML/CSS/JS, ingen build-step, intet framework. Hostes via Cloudflare Pages, koblet direkte til dette GitHub-repo: hvert push til `main` deployer automatisk.

## Struktur

```
index.html                                Forside (om mig, ydelser, hvorfor, presse, faq, kontakt)
vaerktoejer/index.html                    Statisk oversigt over værktøjsserien
vaerktoejer/<slug>/index.html             Én statisk side pr. værktøj
privatliv/index.html                      Privatlivsside
assets/style.css                          Fælles design (farver, typografi, komponenter)
assets/site.js                            Theme-toggle og FAQ-toggle
assets/img/lasse.jpg                      Portrætfoto
assets/og/                                Statiske OG-billeder (1200×630) pr. værktøj
content/                                  Kildemateriale for værktøjerne (ikke publiceret direkte)
```

## Sådan tilføjer du et nyt værktøj

Værktøjerne er håndskrevne statiske sider, ikke en genereret liste. Der er ingen JSON-manifest eller build-step.

1. Opret `vaerktoejer/<slug>/index.html` efter samme opskrift som de eksisterende værktøjssider: `.article-hero`, `.article-section` med `.case-card` / `.quote-stack` / `.pull-quote` efter behov, kolofon og `.pdf-request`-blokken i bunden.
2. Tilføj `og:title`, `og:description`, `og:image` (se eksisterende sider) og generér et 1200×630 OG-billede til `assets/og/<slug>.png`.
3. Tilføj et kort til `vaerktoejer/index.html` der linker til den nye side.
4. Commit og push til `main`. Cloudflare Pages bygger og udgiver automatisk, ingen andre skridt.

## PDF-format

Værktøjerne er frie at læse som HTML på siderne. PDF-versionen ligger ikke offentligt tilgængelig i repoet eller på sitet, den rekvireres pr. mail: besøgende skriver til `lasse@mellemmoederne.dk` (emnefelt "håndtag"), og PDF'en sendes manuelt. Mailadresser gemmes ikke til fremtidig brug, se `privatliv/index.html`.

## Cloudflare Pages, opsætning (én gang)

1. Log ind på Cloudflare Dashboard → **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**.
2. Vælg dette repo (`lasseborris-ctrl/mellemmoederne-web`) og branch `main`.
3. Build-indstillinger: **Framework preset: None**, **Build command: (tom)**, **Build output directory: `/`**.
4. Deploy. Hvert push til `main` herefter trigger en ny deployment automatisk.

## Kobl domænet mellemmoederne.dk til

Forudsætning: domænets nameservers peger allerede på Cloudflare (bekræftet).

1. Gå til det oprettede Pages-projekt → **Custom domains** → **Set up a custom domain**.
2. Tilføj `mellemmoederne.dk` og evt. `www.mellemmoederne.dk`.
3. Cloudflare opretter selv de nødvendige DNS-records, da domænet allerede ligger i samme Cloudflare-konto.
4. Vent på certifikat-udstedelse (typisk få minutter), herefter er siden live på domænet.

## E-mail

Kontakt-adressen `lasse@mellemmoederne.dk` bruges direkte som `mailto:`-link. Hvis Cloudflare's "Email Address Obfuscation" er slået til for zonen, obfuskerer Cloudflare selv adressen ved levering, det kræver ingen håndkodning her.
