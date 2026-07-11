# 凡亞 · Poetry Collection

A minimalist, editorial website exhibiting 凡亞's poetry — 55 poems, in Chinese,
English, and fragments of other languages. Styled in the spirit of *The Paris
Review* and the *Poetry Foundation*: warm paper background, restrained serif
typography, generous whitespace, no clutter.

This is a **static site** — plain HTML/CSS/JS, no build tools, no server
required. It is generated from a small Python script so the poems stay easy
to edit.

## Structure

```
website/
├── index.html          the homepage — hero + full index of all poems
├── about.html           short "about the poet" page
├── poems/
│   └── <slug>.html      one page per poem (55 files, auto-generated)
├── css/style.css        all styling (light + dark mode via prefers-color-scheme)
├── js/main.js           the instant title-search on the homepage
├── scripts/
│   ├── data.py           the source of truth: every poem's text, in order
│   └── generate.py       reads data.py, writes index.html / about.html / poems/*.html
└── .nojekyll             tells GitHub Pages to serve the files as-is
```

## Editing poems

Don't hand-edit files inside `poems/` — they're generated and will be
overwritten. Instead:

1. Open `scripts/data.py`.
2. Add, remove, or edit a poem entry (see the docstring at the top of the
   file for the format — title, optional subtitle/epigraph, the poem's text
   broken into parts and lines, optional footnote).
3. From the `website/` folder, run:
   ```bash
   python3 scripts/generate.py
   ```
   This rewrites `index.html`, `about.html`, and every file in `poems/`.
4. Preview locally before publishing (see below), then commit and push.

Requires only Python 3 (no packages to install).

## Previewing locally

From the `website/` folder:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` in a browser. (Opening `index.html`
directly by double-clicking works for basic viewing, but the search box and
some relative links behave best when served over `http://`.)

## Publishing with GitHub Pages

You said you want this hosted on GitHub — here's the full path from an empty
GitHub account to a live URL.

### 1. Create the repository

- Go to [github.com/new](https://github.com/new).
- Name it anything you like — for a personal site at
  `https://<your-username>.github.io/`, name it exactly
  `<your-username>.github.io`. For a project site at
  `https://<your-username>.github.io/poems/`, name it e.g. `poems` (any name
  works).
- Leave it **public** (GitHub Pages on a free account requires a public repo,
  unless you have GitHub Pro/Team/Enterprise).
- Don't initialize it with a README, .gitignore, or license — this folder
  already has what it needs.

### 2. Push this folder to GitHub

In your terminal:

```bash
cd /Users/fanyangyu/Desktop/fanya/website
git init
git add .
git commit -m "Initial commit: 凡亞's poetry collection"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Replace `<your-username>` and `<repo-name>` with your actual GitHub username
and the repository name you chose in step 1. GitHub will prompt you to sign
in (via browser or a personal access token) the first time you push.

### 3. Turn on GitHub Pages

- On GitHub, open your repository → **Settings** → **Pages** (left sidebar).
- Under "Build and deployment" → "Source", choose **Deploy from a branch**.
- Under "Branch", choose **main** and folder **/ (root)**, then **Save**.
- Wait a minute or two. GitHub will show a banner with your live URL:
  - `https://<your-username>.github.io/` (if you named the repo
    `<your-username>.github.io`), or
  - `https://<your-username>.github.io/<repo-name>/` otherwise.

That's it — the site is live. Every time you `git push` new changes, GitHub
Pages redeploys automatically within a minute or two.

### 4. (Optional) Custom domain

If you own a domain, Settings → Pages → "Custom domain" lets you point it at
the site; GitHub will walk you through the DNS records to add.

## Updating the live site later

```bash
cd /Users/fanyangyu/Desktop/fanya/website
# edit scripts/data.py to add/change poems
python3 scripts/generate.py
git add .
git commit -m "Add new poem(s)"
git push
```

## Notes on the design

- **Typography**: Playfair Display for display headings, Noto Serif /
  Noto Serif SC for poem body text (covers Chinese, English, and Cyrillic in
  one stack), Inter for small UI labels. Loaded from Google Fonts via CDN.
- **Color**: warm paper background with a single brick-red accent; a dark
  mode is included automatically via `prefers-color-scheme`, no toggle
  needed.
- **Poem formatting**: each poem preserves its original line breaks, stanza
  spacing, multi-part structure (一/二/三, 1./2./3., or `&` dividers),
  epigraphs with attribution, dedications, and footnotes exactly as written
  in the source manuscript.
- **No tracking, no analytics, no external requests** other than the Google
  Fonts stylesheet.
