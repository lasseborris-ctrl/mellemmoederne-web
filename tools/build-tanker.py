#!/usr/bin/env python3
"""Bygger /tanker/ ud fra content/tanker/*.md.

Kør fra repoets rod:  python tools/build-tanker.py

Skriver:
  tanker/index.html            oversigten, en sektion pr. værdi
  tanker/<slug>/index.html     én side pr. historie
  index.html                   kun blokken mellem <!-- tanker:featured --> og <!-- /tanker:featured -->

Ny historie: læg NN-slug.md i content/tanker/ (samme frontmatter som de andre) og en evt.
tegning i assets/tanker/, og kør scriptet igen. Head, nav og footer kopieres fra
vaerktoejer/index.html, så de altid matcher resten af sitet.
"""
import glob, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "content", "tanker")
SITE = "https://mellemmoederne.dk"
CALENDLY = "https://calendly.com/mellemmoederne"
MONTHS = ["januar", "februar", "marts", "april", "maj", "juni", "juli", "august", "september", "oktober", "november", "december"]

# Værdi -> (anker, bærende sætning). Rækkefølgen her er rækkefølgen på /tanker/.
VALUES = [
    ("Hørt og set", "hoert-og-set", "Spørgsmålene bærer intet alene. Det kræver, at man rummer det, der kommer tilbage."),
    ("Kasser eller kasseret?", "kasser-eller-kasseret", "Hvor hurtigt vi beslutter os for, hvem mennesker er, ud fra den måde, de optræder på i ét bestemt rum."),
    ("Kommunikation i ledelse", "kommunikation-i-ledelse", "Det, jeg gør, bliver hurtigt læst som det, jeg forventer."),
    ("Kapacitet", "kapacitet", "Det er ikke dovenskab. Det er mental overload."),
    ("Plads til de stille", "plads-til-de-stille", "Det handler ikke om at være den mest højtråbende, men den mest lyttende."),
    ("Vaner", "vaner", "Hun er ikke i gang med at huske en regel. Hun er i gang med at blive en, der tager cykelhjelm på."),
]
ANCHOR = {name: anchor for name, anchor, _ in VALUES}
# Historierne, der vises under "Historierne bag" på forsiden.
FEATURED = ["datter-paa-gulvet", "cykelhjelm", "engel-gennem-stuen"]


def frontmatter(head):
    meta = {}
    for line in head.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        val = val.strip()
        if val.startswith('"') and val.endswith('"'):
            val = json.loads(val)
        meta[key.strip()] = val
    return meta


def parse(path):
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    head, body = raw.split("\n---\n", 1)
    meta = frontmatter(head.lstrip("-\n"))
    meta["body"] = body.strip()
    meta["slug"] = os.path.basename(path)[3:-3]
    meta["min"] = max(1, round(len(body.split()) / 200))
    if meta.get("billede") in ("", "ingen"):
        meta["billede"] = None
    return meta


def esc(s):
    return html.escape(s, quote=True)


def inline(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(s, quote=False))


def body_html(md):
    out = []
    for block in re.split(r"\n\s*\n", md):
        lines = block.strip().splitlines()
        if not lines:
            continue
        if all(l.startswith("> ") for l in lines):
            out.append("<blockquote>" + "<br>".join(inline(l[2:]) for l in lines) + "</blockquote>")
        else:
            out.append("<p>" + "<br>".join(inline(l) for l in lines) + "</p>")
    return "\n".join(out)


def month(d):
    return f"{MONTHS[int(d[5:7]) - 1]} {d[:4]}"


def img_key(p):
    return p["billede"].rsplit(".", 1)[0]


def visual(p, cls):
    if p["billede"]:
        return (f'<img class="{cls} img-{img_key(p)}" src="/assets/tanker/{esc(p["billede"])}" '
                f'alt="Illustration til {esc(p["titel"])}" loading="lazy">')
    return f'<div class="quote-vis"><span>“{esc(p["pointe"])}”</span></div>'


def story_card(p, show_value=True):
    tag = f'<span class="tag">{esc(p["vaerdi"])}</span>' if show_value else ""
    return f"""<a class="story" href="/tanker/{p['slug']}/">
          {visual(p, "card-vis")}
          <div class="story-txt">{tag}<h3>{esc(p['titel'])}</h3><p class="teaser">{esc(p['teaser'])}</p><span class="meta">{p['min']} min · {month(p['dato'])}</span></div>
        </a>"""


# ---------- skabelon fra vaerktoejer/index.html ----------
tpl = open(os.path.join(ROOT, "vaerktoejer", "index.html"), encoding="utf-8").read()
HEAD_TAIL = tpl[tpl.index('<link rel="icon"'):tpl.index("</head>")]
NAV = re.search(r"<nav>.*?</nav>", tpl, re.S).group(0)
FOOTER = re.search(r"<footer>.*?</footer>", tpl, re.S).group(0)


