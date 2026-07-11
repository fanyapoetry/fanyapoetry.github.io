# -*- coding: utf-8 -*-
"""
Static site generator for 凡亞's poetry collection.

Usage:
    cd website
    python3 scripts/generate.py

Reads scripts/data.py (POEMS) and writes:
    index.html
    about.html
    poems/<slug>.html   (one per poem)

No third-party dependencies — standard library only.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from data import POEMS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POEMS_DIR = os.path.join(ROOT, "poems")

AUTHOR = "凡亞"
SITE_TITLE = "凡亞 · 诗集"
SITE_TAGLINE = "Collected Poems"

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?'
    "family=Playfair+Display:ital,wght@0,700;1,700&"
    "family=Noto+Serif:ital,wght@0,400;0,600;1,400&"
    "family=Noto+Serif+SC:wght@400;600&"
    "family=Inter:wght@400;500;600&display=swap"
    '" rel="stylesheet">'
)

CJK_RE = re.compile(r"[一-鿿]")
CYRILLIC_RE = re.compile(r"[Ѐ-ӿ]")
LATIN_RE = re.compile(r"[A-Za-z]")


def esc(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_markup(text):
    """Escape then apply *emphasis* -> <em>emphasis</em>."""
    text = esc(text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def detect_lang(poem):
    text = poem["title"] + "".join(
        "".join(part["lines"]) for part in poem["parts"]
    )
    cjk = len(CJK_RE.findall(text))
    cyr = len(CYRILLIC_RE.findall(text))
    latin = len(LATIN_RE.findall(text))
    counts = {"中文": cjk, "Русский": cyr, "English": latin}
    return max(counts, key=counts.get)


def render_lines_as_stanzas(lines):
    """Group a flat list of lines into stanza <p> blocks, split on
    blank-string separators. A lone '&' line becomes a centered divider."""
    html = []
    stanza = []

    def flush():
        if not stanza:
            return
        if len(stanza) == 1 and stanza[0].strip() == "&":
            html.append('        <div class="poem-divider">&amp;</div>')
        else:
            joined = "<br>".join(
                inline_markup(l.replace("\t", "    ")) for l in stanza
            )
            html.append(f'        <p class="poem-line">{joined}</p>')
        stanza.clear()

    for line in lines:
        if line == "":
            flush()
        else:
            stanza.append(line)
    flush()
    return "\n".join(html)


def render_epigraph(epigraph):
    if not epigraph:
        return ""
    lines_html = "\n".join(
        f"        <p>{inline_markup(l)}</p>" for l in epigraph["lines"]
    )
    cite = ""
    if epigraph.get("attribution"):
        cite = f"        <cite>{inline_markup(epigraph['attribution'])}</cite>\n"
    return f'      <div class="poem-epigraph">\n{lines_html}\n{cite}      </div>\n'


def render_parts(parts):
    blocks = []
    for part in parts:
        label_html = ""
        if part.get("label"):
            label_html = f'        <div class="poem-part__label">{esc(part["label"])}</div>\n'
        body_html = render_lines_as_stanzas(part["lines"])
        blocks.append(f'      <div class="poem-part">\n{label_html}{body_html}\n      </div>')
    return "\n".join(blocks)


def page_shell(title, description, depth, body, active=None, extra_head=""):
    """depth: 0 for root-level pages, 1 for pages inside poems/."""
    prefix = "../" if depth else ""
    nav_items = [
        ("Home", "index.html", "home"),
        ("About", "about.html", "about"),
    ]
    nav_html = "\n".join(
        '        <a href="{href}"{cls}>{label}</a>'.format(
            href=(prefix + href),
            cls=' class="is-active"' if key == active else "",
            label=label,
        )
        for label, href, key in nav_items
    )

    return f"""<!doctype html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  {FONT_LINK}
  <link rel="stylesheet" href="{prefix}css/style.css">
{extra_head}</head>
<body>
  <header class="site-header">
    <div class="site-header__inner">
      <a class="wordmark" href="{prefix}index.html">{AUTHOR}<small>{SITE_TAGLINE}</small></a>
      <nav class="site-nav">
{nav_html}
      </nav>
    </div>
  </header>

{body}

  <footer class="site-footer">
    <div class="site-footer__inner">
      <span>&copy; {AUTHOR}</span>
      <span><a href="{prefix}index.html">Index of Poems</a></span>
    </div>
  </footer>

  <div class="visitor-tracker" aria-hidden="true">
    <script type="text/javascript" id="mapmyvisitors" src="//mapmyvisitors.com/map.js?d=fSyKGPXmTnxk4MFiHPSg3HCBBlN_kawpMl_bpMwMfB4&cl=ffffff&w=a"></script>
  </div>
