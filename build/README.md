# Guided Imagery Scripts — Single Source of Truth

All five practice scripts now live in **one place** and every other format is
generated from it. Edit the source, re-run the generator, and the audio scripts,
the printable PDFs, and the website script blocks all update together. This
prevents the scripts drifting out of sync across formats.

## The source

`scripts/arm_hand.json`, `walking.json`, `balance.json`, `speech.json`,
`fatigue.json` — one file per practice.

Each paragraph is either:

- **plain text** — identical in every version, or
- a small block with three wordings:
  - `agnostic` — the inclusive wording. Never tells the reader to "picture" or
    "watch"; it offers the image and lets them take it visually, as a feeling,
    or simply as knowing. **This is the version used for the audio**, and the
    default shown on the website.
  - `see` — leans into seeing, for strong visualisers.
  - `feel` — leans into felt sensation, for people who image faintly or not at
    all (including aphantasia).

Only the imagery-cue paragraphs carry all three. Everything else is written once.

## What gets generated

Run `python3 generate.py` (needs `reportlab`). It writes into `dist/`:

| Output | What it is | How many |
|---|---|---|
| `audio_scripts/<id>.txt` | Narration script in the inclusive wording, ready to record (e.g. ElevenLabs). One per practice — **not** three. | 5 |
| `pdf/<id>_both.pdf` | Printable script, standard wording | 5 |
| `pdf/<id>_see.pdf` | Printable script, visual wording | 5 |
| `pdf/<id>_feel.pdf` | Printable script, felt-sense wording | 5 |
| `partials/<id>_script.html` | The website script block: agnostic text as the visible default, with `data-see` / `data-feel` on the paragraphs that vary. Drops straight into the exercise page's cue toggle. | 5 |

## Why audio is one file, not three

Recording, storing, and re-recording three versions of five practices (15 audio
files) is a maintenance trap. The inclusive wording removes the need: because it
never assumes a channel, it serves the strong visualiser and the person with
aphantasia from the same recording. The website toggle and the PDFs still offer
the sharper per-channel wording for anyone who wants it in text.

## To change a script

1. Edit the relevant `scripts/<id>.json`.
2. Run `python3 generate.py`.
3. The regenerated `partials/<id>_script.html` can be re-injected into the
   exercise page; the PDFs and audio script are refreshed automatically.

Do not edit the generated files by hand — the next run overwrites them.
