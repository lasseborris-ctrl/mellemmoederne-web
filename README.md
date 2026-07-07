# mellemmoederne-web

Offentlig landingsside for MellemMøderne (Lasse B. Schnipper). Ren statisk HTML/CSS/JS — ingen build-step, intet framework. Hostes via Cloudflare Pages, koblet direkte til dette GitHub-repo: hvert push til `main` deployer automatisk.

## Struktur

```
index.html            Forside (about, services, why, work, faq, kontakt)
vaerktoejer/index.html PDF-værktøjsbibliotek
assets/style.css       Fælles design (farver, typografi, komponenter)
assets/site.js         Theme-toggle, FAQ-toggle, render af værktøjsliste
assets/tools.json      Manifest over de udgivne PDF-værktøjer
assets/pdfs/           De faktiske PDF-filer
```

## Sådan tilføjer du et nyt PDF-værktøj

1. Læg PDF-filen i `assets/pdfs/`, f.eks. `assets/pdfs/moede-tjekliste.pdf`.
2. Åbn `assets/tools.json` og tilføj et objekt til listen:

   ```json
   {
     "title": "Møde-tjekliste",
     "description": "Kort beskrivelse af hvad værktøjet hjælper med.",
     "filename": "moede-tjekliste.pdf",
     "date": "2026-07-07"
   }
   ```

3. Commit og push til `main`. Cloudflare Pages bygger og udgiver automatisk — ingen andre skridt.

Er listen tom, viser siden en pæn "på vej"-besked i stedet for at se tom/fejlbehæftet ud.

## Cloudflare Pages — opsætning (én gang)

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

Kontakt-adressen `lasse@mellemmoederne.dk` bruges direkte som `mailto:`-link. Hvis Cloudflare's "Email Address Obfuscation" er slået til for zonen, obfuskerer Cloudflare selv adressen ved levering — det kræver ingen håndkodning her.
