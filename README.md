# Living Beyond Stroke

A free guided-imagery programme supporting rehabilitation after stroke. Static
website, no backend beyond Netlify's built-in form handling.

## Structure

- **`public/`** — the website. This is the only folder Netlify publishes.
- **`build/`** — the toolkit that generates the practice scripts, PDFs, and audio
  narration text from a single source of truth (`build/scripts/*.json`). Not
  published. See `build/README.md`.
- **`netlify.toml`** — publish settings and headers.
- **`DEPLOY.md`** — step-by-step launch checklist (domain, GitHub, Netlify, DNS, forms).

## Editing content

Ordinary page edits: change the HTML in `public/` directly.

Practice-script edits: **do not** hand-edit the script text in the exercise
pages. Edit `build/scripts/<practice>.json`, re-run `python3 build/generate.py`,
and copy the regenerated partial and PDFs into `public/`. This keeps the website,
the printable PDFs, and the audio narration scripts all in sync. Details in
`build/README.md`.

## Not a medical service

This is an educational resource. It does not replace physiotherapy, occupational
therapy, or speech-language pathology, and it makes no treatment guarantees.
