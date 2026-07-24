# Deploy checklist — livingbeyondstroke.com

A static site on **GitHub → Netlify**, domain via **Cloudflare**. Roughly
30–45 minutes, most of it waiting for DNS.

---

## 0. Before you deploy (do these first)

- [ ] **Decide the guided-imagery page.** Two versions exist. The formal one is
      live in `public/guided_imagery_page.html`. The plain-language one is parked
      in `build/alternates/guided_imagery_page_plain.html`. To use the plain one,
      copy it over the live file (keep the filename `guided_imagery_page.html` so
      every existing link still works), then delete the alternate.
- [ ] **`work_with_jeremy.html`:** swap the placeholder harmonica photo for a
      stroke-neutral image, and set the real session prices (currently USD
      placeholders, flagged in HTML comments).
- [ ] **Record the audio.** The narration scripts are in
      `build/audio_scripts/*.txt`. Recorded files go in
      `public/downloads/audio/` named exactly `audio_arm_hand.mp3`,
      `audio_walking.mp3`, `audio_balance.mp3`, `audio_speech.mp3`,
      `audio_fatigue.mp3` — the exercise pages already point there. Until then the
      players show a graceful fallback and the written scripts remain available.

---

## 1. Domain (Cloudflare)

- [ ] Cloudflare dashboard → **Domain Registration → Register Domains**
- [ ] Register `livingbeyondstroke.com` (optionally `.org` too, to protect the brand)
- [ ] It lands on Cloudflare's nameservers automatically — no nameserver step needed

## 2. GitHub repo

- [ ] Create a new repo (e.g. `living-beyond-stroke`)
- [ ] Push the **entire contents of this folder** to the repo root — so
      `netlify.toml`, `public/`, and `build/` sit at the top level
- [ ] Confirm `public/index.html` exists (it's the homepage Netlify will serve)

## 3. Netlify

- [ ] Netlify → **Add new site → Import an existing project → GitHub** → pick the repo
- [ ] Build settings are read from `netlify.toml` automatically:
      publish directory `public`, no build command. Leave them as detected.
- [ ] Deploy. Test the temporary `*.netlify.app` URL end to end before touching DNS.

## 4. Point the domain (Cloudflare DNS)

- [ ] Netlify → site → **Domain management → Add a domain** → `livingbeyondstroke.com`
- [ ] Netlify shows the DNS target. In **Cloudflare → DNS → Records** add:
  - **A** record, name `@` → `75.2.60.5` (Netlify's load balancer), **or** the
    ALIAS/CNAME target Netlify specifies for the apex
  - **CNAME**, name `www` → your `your-site-name.netlify.app`
- [ ] Set both records to **DNS only** (grey cloud, proxy OFF) for now — Cloudflare's
      proxy interferes with Netlify's SSL provisioning. You can turn the orange
      proxy back on after HTTPS is live, if you want Cloudflare's CDN/analytics.

## 5. HTTPS

- [ ] Wait for DNS to resolve (minutes to a couple of hours). Netlify auto-issues a
      Let's Encrypt certificate.
- [ ] Once issued, enable **Force HTTPS** in Netlify → Domain management.

## 6. Forms

Both forms are plain Netlify forms — no config needed.

- [ ] After first deploy, Netlify → **Forms** should list `contact` and `feedback`.
- [ ] Set the form notification email (Netlify → Forms → Settings → Notifications)
      to Jeremy's address, so submissions are emailed to him.
- [ ] Send a test submission through each to confirm delivery.

## 7. Post-launch niceties (optional)

- [ ] Add the printable PDFs (`public/downloads/pdf/`) as download links on each
      exercise page, if you want them reachable from the site rather than just by URL.
- [ ] Turn Cloudflare proxy (orange cloud) back on for CDN + basic analytics.
- [ ] Add a favicon.
- [ ] Submit the site to Google Search Console.

---

## How the folders work

```
public/     ← the published website (Netlify serves ONLY this)
  *.html
  downloads/
    pdf/    ← printable scripts (3 per practice)
    audio/  ← recorded narration goes here (see step 0)
build/      ← toolkit, NEVER published — safe from public view because it's
              outside public/
  scripts/  ← the single source of truth (one JSON per practice)
  generate.py, partials/, audio_scripts/, README.md
  alternates/ ← the plain-language guided-imagery page, pending your decision
```

To change any practice script: edit `build/scripts/<id>.json`, run
`python3 build/generate.py`, then copy the regenerated
`build/partials/<id>_script.html` into the matching page and the refreshed PDFs
into `public/downloads/pdf/`. See `build/README.md` for detail.