</body>
</html>
"""


def build_index():
    items = []
    for i, poem in enumerate(POEMS, start=1):
        lang = detect_lang(poem)
        subtitle_html = ""
        if poem.get("subtitle"):
            subtitle_html = f'<span class="subtitle">{inline_markup(poem["subtitle"])}</span>'
        search_blob = esc(poem["title"] + " " + (poem.get("subtitle") or ""))
        items.append(f"""      <li data-search="{search_blob}">
        <a href="poems/{poem['slug']}.html">
          <span class="poem-list__num">{i:02d}</span>
          <span class="poem-list__title">{inline_markup(poem['title'])}{subtitle_html}</span>
          <span class="poem-list__lang">{lang}</span>
        </a>
      </li>""")
    items_html = "\n".join(items)

    body = f"""  <section class="hero">
    <h1 class="hero__title">{AUTHOR}</h1>
    <p class="hero__lede">Poetic License: Selected Poems 2016&ndash;2026</p>
    <p class="hero__meta">{len(POEMS)} Poems &middot; An Exhibition</p>
  </section>

  <section class="index-section">
    <div class="index-section__head">
      <h2>All Poems</h2>
      <input type="search" class="poem-search" data-poem-search placeholder="Search titles&hellip;" aria-label="Search poems by title">
    </div>
    <ul class="poem-list" data-poem-list>
{items_html}
    </ul>
    <p class="no-results" data-no-results>No poems match your search.</p>
  </section>"""

    html = page_shell(
        title=f"{AUTHOR} · Collected Poems",
        description=f"A collection of {len(POEMS)} poems by {AUTHOR}, in Chinese, English, and other languages.",
        depth=0,
        body=body,
        active="home",
        extra_head='  <script defer src="js/main.js"></script>\n',
    )
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_about():
    body = f"""  <section class="about-page">
    <h1>About</h1>
    <p>
      {AUTHOR} writes poems intermittently. He is based on the East Coast and
      remains caught in a prolonged adolescence.
    </p>
  </section>"""
    html = page_shell(
        title=f"About · {AUTHOR}",
        description=f"About {AUTHOR}, poet.",
        depth=0,
        body=body,
        active="about",
    )
    with open(os.path.join(ROOT, "about.html"), "w", encoding="utf-8") as f:
        f.write(html)


def clean_stale_poem_pages(valid_slugs):
    if not os.path.isdir(POEMS_DIR):
        return
    for fname in os.listdir(POEMS_DIR):
        if fname.endswith(".html") and fname[:-5] not in valid_slugs:
            os.remove(os.path.join(POEMS_DIR, fname))
            print(f"Removed stale page: poems/{fname}")


def build_poem_pages():
    os.makedirs(POEMS_DIR, exist_ok=True)
    clean_stale_poem_pages({p["slug"] for p in POEMS})
    n = len(POEMS)
    for i, poem in enumerate(POEMS):
        prev_poem = POEMS[(i - 1) % n]
        next_poem = POEMS[(i + 1) % n]

        subtitle_html = ""
        if poem.get("subtitle"):
            subtitle_html = f'      <p class="poem-subtitle">{inline_markup(poem["subtitle"])}</p>\n'

        epigraph_html = render_epigraph(poem.get("epigraph"))
        parts_html = render_parts(poem["parts"])

        note_html = ""
        if poem.get("note"):
            note_html = f'      <p class="poem-note">{inline_markup(poem["note"])}</p>\n'

        body = f"""  <main class="poem-page">
    <p class="poem-nav-top"><a href="../index.html">&larr; Index of Poems</a></p>
    <article>
      <p class="poem-index-num">No. {i + 1:02d} of {n}</p>
      <h1 class="poem-title">{inline_markup(poem['title'])}</h1>
{subtitle_html}{epigraph_html}      <div class="poem-body">
{parts_html}
      </div>
{note_html}      <p class="poem-byline">&mdash; <strong>{AUTHOR}</strong></p>
    </article>

    <nav class="poem-pager">
      <a class="poem-pager__link is-prev" href="{prev_poem['slug']}.html">
        <span class="poem-pager__dir">&larr; Previous</span>
        <span class="poem-pager__title">{inline_markup(prev_poem['title'])}</span>
      </a>
      <a class="poem-pager__link is-next" href="{next_poem['slug']}.html">
        <span class="poem-pager__dir">Next &rarr;</span>
        <span class="poem-pager__title">{inline_markup(next_poem['title'])}</span>
      </a>
    </nav>
  </main>"""

        html = page_shell(
            title=f"{poem['title']} · {AUTHOR}",
            description=f"“{poem['title']}” — a poem by {AUTHOR}.",
            depth=1,
            body=body,
        )
        out_path = os.path.join(POEMS_DIR, f"{poem['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)


def main():
    build_index()
    build_about()
    build_poem_pages()
    print(f"Generated index.html, about.html, and {len(POEMS)} poem pages in poems/.")


if __name__ == "__main__":
    main()