def page(title, desc, path, body, og_type="website", image=None):
    url = SITE + path
    og_img = ""
    if image:
        og_img = f'\n<meta property="og:image" content="{SITE}/assets/tanker/{esc(image)}">\n<meta name="twitter:card" content="summary_large_image">'
    return f"""<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">{og_img}
{HEAD_TAIL}</head>
<body>

<!-- Genereret af tools/build-tanker.py. Ret i content/tanker/*.md og kør scriptet igen. -->

{NAV}

{body}

{FOOTER}

<script src="/assets/site.js"></script>
</body>
</html>
"""


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


posts = [parse(f) for f in sorted(glob.glob(os.path.join(SRC, "[0-9][0-9]-*.md")))]
BY = {p["slug"]: p for p in posts}
for p in posts:
    if p["vaerdi"] not in ANCHOR:
        raise SystemExit(f"Ukendt værdi '{p['vaerdi']}' i {p['slug']}. Tilføj den til VALUES.")
    if p["billede"] and not os.path.exists(os.path.join(ROOT, "assets", "tanker", p["billede"])):
        raise SystemExit(f"Mangler assets/tanker/{p['billede']} til {p['slug']}.")

# ---------- /tanker/ ----------
chips = "\n      ".join(f'<a href="#{a}">{esc(n)}</a>' for n, a, _ in VALUES)
secs = []
for i, (name, anchor, bline) in enumerate(VALUES, 1):
    cards = "\n        ".join(story_card(p, show_value=False) for p in posts if p["vaerdi"] == name)
    if not cards:
        continue
    secs.append(f"""<section class="vsec" id="{anchor}">
  <div class="wrap">
    <span class="idx">{i:02d}</span>
    <h2>{esc(name)}</h2>
    <blockquote class="pull">{esc(bline)}</blockquote>
    <div class="sgrid">
        {cards}
    </div>
  </div>
</section>""")

lede = f"{len(posts)} historier fra mit eget lederskab og min egen hverdag. Hver af dem ender i noget, du kan bruge."
index_body = f"""<header class="hero">
  <div class="wrap">
    <div class="label">Tanker</div>
    <h1>Det jeg står for,<br><em>fortalt gennem det, jeg har oplevet.</em></h1>
    <p class="lede">{lede}</p>
    <div class="chips">
      {chips}
    </div>
  </div>
</header>

{chr(10).join(secs)}"""
write("tanker/index.html", page("Tanker · Lasse B. Schnipper", lede, "/tanker/", index_body))

# ---------- /tanker/<slug>/ ----------
for idx, p in enumerate(posts):
    nxt = posts[(idx + 1) % len(posts)]
    vis = visual(p, "art-vis") if p["billede"] else ""
    body = f"""<main class="art">
  <div class="article-wrap">
    <a class="back" href="/tanker/#{ANCHOR[p['vaerdi']]}">← {esc(p['vaerdi'])}</a>
    <div class="label">{esc(p['vaerdi'])} · {p['min']} min</div>
    <h1 class="art-h">{esc(p['titel'])}</h1>
    {vis}
    <div class="art-body">
{body_html(p['body'])}
    </div>
    <p class="orig">Først bragt på LinkedIn, {month(p['dato'])}.</p>
    <div class="art-cta"><strong>Kender du situationen fra dit eget team?</strong><br>Tag den med til en første samtale. 45 minutter, ingen slides.<br><a class="btn-primary" href="{CALENDLY}" target="_blank" rel="noopener">Book en tid</a></div>
    <a class="next" href="/tanker/{nxt['slug']}/"><span class="meta">Næste historie</span>{esc(nxt['titel'])} →</a>
  </div>
</main>"""
    write(f"tanker/{p['slug']}/index.html",
          page(f"{p['titel']} · Lasse B. Schnipper", p["teaser"], f"/tanker/{p['slug']}/", body,
               og_type="article", image=p["billede"]))

# Fjern genererede sider for historier, der er omdøbt eller slettet.
for old in glob.glob(os.path.join(ROOT, "tanker", "*", "index.html")):
    slug = os.path.basename(os.path.dirname(old))
    if slug not in BY and "Genereret af tools/build-tanker.py" in open(old, encoding="utf-8").read():
        os.remove(old)
        os.rmdir(os.path.dirname(old))
        print(f"fjernet: tanker/{slug}/")

# ---------- forsidens "Historierne bag" ----------
idx_path = os.path.join(ROOT, "index.html")
front = open(idx_path, encoding="utf-8").read()
featured = "\n        ".join(story_card(BY[s]) for s in FEATURED)
block = f"""<!-- tanker:featured -->
    <div class="sgrid">
        {featured}
    </div>
    <p><a class="btn-ghost" href="/tanker/">Alle {len(posts)} historier →</a></p>
    <!-- /tanker:featured -->"""
front, n = re.subn(r"<!-- tanker:featured -->.*?<!-- /tanker:featured -->", lambda m: block, front, flags=re.S)
if n != 1:
    raise SystemExit("Fandt ikke <!-- tanker:featured --> i index.html.")
with open(idx_path, "w", encoding="utf-8", newline="") as f:
    f.write(front)

print(f"ok: {len(posts)} historier, {sum(1 for p in posts if p['billede'])} med tegning")
